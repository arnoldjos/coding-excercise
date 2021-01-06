from flask import Flask, jsonify, request
from payment_providers import ProcessPayment

app = Flask(__name__)


@app.route('/process_payment', methods=["POST"])
def process_payment():
    response = {"status": "success", "description": "success"}
    status = 200
    try:
        data = request.get_json()
        data = data if data else {}

        cc_number = data.get("CreditCardNumber")
        card_holder = data.get("CardHolder")
        exp_date = data.get("ExpirationDate")
        security_code = data.get("SecurityCode")
        amount = data.get("Amount")
        success = data.get("success", True)
        retry = data.get("retry", 0)

        payment = ProcessPayment().process(cc_number, card_holder, exp_date, security_code, amount, success, retry)
        if payment:
            response["description"] = "Payment is processed."
        else:
            response["description"] = "The request is invalid."
            response["status"] = "fail"
            status = 400
    except Exception as e:
        response["status"] = "fail"
        response["description"] = "The request is invalid."
        status = 500
    return response, status


if __name__ == '__main__':
    app.run()
