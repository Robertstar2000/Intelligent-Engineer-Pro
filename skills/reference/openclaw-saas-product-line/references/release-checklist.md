# Release Readiness Checklist

Use this checklist when assessing whether a SaaS product is ready to ship commercially.

---

## 1. Onboarding

- [ ] New users can sign up and access core features without assistance
- [ ] Onboarding flow is documented (screenshot walkthrough or video)
- [ ] First-run experience is frictionless (ideally < 5 minutes to value)
- [ ] Placeholder content or sample data exists for new accounts
- [ ] Error messages during onboarding are actionable

---

## 2. Authentication & Account Lifecycle

- [ ] Sign up, email verification, login, and logout work end-to-end
- [ ] Password reset flow is functional
- [ ] Session management is secure (JWT/expiry, refresh tokens if applicable)
- [ ] Account deletion or data export path exists (GDPR compliance consideration)
- [ ] No hardcoded test credentials in production

---

## 3. Billing Entry Point

- [ ] At least one Stripe payment link or checkout flow exists
- [ ] Pricing page or doc is accurate and matches actual product
- [ ] Upgrade/downgrade/cancel paths are functional
- [ ] Failed payment handling is graceful (no silent failures)
- [ ] Receipt or confirmation is sent after payment

---

## 4. Legal Pages

- [ ] Terms of Service published
- [ ] Privacy Policy published
- [ ] Cookie policy if EU/GDPR relevant
- [ ] Refund policy is stated

---

## 5. Support Path

- [ ] Help docs or FAQ exists (even minimal)
- [ ] Contact support path is clear (email, form, or chat)
- [ ] Response time expectation is set
- [ ] Known issue / status page exists or is planned

---

## 6. Observability & Error Handling

- [ ] Errors are logged to a monitoring system (Sentry, etc.)
- [ ] Alerts exist for critical failures
- [ ] Error messages shown to users are not stack traces
- [ ] Uptime is being tracked
- [ ] Basic dashboards exist for support investigation

---

## 7. Analytics & Conversion Tracking

- [ ] Page views are tracked (even via simple analytics)
- [ ] Sign-up funnel is measurable
- [ ] Payment or CTA clicks are tracked
- [ ] Stripe events are being received (for webhook verification)
- [ ] Key conversion events are identifiable in data

---

## 8. Demoability

- [ ] A shareable demo account or sandbox exists (if applicable)
- [ ] Screenshots of key features are capturable
- [ ] A demo video or GIF can be produced in under an hour
- [ ] Feature walkthrough doc exists for sales use

---

## 9. Installation Clarity

- [ ] README includes clear install/run steps
- [ ] One-click deploy option exists (Railway, Vercel, Render, etc.) OR self-host docs are complete
- [ ] Environment variables are documented
- [ ] Dependencies and versions are pinned
- [ ] Common setup errors have documented fixes

---

## 10. Upgrade Path & Versioning

- [ ] Changelog exists (even minimal — what changed in each release)
- [ ] Version numbers follow semver or clear convention
- [ ] Migration steps for config or data changes are documented
- [ ] Breaking changes are flagged

---

## 11. Security Foundations

- [ ] No secrets or keys in repo
- [ ] Environment variables used for all sensitive config
- [ ] HTTPS enforced in production
- [ ] Input validation on all user-facing endpoints
- [ ] Rate limiting exists on auth and payment endpoints

---

## Bucket Summary

| Category | Status |
|----------|--------|
| Onboarding | |
| Auth & Account | |
| Billing Entry | |
| Legal Pages | |
| Support Path | |
| Observability | |
| Analytics | |
| Demoability | |
| Installation | |
| Upgrade Path | |
| Security | |

**Overall readiness:** Ready / Near-ready / Not-ready

---

## Launch blockers (priority order)

1.
2.
3.

---
