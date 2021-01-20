from django.conf.urls import include, url

urlpatterns = [

                       url(r'^service/', include('payment.services.urls')),

]