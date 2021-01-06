import datetime

class ProcessPayment:
    MAX_CHEAP_PAYMENT_RETRY = 1
    MAX_PREMIUM_PAYMENT_RETRY = 3

    def process(self, cc_number, card_holder, exp_date, security_code, amount, success=True, retry=0):

        is_valid = self.validate_values(cc_number, card_holder, exp_date, security_code, amount)
        if is_valid is False:
            return False

        if amount < 20:
            return CheapPaymentGateway(cc_number, card_holder, exp_date, security_code, amount).process_payment(success)
        elif amount >= 21 and amount <= 500:
            count = 0
            payment = ExpensivePaymentGateway(cc_number, card_holder, exp_date, security_code,
                                              amount).process_payment(success)
            if payment:
                return payment
            else:
                success = False
                while count != self.MAX_CHEAP_PAYMENT_RETRY and retry > 0:
                    count += 1
                    if count == retry:
                        success = True
                    payment = CheapPaymentGateway(cc_number, card_holder, exp_date, security_code,
                                                  amount).process_payment(success)
                    if payment:
                        return payment
        elif amount > 500:
            count = 0
            success = False
            while count != self.MAX_CHEAP_PAYMENT_RETRY and retry > 0:
                count += 1
                if count == retry:
                    success = True
                payment = PremiumPaymentGateway(cc_number, card_holder, exp_date, security_code,
                                                amount).process_payment(success)
                if payment:
                    return payment
        return False

    def validate_values(self, cc_number, card_holder, exp_date, security_code, amount):
        try:
            expire = datetime.datetime.strptime(exp_date, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date time format")
            return False

        date_now = datetime.datetime.now()
        if not cc_number or self.validate_credit_card(cc_number) is False:
            print("Invalid CC Number")
            return False
        elif not card_holder or type(card_holder) != str:
            print("Invalid Card Holder")
            return False
        elif not expire or date_now > expire:
            print("Invalid Exp Date")
            return False
        elif not security_code or len(security_code) != 3 or type(security_code) != str:
            print("Invalid Security Code")
            return False
        elif amount < 0 or type(amount) != int:
            print("Invalid Amount")
            return False
        return True

    @staticmethod
    def validate_credit_card(cc_number):
        cc_num = cc_number[::-1]
        cc_num = [int(x) for x in cc_num]

        doubled_second_numbers = []
        for index, num in enumerate(cc_num):
            if (index + 1) % 2 == 0:
                doubled_second_numbers.append(num * 2)
            else:
                doubled_second_numbers.append(num)

        sum_nums = lambda x: x if x < 10 else (x % 10) + (x // 10)
        doubled_second_numbers = [sum_nums(x) for x in doubled_second_numbers]
        return sum(doubled_second_numbers) % 10 == 0


class PaymentGateway:

    def __init__(self, cc_number, card_holder, exp_date, security_code, amount):
        self.cc_number = cc_number
        self.card_holder = card_holder
        self.exp_date = exp_date
        self.amount = amount
        self.security_code = security_code

    def process_payment(self):
        raise NotImplementedError


class PremiumPaymentGateway(PaymentGateway):
    name = "Premium"

    def __init__(self, cc_number, card_holder, exp_date, security_code, amount):
        super().__init__(cc_number, card_holder, exp_date, security_code, amount)

    def process_payment(self, success=True):
        print(f"Processing - {self.name}")
        if success:
            print(f"Processed - {self.amount} for {self.card_holder}")
        return success


class ExpensivePaymentGateway(PaymentGateway):
    name = "Expensive"

    def __init__(self, cc_number, card_holder, exp_date, security_code, amount):
        super().__init__(cc_number, card_holder, exp_date, security_code, amount)

    def process_payment(self, success=True):
        print(f"Processing - {self.name}")
        if success:
            print(f"Processed - {self.amount} for {self.card_holder}")
        return success


class CheapPaymentGateway(PaymentGateway):
    name = "Cheap"

    def __init__(self, cc_number, card_holder, exp_date, security_code, amount):
        super().__init__(cc_number, card_holder, exp_date, security_code, amount)

    def process_payment(self, success=True):
        print(f"Processing - {self.name}")
        if success:
            print(f"Processed - {self.amount} for {self.card_holder}")
        return success
