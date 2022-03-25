from django.test import TestCase
from api.models import Company,Transaction
from api.serializers import CompanySerializers, TransactionSerializers


class CompanyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for num in range(10):
            Company.objects.create(name='Plerk %s' % (num+1), status='activa')

    def test_view_get_companies(self):
        companies = Company.objects.all()
        resp = self.client.get('/company')
        serializer = CompanySerializers(companies, many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(companies.count(), 10)
        self.assertEquals(serializer.data,resp.data)

    def test_view_get_company(self):
        company = Company.objects.get(id=5)
        resp = self.client.get('/company/5/')
        serializer = CompanySerializers(company)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(company.name, 'Plerk 3')
        self.assertEquals(serializer.data,resp.data)

    def test_view_delete_company(self):
        resp = self.client.delete('/company/5/')
        self.assertEqual(resp.status_code, 204)

class TransactionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company =Company.objects.create(name='Plerk', status='activa')
        for num in range(10):
            Transaction.objects.create(company_id=company, price=(100*num), status_transaction='closed', status_approved=True)

    def test_view_get_transactions(self):
        transactions = Transaction.objects.all()
        resp = self.client.get('/transaction')
        serializer = TransactionSerializers(transactions, many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(transactions.count(), 10)
        self.assertEquals(serializer.data, resp.data)

    def test_view_get_transaction(self):
        transaction = Transaction.objects.get(id=5)
        resp = self.client.get('/transaction/5/')
        serializer = TransactionSerializers(transaction)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(transaction.price, 300)
        self.assertEquals(serializer.data,resp.data)

    def test_view_delete_transaction(self):
        resp = self.client.delete('/transaction/5/')
        self.assertEqual(resp.status_code, 204)

    def test_view_summary(self):
        resp = self.client.get('/summary')
        self.assertEqual(resp.status_code, 200)

    def test_view_company_summary(self):
        resp = self.client.get('/company/3/summary')
        self.assertEqual(resp.status_code, 200)
