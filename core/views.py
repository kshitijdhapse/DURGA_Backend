from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound


# DRF imports
from rest_framework_simplejwt.tokens import AccessToken , RefreshToken
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
class FoodDetail(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        categorical = {}
        
        Food = FoodItem.objects.filter(hide = False)
        for item in Food:
            if item.category not in categorical:
                categorical[item.category] = []
            categorical[item.category].append({
                'name': item.name,
                'desc': item.description,
                'price': str(item.price),
                'topping': item.topping,
                'topping_price': str(item.topping_price),
                'image': str(item.image),
            })
        return Response(categorical)


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    
class BranchMenuAPI(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        categorical = {}
        branch = kwargs.get('branch')
        # branch_instance = get_object_or_404(Branch, branch=branch)
        Food = BranchMenu.objects.filter(branch=branch)
        for BranchItem in Food:
            item=BranchItem.foodname
            if item.category not in categorical:
                categorical[item.category] = []
            categorical[item.category].append({
                'name': item.name,
                'desc': item.description,
                'price': str(item.price),
                'topping': item.topping,
                'topping_price': str(item.topping_price),
                'image': str(item.image),
            })
        return Response(categorical)

class BranchSelectAPI(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        Branches=Branch.objects.all()
        serialized = BranchSerializer(Branches,many=True)
        return Response(serialized.data)

class OtherBranchMenuAPI(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        categorical = {}
        branch = kwargs.get('branch')
        # branch_instance = get_object_or_404(Branch, branch=branch)
        Food = set(BranchMenu.objects.filter(branch=branch).values_list('foodname', flat=True))
        AllFood = FoodItem.objects.filter(hide=False)
        result = [item for item in AllFood if item.id not in Food]
        print(result)
        for item in result:
            # item=BranchItem.name
            if item.category not in categorical:
                categorical[item.category] = [] 
            categorical[item.category].append({
                'name': item.name,
                'desc': item.description,
                'price': str(item.price),
                'topping': item.topping,
                'topping_price': str(item.topping_price),
                'image': str(item.image),
            })
        return Response(categorical)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            tokens = {
                'access': str(AccessToken.for_user(user)),
                'refresh': str(RefreshToken.for_user(user)),
            }
            user_data = UserSerializer(user).data
            user_data.update(tokens)  # Append the tokens
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
        
class AddToBranchMenu(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        branch = request.user.branch  # Get the user's branch from the JWT payload
        items = request.data.get('items', [])

        if not items:
            return Response({"detail": "No items selected."}, status=400)

        for item_name in items:
            food_item = get_object_or_404(FoodItem, name=item_name)
            BranchMenu.objects.create(
                branch=branch,
                foodname=food_item,
                price=food_item.price
            )
        return Response({"detail": "Items added successfully!"}, status=200)

class UpdateBranchMenuPriceAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def post(self, request, *args, **kwargs):
        branch_menu_id = kwargs.get('id')
        new_price = request.data.get('price')

        if new_price is None:
            return Response({"detail": "Price is required."}, status=400)

        branch_menu_item = get_object_or_404(BranchMenu, id=branch_menu_id, branch=request.user.branch)
        branch_menu_item.price = new_price
        branch_menu_item.save()

        return Response({"detail": "Price updated successfully!"}, status=200)

