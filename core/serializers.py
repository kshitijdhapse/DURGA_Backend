from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)  # Adjust based on your Branch model

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'branch']

    def create(self, validated_data):
        password = validated_data.pop('password')
        branch = validated_data.pop('branch', None)
        user = User(**validated_data)
        if branch:
            user.branch = branch
        user.set_password(password)
        user.save()
        return user
    
class FoodItemSerializer(ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name','desc','price','topping','toppingprice','image']
        # exclude = ['answer','paidHint','keywords']
        
class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch','owner','contact']
                
class BranchMenuSerializer(ModelSerializer):
    class Meta:
        model = BranchMenu
        fields = ['branch','foodname','price']
        read_only_fields = ['branch','foodname']