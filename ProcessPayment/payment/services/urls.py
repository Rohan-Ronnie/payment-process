from django.conf.urls import include, url

from tastypie.api import Api
from payment.services.payment_services import process_paymentResource
v1_auto_mail_send_api = Api(api_name='v1')
v1_auto_mail_send_api.register(process_paymentResource())
urlpatterns = [
    url(r'^', include(v1_auto_mail_send_api.urls))
]