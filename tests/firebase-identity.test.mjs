import test from 'node:test';
import assert from 'node:assert/strict';
import { createFirebaseIdentityHandler } from '../server/firebaseIdentity.mjs';

async function request({ token = 'Bearer token', projectId = 'engineering-test', verifyToken = async () => ({
  uid: 'verified-user', aud: 'engineering-test',
  iss: 'https://securetoken.google.com/engineering-test',
  email: 'owner@example.test', email_verified: true, geminiKey: 'must-not-leak',
  plan: 'business',
}) } = {}) {
  let status = 200, body;
  const headers = {};
  await createFirebaseIdentityHandler({ projectId, verifyToken })(
    { headers: { authorization: token }, body: { uid: 'forged-user', plan: 'business' } },
    { setHeader(key, value) { headers[key] = value; },
      status(value) { status = value; return this; },
      json(value) { body = value; return this; } });
  return { status, body, headers };
}
test('only verified identity is returned; no user-supplied identity or paid claims', async () => {
  const result = await request();
  assert.equal(result.status, 200);
  assert.deepEqual(result.body, { user: { id: 'verified-user', email: 'owner@example.test', emailVerified: true } });
  assert.equal(result.headers['Cache-Control'], 'no-store');
});
test('missing, malformed, and oversized bearer tokens never reach verification', async () => {
  for (const token of ['', 'Basic token', 'Bearer two tokens', 'Bearer ' + 'x'.repeat(16385)]) {
    const result = await request({ token, verifyToken: () => assert.fail('Must not verify malformed input') });
    assert.equal(result.status, 401);
  }
});
test('unconfigured identity service fails closed', async () => {
  assert.equal((await request({ projectId: '', verifyToken: () => assert.fail('Not configured') })).status, 503);
});
test('wrong project and issuer cannot authenticate', async () => {
  for (const identity of [
    { uid: 'user', aud: 'other', iss: 'https://securetoken.google.com/engineering-test' },
    { uid: 'user', aud: 'engineering-test', iss: 'https://attacker.example' },
    { aud: 'engineering-test', iss: 'https://securetoken.google.com/engineering-test' },
  ]) {
    assert.equal((await request({ verifyToken: async () => identity })).status, 401);
  }
});
test('expired/revoked/disabled tokens are denied without leaking provider errors', async () => {
  for (const code of ['auth/id-token-expired', 'auth/id-token-revoked', 'auth/user-disabled']) {
    const result = await request({ verifyToken: async () => { throw Object.assign(new Error('private detail'), { code }); } });
    assert.equal(result.status, 401);
    assert.equal(result.body.error, 'Invalid authentication token');
  }
});
test('provider outage fails closed with retryable service status', async () => {
  const result = await request({ verifyToken: async () => { throw new Error('private credential path'); } });
  assert.equal(result.status, 503);
  assert.equal(result.body.error, 'Identity verification unavailable');
});
