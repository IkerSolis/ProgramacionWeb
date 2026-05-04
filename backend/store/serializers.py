from rest_framework import serializers
from .models import Product, KeyCode, Sale, User
from django.contrib.auth.hashers import make_password

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class KeyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyCode
        fields = ['id', 'product', 'is_used', 'price', 'platform', 'region', 'created_at']

class KeyCodePrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyCode
        fields = ['id', 'product', 'key', 'is_used', 'price', 'platform', 'region']

class SaleSerializer(serializers.ModelSerializer):
    key_code = KeyCodePrivateSerializer(read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'password']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)
