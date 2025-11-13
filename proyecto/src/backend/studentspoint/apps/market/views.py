"""Views para el sistema de compra/venta."""

from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import (
    CategoriaProducto, Producto, ProductoFavorito, 
    ProductoReporte, ProductoAnalytics
)
from .serializers import (
    CategoriaProductoSerializer, ProductoSerializer, ProductoCreateSerializer,
    ProductoFavoritoSerializer, ProductoReporteSerializer, 
    ProductoAnalyticsSerializer, ProductoListSerializer
)


class CategoriaProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para categorías de productos."""
    
    queryset = CategoriaProducto.objects.filter(activa=True)
    serializer_class = CategoriaProductoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductoViewSet(viewsets.ModelViewSet):
    """ViewSet para productos."""
    
    queryset = Producto.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra productos según el usuario y parámetros."""
        queryset = Producto.objects.select_related(
            'categoria', 'vendedor', 'campus'
        ).prefetch_related('favoritos')
        
        # Filtros básicos
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        campus = self.request.query_params.get('campus')
        if campus:
            try:
                queryset = queryset.filter(campus_id=int(campus))
            except (TypeError, ValueError):
                queryset = queryset.filter(campus__slug=campus)
        
        carrera = self.request.query_params.get('carrera')
        if carrera:
            queryset = queryset.filter(carrera__icontains=carrera)
        
        # Búsqueda
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) | 
                Q(descripcion__icontains=search)
            )
        
        # Solo productos activos por defecto
        if not estado:
            queryset = queryset.filter(estado=Producto.Estados.PUBLICADO)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción."""
        if self.action == 'create':
            return ProductoCreateSerializer
        elif self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    def perform_create(self, serializer):
        """Crea un nuevo producto."""
        serializer.save()
    
    def retrieve(self, request, *args, **kwargs):
        """Obtiene un producto y registra la visualización."""
        instance = self.get_object()
        
        # Incrementar visualizaciones
        instance.visualizaciones += 1
        instance.save()
        
        # Actualizar analytics
        try:
            analytics = instance.analytics
            analytics.actualizar_estadisticas()
        except ProductoAnalytics.DoesNotExist:
            ProductoAnalytics.objects.create(producto=instance)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Marcar/desmarcar producto como favorito",
        responses={200: {"description": "Estado del favorito actualizado"}}
    )
    @action(detail=True, methods=['post'])
    def toggle_favorito(self, request, pk=None):
        """Marca o desmarca un producto como favorito."""
        producto = self.get_object()
        usuario = request.user
        
        favorito, created = ProductoFavorito.objects.get_or_create(
            usuario=usuario,
            producto=producto
        )
        
        if not created:
            favorito.delete()
            es_favorito = False
        else:
            es_favorito = True
        
        return Response({
            'es_favorito': es_favorito,
            'total_favoritos': producto.favoritos.count()
        })
    
    @extend_schema(
        summary="Registrar click en enlace del producto",
        responses={200: {"description": "Click registrado"}}
    )
    @action(detail=True, methods=['post'])
    def registrar_click(self, request, pk=None):
        """Registra un click en el enlace del producto."""
        producto = self.get_object()
        producto.clicks_enlace += 1
        producto.save()
        
        # Actualizar analytics
        try:
            analytics = producto.analytics
            analytics.actualizar_estadisticas()
        except ProductoAnalytics.DoesNotExist:
            ProductoAnalytics.objects.create(producto=producto)
        
        return Response({'clicks_total': producto.clicks_enlace})
    
    @extend_schema(
        summary="Obtener productos favoritos del usuario",
        responses={200: ProductoFavoritoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def mis_favoritos(self, request):
        """Obtiene los productos favoritos del usuario."""
        favoritos = ProductoFavorito.objects.filter(
            usuario=request.user
        ).select_related('producto__categoria', 'producto__vendedor', 'producto__campus')
        
        serializer = ProductoFavoritoSerializer(favoritos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(
        summary="Obtener productos del usuario",
        responses={200: ProductoListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def mis_productos(self, request):
        """Obtiene los productos del usuario."""
        productos = Producto.objects.filter(
            vendedor=request.user
        ).select_related('categoria', 'campus').prefetch_related('favoritos')
        
        serializer = ProductoListSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(
        summary="Obtener analytics de un producto",
        responses={200: ProductoAnalyticsSerializer}
    )
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Obtiene analytics de un producto."""
        producto = self.get_object()
        
        # Verificar permisos (solo el vendedor puede ver analytics)
        if producto.vendedor != request.user and not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para ver estos analytics'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            analytics = producto.analytics
            analytics.actualizar_estadisticas()
        except ProductoAnalytics.DoesNotExist:
            analytics = ProductoAnalytics.objects.create(producto=producto)
        
        serializer = ProductoAnalyticsSerializer(analytics)
        return Response(serializer.data)


class ProductoReporteViewSet(viewsets.ModelViewSet):
    """ViewSet para reportes de productos."""
    
    queryset = ProductoReporte.objects.all()
    serializer_class = ProductoReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra reportes según el usuario."""
        queryset = ProductoReporte.objects.select_related(
            'producto', 'reportador'
        )
        
        # Solo staff puede ver todos los reportes
        if not self.request.user.is_staff:
            queryset = queryset.filter(reportador=self.request.user)
        
        return queryset.order_by('-created_at')
    
    @extend_schema(
        summary="Reportar un producto",
        request=ProductoReporteSerializer,
        responses={201: ProductoReporteSerializer}
    )
    def create(self, request, *args, **kwargs):
        """Crea un nuevo reporte."""
        producto_id = request.data.get('producto')
        if not producto_id:
            return Response(
                {'error': 'ID del producto es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        producto = get_object_or_404(Producto, id=producto_id)
        
        # Verificar que no haya reportado antes
        if ProductoReporte.objects.filter(
            producto=producto, 
            reportador=request.user
        ).exists():
            return Response(
                {'error': 'Ya has reportado este producto'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Actualizar analytics del producto
        try:
            analytics = producto.analytics
            analytics.actualizar_estadisticas()
        except ProductoAnalytics.DoesNotExist:
            ProductoAnalytics.objects.create(producto=producto)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductoAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para analytics de productos."""
    
    queryset = ProductoAnalytics.objects.all()
    serializer_class = ProductoAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra analytics según permisos del usuario."""
        queryset = ProductoAnalytics.objects.select_related('producto__vendedor')
        
        # Solo staff puede ver todos los analytics
        if not self.request.user.is_staff:
            queryset = queryset.filter(producto__vendedor=self.request.user)
        
        return queryset

