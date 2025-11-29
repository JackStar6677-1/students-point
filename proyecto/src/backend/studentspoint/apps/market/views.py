"""Views SIMPLES para marketplace - igual que reportes"""

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from studentspoint.apps.accounts.permissions import IsModerator
from rest_framework.permissions import IsAuthenticated
from .models import Producto, CategoriaProducto, ProductoReporte
from .serializers import ProductoReporteSerializer


class ProductoViewSet(viewsets.ViewSet):
    """ViewSet simple para productos con soporte de imágenes"""
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def list(self, request):
        """Listar productos"""
        productos = Producto.objects.filter(estado='publicado').order_by('-created_at')[:100]
        
        data = [{
            'id': p.id,
            'descripcion': p.descripcion or p.titulo,
            'url': p.url_principal,
            'precio': str(p.precio) if p.precio else None,
            'precio_estudiante': str(p.precio_student_point) if p.precio_student_point else None,
            'fecha': p.created_at.strftime('%d/%m/%Y'),
            'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None
        } for p in productos]
        
        return Response(data)
    
    def create(self, request):
        """Crear producto con imagen opcional"""
        if not request.user.is_authenticated:
            return Response({'error': 'Login requerido'}, status=401)
        
        descripcion = request.data.get('descripcion', '').strip()
        url = request.data.get('url', '').strip()
        
        if not descripcion or not url:
            return Response({'error': 'Faltan datos'}, status=400)
        
        # Categoría por defecto
        categoria, _ = CategoriaProducto.objects.get_or_create(
            nombre='General',
            defaults={'activa': True}
        )
        
        # Crear producto
        producto = Producto.objects.create(
            titulo=descripcion[:100],
            descripcion=descripcion,
            url_principal=url,
            precio=request.data.get('precio'),
            precio_student_point=request.data.get('precio_estudiante'),
            vendedor=request.user,
            categoria=categoria,
            estado='publicado',
            publicado_at=timezone.now(),
            moneda='CLP',
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        # Agregar imagen si existe
        imagen = request.FILES.get('imagen')
        if imagen:
            producto.imagen = imagen
            producto.save()
        
        return Response({
            'id': producto.id,
            'success': True,
            'imagen': request.build_absolute_uri(producto.imagen.url) if producto.imagen else None
        }, status=201)
    
    def destroy(self, request, pk=None):
        """Eliminar un producto y actualizar reportes relacionados. Solo para moderadores/admins."""
        # Verificar permisos de moderador/admin
        if not IsModerator().has_permission(request, self):
            return Response(
                {'error': 'No tienes permisos para eliminar productos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        producto = get_object_or_404(Producto, pk=pk)
        
        # Actualizar todos los reportes relacionados a "producto_eliminado"
        ProductoReporte.objects.filter(producto=producto).update(
            estado=ProductoReporte.Estado.PRODUCTO_ELIMINADO
        )
        
        # Eliminar el producto
        producto.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductoReporteView(generics.CreateAPIView):
    """Permite a usuarios reportar productos inapropiados."""
    
    serializer_class = ProductoReporteSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Crear reporte con manejo de errores mejorado"""
        try:
            producto = get_object_or_404(Producto, pk=self.kwargs["pk"])
            
            # Validar datos
            tipo = request.data.get('tipo')
            descripcion = request.data.get('descripcion', '')
            
            if not tipo:
                return Response(
                    {'error': 'Debes especificar el tipo de reporte'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el método reportar del modelo (maneja duplicados automáticamente)
            reporte = producto.reportar(request.user, tipo, descripcion)
            
            # Serializar el reporte creado/actualizado
            serializer = self.get_serializer(reporte)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al crear el reporte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductoReportesListView(generics.ListAPIView):
    """Lista reportes de un producto específico."""
    
    permission_classes = [IsModerator]
    serializer_class = ProductoReporteSerializer
    
    def get_queryset(self):
        producto = get_object_or_404(Producto, pk=self.kwargs["pk"])
        qs = ProductoReporte.objects.filter(producto=producto).order_by("-created_at")
        estado = self.request.query_params.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class ProductoReporteUpdateView(generics.UpdateAPIView):
    """Permite a moderadores y administradores actualizar el estado de un reporte."""
    permission_classes = [IsModerator]
    serializer_class = ProductoReporteSerializer

    def get_queryset(self):
        return ProductoReporte.objects.all()


class TodosProductoReportesListView(generics.ListAPIView):
    """Lista TODOS los reportes de productos - Solo para administradores."""
    
    permission_classes = [IsModerator]
    serializer_class = ProductoReporteSerializer
    
    def get_queryset(self):
        """Obtener todos los reportes con información del producto"""
        qs = ProductoReporte.objects.select_related(
            'producto', 'producto__vendedor', 'reportador'
        ).order_by("-created_at")
        
        # Filtros opcionales
        estado = self.request.query_params.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        
        tipo = self.request.query_params.get("tipo")
        if tipo:
            qs = qs.filter(tipo=tipo)
        
        return qs
