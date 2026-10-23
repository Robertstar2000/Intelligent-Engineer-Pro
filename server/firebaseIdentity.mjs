// Server-only identity boundary. Identity verification never grants paid access.
export function createFirebaseIdentityHandler({ projectId, verifyToken }) {
  return async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const match = /^Bearer ([^\s]+)$/i.exec(req.headers.authorization || '');
    if (!match || match[1].length > 16384) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    if (!projectId) {
      return res.status(503).json({ error: 'Identity verification is not configured' });
    }
    try {
      const identity = await verifyToken(match[1], projectId);
      if (!identity?.uid || identity.aud !== projectId ||
          identity.iss !== 'https://securetoken.google.com/' + projectId) {
        return res.status(401).json({ error: 'Invalid authentication token' });
      }
      return res.json({ user: {
        id: identity.uid,
        email: identity.email || null,
        emailVerified: identity.email_verified === true,
      } });
    } catch (error) {
      const code = error?.code;
      const invalidToken = ['auth/id-token-expired', 'auth/id-token-revoked',
        'auth/invalid-id-token', 'auth/argument-error', 'auth/user-disabled',
        'auth/user-not-found'].includes(code);
      return res.status(invalidToken ? 401 : 503).json({
        error: invalidToken ? 'Invalid authentication token' : 'Identity verification unavailable',
      });
    }
  };
}

export async function verifyFirebaseToken(token, projectId) {
  // Cloud Run supplies Application Default Credentials through its service identity.
  // No browser tokens, private keys, or credentials are logged or stored here.
  const { getApps, initializeApp, applicationDefault } = await import('firebase-admin/app');
  const { getAuth } = await import('firebase-admin/auth');
  const name = 'mifeco-engineering-identity';
  const app = getApps().find(app => app.name === name) ||
    initializeApp({ projectId, credential: applicationDefault() }, name);
  return getAuth(app).verifyIdToken(token, true);
}
