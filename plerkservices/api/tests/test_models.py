from django.test import TestCase
from api.models import Company,Transaction


class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='Plerk', status='activa')

    def test_name(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
        self.assertEquals(company.name, 'Plerk')

    def test_status(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')
        self.assertEquals(company.status, 'activa')

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company =Company.objects.create(name='Plerk', status='activa')
        Transaction.objects.create(company_id=company, price=100, status_transaction='closed', status_approved=True)

    def test_price(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')
        self.assertEquals(transaction.price, 100)

    def test_status_transaction(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('status_transaction').verbose_name
        self.assertEquals(field_label, 'status transaction')
        self.assertEquals(transaction.status_transaction, 'closed')
