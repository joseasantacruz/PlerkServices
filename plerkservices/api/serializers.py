from rest_framework import serializers
from api.models import Company, Transaction

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'status']

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'company_id', 'price','status_transaction','status_approved','final_payment','created_on']