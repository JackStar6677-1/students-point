from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, Transaction, Review
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer, 
    ProductCreateSerializer, TransactionSerializer, TransactionCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(status='available').select_related('category', 'seller')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'status', 'seller']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category', 'seller')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductDetailSerializer
    
    def perform_update(self, serializer):
        # Solo el vendedor puede actualizar su producto
        if serializer.instance.seller != self.request.user:
            raise PermissionError("No tienes permisos para actualizar este producto")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Solo el vendedor puede eliminar su producto
        if instance.seller != self.request.user:
            raise PermissionError("No tienes permisos para eliminar este producto")
        instance.delete()

class UserProductsAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related('category')

class TransactionListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).select_related('product', 'buyer', 'seller')
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class TransactionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.select_related('product', 'buyer', 'seller')
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        )

class ReviewListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Review.objects.filter(reviewed_user_id=user_id).select_related('reviewer', 'reviewed_user')
        return Review.objects.all().select_related('reviewer', 'reviewed_user')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_product_views(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.views += 1
        product.save()
        return Response({'views': product.views})
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_products(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    condition = request.GET.get('condition')
    
    queryset = Product.objects.filter(status='available')
    
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    if condition:
        queryset = queryset.filter(condition=condition)
    
    serializer = ProductListSerializer(queryset, many=True)
    return Response(serializer.data)