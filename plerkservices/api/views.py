from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompanySerializers, TransactionSerializers
from .models import Company, Transaction
from rest_framework import status
from django.http import Http404, JsonResponse
from django.db.models import F, Func, Value, CharField, Count


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
        transaction = Transaction.objects.all()
        company = Company.objects.all()
        counts = []
        rejections=[]
        total_true=0
        total_false=0
        for i in range(company.count()):
            counts.append(0)
            rejections.append(0)
        for transact in transaction:
            counts[transact.company_id.id-1]=counts[transact.company_id.id-1]+1
            if transact.final_payment:
                total_true=total_true+transact.price
            else:
                total_false=total_false+transact.price
                rejections[transact.company_id.id-1]=rejections[transact.company_id.id-1]+1
        max=0
        i_max=0
        min=company.count()+1
        i_min=0
        max_rejections=0
        i_max_rejections=0
        for i in range(company.count()):
            if counts[i] > max:
                max = counts[i]
                i_max = i
            if counts[i] < min:
                min = counts[i]
                i_min = i
            if rejections[i] > max_rejections:
                max_rejections = rejections[i]
                i_max_rejections = i
        return JsonResponse({'Empresa con más ventas':company[i_max].name+', con '+str(max)+' ventas','Empresa con menos ventas':company[i_min].name+', con '+str(min)+' ventas',
                             'Precio total de las transacciones que SÍ se cobraron':str(total_true),'Precio total de las transacciones que NO se cobraron':str(total_false),
                             'La empresa con más rechazos de ventas es ':company[i_max_rejections].name+', con '+str(max_rejections)+' rechazos.'})

class Company_Summary_APIView(APIView):
    def get(self, request, pk, format=None):
        company = Company.objects.get(id=pk)
        #serializer = CompanySerializers(company)
        transactions = Transaction.objects.all().filter(company_id=pk).values('created_on__date').annotate(count=Count('id')).values('created_on__date','count').order_by('created_on__date')
        total_true=Transaction.objects.all().filter(company_id=pk,final_payment=True).count()
        total_false=Transaction.objects.all().filter(company_id=pk,final_payment=False).count()


        return JsonResponse({'Empresa': company.name, 'Total de transacciones que SÍ se cobraron': str(total_true),
                             'Total de transacciones que NO se cobraron': str(total_false),
                             'Día que se registraron más transacciones': str(transactions.latest('count')['created_on__date'])+' con '+str(transactions.latest('count')['count'])+' transacciones'})

