from tastypie.authorization import Authorization
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from payment.models.payment_model import payment_details
from payment.validators.__common_validators__ import ModelFormValidation
from payment.forms.payment_forms import payment_detailsForm
from datetime import datetime
from tastypie.resources import ModelResource
APP_ID = "68548109-ce24-4831-gstd-8659-2e42d1bcd87"


class process_paymentResource(ModelResource):
    class Meta:
        authorization = Authorization()
        resource_name = 'process_payment'

    def dispatch(self, request_type, request, **kwargs):
        print("dmxndshdk")
        if request.method == 'POST':
            print("mxkmdlsd")
            try:
                data = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
                Credit_Card_Number = data['Credit_Card_Number']
                Card_Holder = data['Card_Holder']
                ExpirationDate = data['ExpirationDate']
                SecurityCode = data['SecurityCode']
                Amount = data['Amount']
                formated_ExpirationDate = datetime.strptime(ExpirationDate, "%Y-%m-%d %H:%M:%S")
                if formated_ExpirationDate > datetime.now():
                    if self.validate_card(Credit_Card_Number) == True:
                        if Amount < 20:
                            try:
                                self.CheapPaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                            except Exception as e:
                                status = "Error"
                                return self.create_response(request, {"status": status, "reason": str(e), "status_code": 500})
                        elif 21<Amount<500:
                            try:
                                try:
                                    self.ExpensivePaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                                except Exception as e:
                                    self.CheapPaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                            except Exception as e:
                                status = "Error"
                                return self.create_response(request, {"status": status, "reason": str(e), "status_code": 500})
                        else:
                            try:
                                self.PremiumPaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                            except Exception as e:
                                try:
                                    self.PremiumPaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                                except Exception as e:
                                    try:
                                        self.PremiumPaymentGateway(Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount)
                                    except Exception as e:
                                        status = "Error"
                                        return self.create_response(request, {"status": status, "reason": str(e), "status_code": 500})
                        status = "success"
                        reason = "details stored"
                        return self.create_response(request, {"status": status, "reason": reason, "status_code": 200})
                    else:
                        status = "Error"
                        reason = "invalid Credit Card Number"
                        return self.create_response(request, {"status": status, "reason": reason, "status_code": 400})
                else:
                    status = "Error"
                    reason = "Credit_Card expired"
                    return self.create_response(request, {"status": status, "reason": reason, "status_code": 400})
            except Exception as e:
                print(e)
                status = "Error"
                reason = "failed to add data"
                return self.create_response(request, {"status": status, "reason": reason, "status_code": 500})
    def PremiumPaymentGateway(self, Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount):
        # PremiumPaymentGateway code
        payment_obj = payment_details(Credit_Card_Number=Credit_Card_Number, Card_Holder=Card_Holder,
                                      ExpirationDate=ExpirationDate, SecurityCode=SecurityCode,
                                      Amount=Amount)
        payment_obj.save()

    def ExpensivePaymentGateway(self, Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount):
        # ExpensivePaymentGateway code
        payment_obj = payment_details(Credit_Card_Number=Credit_Card_Number, Card_Holder=Card_Holder,
                                      ExpirationDate=ExpirationDate, SecurityCode=SecurityCode,
                                      Amount=Amount)
        payment_obj.save()

    def CheapPaymentGateway(self, Credit_Card_Number, Card_Holder, ExpirationDate, SecurityCode, Amount):
        # CheapPaymentGateway code
        payment_obj = payment_details(Credit_Card_Number=Credit_Card_Number, Card_Holder=Card_Holder,
                                      ExpirationDate=ExpirationDate, SecurityCode=SecurityCode,
                                      Amount=Amount)
        payment_obj.save()

    def validate_card(self, input):
        digits = [int(c) for c in input if c.isdigit()]
        checksum = digits.pop()
        digits.reverse()
        doubled = [2 * d for d in digits[0::2]]
        total = sum(d - 9 if d > 9 else d for d in doubled) + sum(digits[1::2])
        return (total * 9) % 10 == checksum
