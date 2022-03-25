from django.test import TestCase
from api.models import Company,Transaction
from api.serializers import CompanySerializers, TransactionSerializers
from django.urls import reverse


class CompanyListViewTest(TestCase):
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