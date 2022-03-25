from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompanySerializers, TransactionSerializers
from .models import Company, Transaction
from rest_framework import status
from django.http import Http404, JsonResponse
from django.db.models import Sum, Count


class Company_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        company = Company.objects.all()
        serializer = CompanySerializers(company, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompanySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Company_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializers(company)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializers(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Transaction_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        transaction = Transaction.objects.all()
        serializer = TransactionSerializers(transaction, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Transaction_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializers(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializers(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Summary_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        try:
            transactions = Transaction.objects.all()
            count_transactions = transactions.values('company_id').annotate(count=Count('id')).values('company_id', 'count').order_by('company_id')
            max_company = Company.objects.get(id=count_transactions.latest('count')['company_id'])
            min_company = Company.objects.get(id=count_transactions.earliest('count')['company_id'])
            payment_transactions = transactions.values('final_payment').annotate(sum=Sum('price')).values('final_payment', 'sum').order_by('final_payment')
            total_true = payment_transactions.filter(final_payment=True).latest('sum')['sum']
            total_false = payment_transactions.filter(final_payment=False).latest('sum')['sum']
            rejections = transactions.filter(final_payment=False).values('company_id').annotate(count=Count('id')).values('company_id', 'count').order_by('company_id')
            max_rejections = Company.objects.get(id=rejections.latest('count')['company_id'])
            return JsonResponse({'Empresa con más ventas':max_company.name+', con '+str(count_transactions.latest('count')['count'])+' ventas','Empresa con menos ventas':min_company.name+', con '+str(count_transactions.earliest('count')['count'])+' ventas',
                                 'Precio total de las transacciones que SÍ se cobraron':str(total_true),'Precio total de las transacciones que NO se cobraron':str(total_false),
                                 'La empresa con más rechazos de ventas es ':max_rejections.name+', con '+str(rejections.latest('count')['count'])+' rechazos.'})
        except Transaction.DoesNotExist:
            return JsonResponse({'Error': 'No hay datos de transacciones en la base de datos.' , 'status':404})
        except Company.DoesNotExist:
            return JsonResponse({'Error': 'No hay datos de compañias en la base de datos.' , 'status':404})

class Company_Summary_APIView(APIView):
    def get(self, request, pk, format=None):
        try:
            company = Company.objects.get(id=pk)
            transactions = Transaction.objects.all().filter(company_id=pk).values('created_on__date').annotate(count=Count('id')).values('created_on__date','count').order_by('created_on__date')
            total_true=Transaction.objects.all().filter(company_id=pk,final_payment=True).count()
            total_false=Transaction.objects.all().filter(company_id=pk,final_payment=False).count()
            return JsonResponse({'Empresa': company.name, 'Total de transacciones que SÍ se cobraron': str(total_true),
                             'Total de transacciones que NO se cobraron': str(total_false),
                             'Día que se registraron más transacciones': str(transactions.latest('count')['created_on__date'])+' con '+str(transactions.latest('count')['count'])+' transacciones'})
        except Transaction.DoesNotExist:
            return JsonResponse({'Error': 'No hay datos de transacciones en la base de datos.', 'status': 404})
        except Company.DoesNotExist:
            return JsonResponse({'Error': 'No hay datos de la compañia en la base de datos.', 'status': 404})