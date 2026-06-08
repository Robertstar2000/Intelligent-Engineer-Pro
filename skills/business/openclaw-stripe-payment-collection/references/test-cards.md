# Stripe Test Card Numbers

## Successful Payments

| Card Number | Brand | Scenario |
|-------------|-------|----------|
| 4242 4242 4242 4242 | Visa | Default success |
| 5555 5555 5555 4444 | Mastercard | Success |
| 3782 822463 10005 | American Express | Success |
| 6011 1111 1111 1117 | Discover | Success |

## Declined Payments

| Card Number | Decline Reason |
|-------------|----------------|
| 4000 0000 0000 0002 | Generic decline |
| 4000 0000 0000 9995 | Insufficient funds |
| 4000 0000 0000 9987 | Lost card |
| 4000 0000 0000 9979 | Stolen card |
| 4000 0000 0000 9961 | Expired card |
| 4000 0000 0000 9953 | Incorrect CVC |
| 4000 0000 0000 9946 | Processing error |
| 4000 0000 0000 9938 | Incorrect number |

## 3D Secure

| Card Number | Scenario |
|-------------|----------|
| 4000 0025 0000 3155 | 3D Secure required (frictionless) |
| 4000 0027 6000 3184 | 3D Secure required (challenge) |

## Test Card Details

- **Expiry:** Any future date (MM/YY)
- **CVC:** Any 3 digits (4 for Amex)
- **ZIP:** Any 5 digits

## International Cards

| Card Number | Country |
|-------------|---------|
| 4000 0076 4000 0002 | Brazil |
| 4000 0052 4000 0002 | Mexico |
| 4000 0037 2000 0002 | India |
| 4000 0055 4000 0002 | Japan |
