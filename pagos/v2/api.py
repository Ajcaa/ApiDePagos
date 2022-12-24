from django.shortcuts import get_object_or_404
from pagos.models import Payment_user, Services, Expired_payments
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .serializers import PaymentUserSerializer,ServicesSerializer,ExpiredPaymentsSerializer
from .pagination import StandardResultsSetPagination



class ServicesViewSet(viewsets.ModelViewSet):

    queryset = Services.objects.all()
    pagination_class = StandardResultsSetPagination
    throttle_scope = 'others'

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        return ServicesSerializer

    def retrieve(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServicesSerializer(service)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = ServicesSerializer(data=request.data, many = True)
        else:
            serializer = ServicesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServicesSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServicesSerializer(service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        service.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class PaymentUserViewSet(viewsets.ModelViewSet):

    queryset = Payment_user.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['PaymentDate', 'ExpirationDate']
    throttle_scope = 'pagos'

    def get_permissions(self):
        permission_classes = []

        if self.action == 'create' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        return PaymentUserSerializer

    def retrieve(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = PaymentUserSerializer(data=request.data, many = True)
        else:
            serializer = PaymentUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()


            if isinstance(request.data, list):
                lista = []
                for i in range(len(request.data)):
                    if request.data[i]["ExpirationDate"] < serializer.data[i]["PaymentDate"]:
                        lista.append({
                            "Payment_user_id": serializer.data[i]["Id"],
                            "Penalty_fee_amount": 20.00
                            })
                print(lista)
                expired_serial=ExpiredPaymentsSerializer(data=lista, many=True)

                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)
            else:
                if request.data["ExpirationDate"] < serializer.data["PaymentDate"]:
                    expired_serial=ExpiredPaymentsSerializer(data={
                        "Payment_user_id": serializer.data["Id"],
                        "Penalty_fee_amount": 20.00
                        })
                        
                    if expired_serial.is_valid():
                        ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment, data=request.data)

        if serializer.is_valid():
            serializer.save()

            if request.data["ExpirationDate"] < serializer.data["PaymentDate"]:
                expired_serial=ExpiredPaymentsSerializer(data={                   
                    "Payment_user_id ": serializer.data["id"],
                    "Penalty_fee_amount": 20.00
                    })
                    
                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        serializer = PaymentUserSerializer(payment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            if request.data["ExpirationDate"] < serializer.data["PaymentDate"]:
                expired_serial=ExpiredPaymentsSerializer(data={
                    "Payment_user_id": serializer.data["Id"],
                    "Penalty_fee_amount": 20.00
                    })
                    
                if expired_serial.is_valid():
                    ExpiredPaymentsViewSet.create(ExpiredPaymentsViewSet,request=expired_serial)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk)
        payment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class ExpiredPaymentsViewSet(viewsets.ModelViewSet):

    queryset = Expired_payments.objects.all()
    pagination_class = StandardResultsSetPagination
    throttle_scope = 'others'

    def get_permissions(self):
        permission_classes = []

        if self.action == 'create' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'retrieve':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        return ExpiredPaymentsSerializer

    def retrieve(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired)

        return Response(serializer.data)

    def create(self, request):

        if isinstance(request.data, list):
            serializer = ExpiredPaymentsSerializer(data=request.data, many = True)
        else:
            serializer = ExpiredPaymentsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        serializer = ExpiredPaymentsSerializer(expired, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        expired = get_object_or_404(self.queryset, pk=pk)
        expired.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)