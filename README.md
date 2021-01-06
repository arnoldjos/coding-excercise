# coding-excercise

Printed out the validations and also the error for debugging.


Added success(boolean) and retry(int) parameter for testing.

How to use:
- Set success to true to test successfull payment
- Set number of retries using the retry param and set success to false for testing retrying of payment.

Example post data:
```
{
    "CreditCardNumber": "5540455316944240",
    "CardHolder": "Test Name",
    "ExpirationDate": "2021-01-10 01:10",
    "SecurityCode": "123",
    "Amount": 501,
    "success": false,
    "retry": 2
}
```