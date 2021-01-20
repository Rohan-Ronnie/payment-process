from django.db import models


class payment_details(models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    Credit_Card_Number = models.CharField(max_length=200, null=False, blank=False)
    Card_Holder = models.CharField(max_length=200, null=False, blank=False)
    ExpirationDate = models.DateTimeField()
    SecurityCode = models.CharField(max_length=200, null=False, blank=False)
    Amount = models.IntegerField()

    class Meta:
        app_label = 'payment'