from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic Validation
        if not email or not password:
            messages.error(request, 'All fields are required')
            return redirect('accounts:signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists')
            return redirect('accounts:signup')
        
        # create user 
        User.objects.create_user(email=email, password=password)
        messages.success(request, 'Account Created Successfully')
        return redirect('accounts:login')
    
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user) # create session
            return redirect('accounts:dashboard')
        
        messages.error(request, 'Invalid mail or password')

    return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
def dashboard_view(request):
    return render(request,'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')



class SignupAPIView(APIView):
    def post(Self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message' : 'User Created Successfully'},
            status=status.HTTP_201_CREATED
        )
    

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)


        return Response({
            'access' : str(refresh.access_token),
            'refresh' : str(refresh),
        })   
    

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'email' : request.user.email,
            'role' : request.user.role
        })
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = refresh_token(refresh_token)
            token.blacklist()

            return Response(
                {'message' : 'Logout Successfully'},
                status=status.HTTP_205_RESET_CONTENT
                )
        
        except:
            return Response(
                {'error' : 'Invalid or expried token'},
                status=status.HTTP_400_BAD_REQUEST
                )


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            'message' : 'Welcome Admin'
        })
    
class ManagerAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        return Response({
            'message' : 'Manager access granted'
        })