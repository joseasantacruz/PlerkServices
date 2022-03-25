from django.db import models

class Company(models.Model):
    StatusType=(('activa',('activa')),('inactiva',('inactiva')))

    created_on = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Creado el')
    last_updated_on = models.DateTimeField(auto_now=True,
                                           verbose_name='Creado el')
    name = models.CharField(max_length=255, default="DESCONOCIDO",null=False)
    status = models.CharField(choices=StatusType,
                                     max_length=100,
                                     null=False)
class Transaction(models.Model):
    StatusType=(('closed',('closed')),('reversed',('reversed')),('pending',('pending')))

    created_on = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Creado el')
    last_updated_on = models.DateTimeField(auto_now=True,
                                           verbose_name='Creado el')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=False
    )
    status_transaction = models.CharField(
        choices=StatusType,
        max_length=100,
        null=False)
    status_approved = models.BooleanField(
        null=False)
    final_payment = models.BooleanField(
        null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            old_transaction = ''
            if self.status_transaction == 'closed' and self.status_approved:
                self.final_payment = True
            else:
                self.final_payment = False
        else:
            old_transaction = Transaction.objects.get(id=self.id)
        super().save(*args, **kwargs)
        if old_transaction != '' and self.final_payment == old_transaction.final_payment:
            if self.status_transaction == 'closed' and self.status_approved:
                self.final_payment = True
            else:
                self.final_payment = False
            self.save()