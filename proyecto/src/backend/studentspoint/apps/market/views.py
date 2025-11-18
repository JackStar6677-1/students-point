"""Views SIMPLES para marketplace - igual que reportes"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Producto, CategoriaProducto


class ProductoViewSet(viewsets.ViewSet):
    """ViewSet simple para productos"""
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        """Listar productos"""
        productos = Producto.objects.filter(estado='publicado').order_by('-created_at')[:100]
        
        data = [{
            'id': p.id,
            'descripcion': p.descripcion or p.titulo,
            'url': p.url_principal,
            'precio': str(p.precio) if p.precio else None,
            'precio_estudiante': str(p.precio_student_point) if p.precio_student_point else None,
            'fecha': p.created_at.strftime('%d/%m/%Y')
        } for p in productos]
        
        return Response(data)
    
    def create(self, request):
        """Crear producto"""
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
        
        return Response({'id': producto.id, 'success': True}, status=201)
