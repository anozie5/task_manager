from django.shortcuts import render
from siteApi.models import *
from siteApi.serializers import *
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
#user creation
class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreationSerializer

    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    
#user login
class LoginUser(TokenObtainPairView):
    serializer_class = LoginSerializer

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'username': user.username,
            'email': user.email,
        }

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        }, status = status.HTTP_200_OK)


# views for the actual job
#for job
class JobView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        new_job = JobSerializer(data=request.data)
        if new_job.is_valid():
            new_job.save(owner=request.user)
            return Response(new_job.data, status=status.HTTP_201_CREATED)
        return Response(new_job.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, pk, user):
        return get_object_or_404(Job, pk=pk, owner=user)
    
    def get(self, request, pk=None):
        if pk is None:
            jobs = Job.objects.filter(owner=request.user)
            all_jobs = JobSerializer(jobs, many=True)
            return Response(all_jobs.data, status=status.HTTP_200_OK)        
        job = self.get_object(pk, request.user)
        job_data = JobSerializer(job)
        return Response(job_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        job = self.get_object(pk, request.user)
        job_update = JobSerializer(job, data=request.data, partial=False)
        if job_update.is_valid():
            job_update.save()
            return Response(job_update.data, status=status.HTTP_200_OK)
        return Response(job_update.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        job = self.get_object(pk, request.user)
        job_patch = JobSerializer(job, data=request.data, partial=True)
        if job_patch.is_valid():
            job_patch.save()
            return Response(job_patch.data, status=status.HTTP_200_OK)
        return Response(job_patch.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is None:
            jobs = Job.objects.filter(owner=request.user)
            jobs.delete()
            return Response({"message": "All jobs deleted"}, status=status.HTTP_200_OK)        
        job = self.get_object(pk, request.user)
        job.delete()
        return Response({"message": "Job deleted"}, status=status.HTTP_200_OK)



#for pay
class PayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_pay = PaySerializer(data=request.data)
        if new_pay.is_valid():
            new_pay.save(client_name__owner=request.user)
            return Response(new_pay.data, status=status.HTTP_201_CREATED)
        return Response(new_pay.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk, user):
        return get_object_or_404(Pay, pk=pk, client_name__owner=user)

    def get(self, request, pk=None):
        if pk is None:
            pays = Pay.objects.filter(client_name__owner=request.user)
            all_pays = PaySerializer(pays, many=True)
            return Response(all_pays.data, status=status.HTTP_200_OK)        
        pay = self.get_object(pk, request.user)
        pay_data = PaySerializer(pay)
        return Response(pay_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        pay = self.get_object(pk, request.user)
        pay_update = PaySerializer(pay, data=request.data, partial=False)
        if pay_update.is_valid():
            pay_update.save()
            return Response(pay_update.data, status=status.HTTP_200_OK)
        return Response(pay_update.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        pay = self.get_object(pk, request.user)
        pay_patch = PaySerializer(pay, data=request.data, partial=True)
        if pay_patch.is_valid():
            pay_patch.save()
            return Response(pay_patch.data, status=status.HTTP_200_OK)
        return Response(pay_patch.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is None:
            pays = Pay.objects.filter(client_name__owner=request.user)
            pays.delete()
            return Response({"message": "All pays deleted"}, status=status.HTTP_200_OK)        
        pay = self.get_object(pk, request.user)
        pay.delete()
        return Response({"message": "Pay deleted"}, status=status.HTTP_200_OK)