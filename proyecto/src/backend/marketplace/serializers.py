from rest_framework import serializers
from .models import Category, Product, ProductImage, Transaction, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'created_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'condition', 'status', 'location', 'views', 'created_at', 'category', 'seller', 'primary_image']
    
    def get_primary_image(self, obj):
        primary_img = obj.product_images.filter(is_primary=True).first()
        if primary_img:
            return primary_img.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'condition', 'status', 'location', 'contact_info', 'images', 'views', 'created_at', 'updated_at', 'category', 'seller']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'condition', 'location', 'contact_info']
    
    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'product', 'buyer', 'seller', 'status', 'message', 'created_at', 'updated_at']

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['product', 'message']
    
    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        validated_data['seller'] = validated_data['product'].seller
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    reviewed_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'reviewer', 'reviewed_user', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['transaction', 'rating', 'comment']
    
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        validated_data['reviewed_user'] = validated_data['transaction'].seller
        return super().create(validated_data)
