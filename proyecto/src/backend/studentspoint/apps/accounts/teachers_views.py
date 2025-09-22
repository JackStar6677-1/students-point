"""Vistas para el directorio de profesores."""

from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class TeachersListView(generics.ListAPIView):
    """Lista todos los profesores y personal docente."""
    
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """Filtrar usuarios que son profesores o personal docente."""
        return User.objects.filter(
            role__in=[
                User.Roles.MODERATOR,
                User.Roles.DIRECTOR_CARRERA,
                User.Roles.ADMIN_GLOBAL
            ],
            is_active=True
        ).select_related('campus')
    
    def list(self, request, *args, **kwargs):
        """Personalizar respuesta para incluir información adicional."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Agregar información adicional para cada profesor
        teachers_data = []
        for teacher in queryset:
            teacher_data = serializer.data[queryset.index(teacher)]
            teacher_data.update({
                'role_display': teacher.get_role_display(),
                'campus_name': teacher.campus.nombre if teacher.campus else 'No asignado',
                'is_available': True,  # Por defecto todos están disponibles
                'specialties': self._get_teacher_specialties(teacher),
                'contact_info': {
                    'email': teacher.email,
                    'phone': getattr(teacher, 'telefono', ''),
                    'linkedin': getattr(teacher, 'linkedin_url', ''),
                    'github': getattr(teacher, 'github_url', '')
                }
            })
            teachers_data.append(teacher_data)
        
        return Response({
            'count': len(teachers_data),
            'teachers': teachers_data
        })
    
    def _get_teacher_specialties(self, teacher):
        """Obtener especialidades del profesor basadas en su rol y carrera."""
        specialties = []
        
        if teacher.role == User.Roles.MODERATOR:
            specialties.extend(['Moderación', 'Comunidad'])
        elif teacher.role == User.Roles.DIRECTOR_CARRERA:
            specialties.extend(['Dirección Académica', 'Planificación'])
        elif teacher.role == User.Roles.ADMIN_GLOBAL:
            specialties.extend(['Administración', 'Sistemas'])
        
        # Agregar especialidades basadas en la carrera
        if teacher.career:
            specialties.append(teacher.career)
        
        return specialties


class TeacherDetailView(generics.RetrieveAPIView):
    """Detalle de un profesor específico."""
    
    serializer_class = UserSerializer
    queryset = User.objects.filter(
        role__in=[
            User.Roles.MODERATOR,
            User.Roles.DIRECTOR_CARRERA,
            User.Roles.ADMIN_GLOBAL
        ],
        is_active=True
    )
    
    def retrieve(self, request, *args, **kwargs):
        """Personalizar respuesta con información detallada del profesor."""
        teacher = self.get_object()
        serializer = self.get_serializer(teacher)
        
        teacher_data = serializer.data
        teacher_data.update({
            'role_display': teacher.get_role_display(),
            'campus_name': teacher.campus.nombre if teacher.campus else 'No asignado',
            'specialties': self._get_teacher_specialties(teacher),
            'contact_info': {
                'email': teacher.email,
                'phone': getattr(teacher, 'telefono', ''),
                'linkedin': getattr(teacher, 'linkedin_url', ''),
                'github': getattr(teacher, 'github_url', '')
            },
            'availability': {
                'is_available': True,
                'office_hours': 'Lunes a Viernes 9:00 - 17:00',
                'response_time': '24-48 horas'
            }
        })
        
        return Response(teacher_data)
    
    def _get_teacher_specialties(self, teacher):
        """Obtener especialidades del profesor."""
        specialties = []
        
        if teacher.role == User.Roles.MODERATOR:
            specialties.extend(['Moderación', 'Comunidad'])
        elif teacher.role == User.Roles.DIRECTOR_CARRERA:
            specialties.extend(['Dirección Académica', 'Planificación'])
        elif teacher.role == User.Roles.ADMIN_GLOBAL:
            specialties.extend(['Administración', 'Sistemas'])
        
        if teacher.career:
            specialties.append(teacher.career)
        
        return specialties

