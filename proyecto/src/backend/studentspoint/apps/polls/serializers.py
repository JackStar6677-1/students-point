"""Serializadores mejorados para el sistema completo de encuestas."""

import csv
import io
from rest_framework import serializers
from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field

from studentspoint.apps.campuses.models import Sede
from .models import Poll, PollOpcion, PollVoto, PollAnalytics


class PollOpcionSerializer(serializers.ModelSerializer):
    """Serializa opciones de encuesta con estadísticas."""
    
    votos = serializers.IntegerField(read_only=True)
    porcentaje = serializers.SerializerMethodField()
    
    class Meta:
        model = PollOpcion
        fields = ["id", "texto", "descripcion", "orden", "color", "votos", "porcentaje"]
        
    @extend_schema_field(serializers.FloatField())
    def get_porcentaje(self, obj) -> float:
        return obj.porcentaje_votos


class PollOpcionCreateSerializer(serializers.ModelSerializer):
    """Serializa opciones para creación de encuestas."""
    
    class Meta:
        model = PollOpcion
        fields = ["texto", "descripcion", "orden", "color"]


class PollListSerializer(serializers.ModelSerializer):
    """Serializa encuestas para listado con información básica."""
    
    creador_nombre = serializers.CharField(source="creador.name", read_only=True)
    total_votos = serializers.IntegerField(read_only=True)
    esta_activa = serializers.BooleanField(read_only=True)
    puede_votar = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = [
            "id", "titulo", "descripcion", "creador_nombre", "estado", 
            "inicia_at", "cierra_at", "total_votos", "esta_activa", 
            "puede_votar", "created_at"
        ]
        
    def get_puede_votar(self, obj) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.puede_votar(request.user)
        return False


class PollDetailSerializer(serializers.ModelSerializer):
    """Serializa encuesta completa con opciones y resultados."""
    
    opciones = serializers.SerializerMethodField()
    creador_nombre = serializers.CharField(source="creador.name", read_only=True)
    total_votos = serializers.IntegerField(read_only=True)
    esta_activa = serializers.BooleanField(read_only=True)
    puede_votar = serializers.SerializerMethodField()
    puede_ver_resultados = serializers.SerializerMethodField()
    sedes_nombres = serializers.StringRelatedField(source="sedes", many=True, read_only=True)
    analytics = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = [
            "id", "titulo", "descripcion", "creador_nombre", "multi", "anonima",
            "requiere_justificacion", "mostrar_resultados", "estado", "inicia_at", 
            "cierra_at", "sedes_nombres", "carreras", "opciones", "total_votos",
            "esta_activa", "puede_votar", "puede_ver_resultados", "analytics",
            "created_at", "updated_at"
        ]
    
    @extend_schema_field(PollOpcionSerializer(many=True))
    def get_opciones(self, obj):
        user = self.context.get("request").user
        opciones = obj.opciones.all()
        
        if obj.puede_ver_resultados(user):
            # Mostrar con estadísticas
            opciones_data = []
            for opcion in opciones:
                opciones_data.append({
                    "id": opcion.id,
                    "texto": opcion.texto,
                    "descripcion": opcion.descripcion,
                    "orden": opcion.orden,
                    "color": opcion.color,
                    "votos": opcion.total_votos,
                    "porcentaje": opcion.porcentaje_votos
                })
            return opciones_data
        else:
            # Solo mostrar opciones sin estadísticas
            return PollOpcionCreateSerializer(opciones, many=True).data
    
    def get_puede_votar(self, obj) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.puede_votar(request.user)
        return False
    
    def get_puede_ver_resultados(self, obj) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.puede_ver_resultados(request.user)
        return False
    
    @extend_schema_field(serializers.DictField())
    def get_analytics(self, obj):
        user = self.context.get("request").user
        if not obj.puede_ver_resultados(user):
            return None
            
        try:
            analytics = obj.analytics
            return {
                "total_participantes": analytics.total_participantes,
                "distribucion_sedes": analytics.distribucion_sedes,
                "distribucion_carreras": analytics.distribucion_carreras,
                "ultima_actualizacion": analytics.ultima_actualizacion
            }
        except PollAnalytics.DoesNotExist:
            return None


class PollCreateSerializer(serializers.ModelSerializer):
    """Serializa creación de encuestas con opciones."""
    
    opciones = PollOpcionCreateSerializer(many=True, write_only=True)
    sedes_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    
    class Meta:
        model = Poll
        fields = [
            "titulo", "descripcion", "multi", "anonima", "requiere_justificacion",
            "mostrar_resultados", "inicia_at", "cierra_at", "carreras", 
            "sedes_ids", "opciones"
        ]
    
    def validate_opciones(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Se requieren al menos 2 opciones")
        if len(value) > 10:
            raise serializers.ValidationError("Máximo 10 opciones permitidas")
        return value
    
    def validate(self, attrs):
        if attrs.get("cierra_at") and attrs.get("inicia_at"):
            if attrs["cierra_at"] <= attrs["inicia_at"]:
                raise serializers.ValidationError(
                    "La fecha de cierre debe ser posterior a la fecha de inicio"
                )
        return attrs
    
    def create(self, validated_data):
        opciones_data = validated_data.pop("opciones")
        sedes_ids = validated_data.pop("sedes_ids", [])
        
        # Asignar creador
        validated_data["creador"] = self.context["request"].user
        validated_data["estado"] = Poll.Estado.ACTIVA  # Activar automáticamente
        
        poll = Poll.objects.create(**validated_data)
        
        # Asignar sedes
        if sedes_ids:
            sedes = Sede.objects.filter(id__in=sedes_ids)
            poll.sedes.set(sedes)
        
        # Crear opciones
        for i, opcion_data in enumerate(opciones_data):
            opcion_data["orden"] = i
            PollOpcion.objects.create(poll=poll, **opcion_data)
        
        # Crear analytics
        PollAnalytics.objects.create(poll=poll)
        
        return poll


class PollUpdateSerializer(serializers.ModelSerializer):
    """Serializa actualización de encuestas (solo ciertos campos)."""
    
    class Meta:
        model = Poll
        fields = ["titulo", "descripcion", "estado", "cierra_at", "mostrar_resultados"]
    
    def validate(self, attrs):
        instance = self.instance
        
        # No permitir cambios si ya hay votos
        if instance.total_votos > 0:
            campos_bloqueados = ["titulo", "descripcion"]
            for campo in campos_bloqueados:
                if campo in attrs:
                    raise serializers.ValidationError(
                        f"No se puede modificar '{campo}' cuando ya existen votos"
                    )
        
        return attrs


class PollVoteSerializer(serializers.Serializer):
    """Serializa votación en encuestas."""
    
    opciones = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    justificacion = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        poll = self.context["poll"]
        user = self.context["request"].user
        opcion_ids = attrs["opciones"]
        
        # Verificar que la encuesta esté activa
        if not poll.esta_activa:
            raise serializers.ValidationError("La encuesta no está activa")
        
        # Verificar permisos para votar
        if not poll.puede_votar(user):
            raise serializers.ValidationError("No tienes permisos para votar en esta encuesta")
        
        # Validar opciones
        opciones = PollOpcion.objects.filter(poll=poll, id__in=opcion_ids)
        if opciones.count() != len(opcion_ids):
            raise serializers.ValidationError("Una o más opciones no son válidas")
        
        # Verificar si permite múltiples opciones
        if not poll.multi and len(opcion_ids) > 1:
            raise serializers.ValidationError("Esta encuesta solo permite una opción")
        
        # Verificar votos existentes
        if PollVoto.objects.filter(poll=poll, usuario=user).exists():
            raise serializers.ValidationError("Ya has votado en esta encuesta")
        
        # Verificar justificación requerida
        if poll.requiere_justificacion and not attrs.get("justificacion"):
            raise serializers.ValidationError("Esta encuesta requiere justificación")
        
        attrs["_opciones_objs"] = list(opciones)
        return attrs
    
    def create(self, validated_data):
        poll = self.context["poll"]
        user = self.context["request"].user
        request = self.context["request"]
        justificacion = validated_data.get("justificacion", "")
        
        # Obtener IP y User-Agent para auditoría
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        
        # Crear votos
        for opcion in validated_data["_opciones_objs"]:
            PollVoto.objects.create(
                poll=poll,
                opcion=opcion,
                usuario=user,
                justificacion=justificacion,
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        return poll
    
    def get_client_ip(self, request):
        """Obtiene la IP del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PollExportSerializer(serializers.Serializer):
    """Serializa parámetros para exportación de resultados."""
    
    formato = serializers.ChoiceField(choices=["csv", "json"], default="csv")
    incluir_metadatos = serializers.BooleanField(default=True)
    incluir_justificaciones = serializers.BooleanField(default=False)
    
    def export_csv(self, poll):
        """Exporta resultados de encuesta a CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        headers = ["Opción", "Votos", "Porcentaje"]
        if self.validated_data.get("incluir_metadatos"):
            headers.extend(["Sede", "Carrera", "Fecha Voto"])
        if self.validated_data.get("incluir_justificaciones"):
            headers.append("Justificación")
        
        writer.writerow(headers)
        
        # Datos por opción
        for opcion in poll.opciones.all():
            votos = opcion.votos.select_related("usuario", "sede_voto")
            
            if not self.validated_data.get("incluir_metadatos"):
                # Solo totales por opción
                writer.writerow([
                    opcion.texto,
                    opcion.total_votos,
                    f"{opcion.porcentaje_votos}%"
                ])
            else:
                # Detalle por voto
                for voto in votos:
                    row = [
                        opcion.texto,
                        1,  # Un voto
                        "",  # Porcentaje se calcula al final
                        voto.sede_voto.nombre if voto.sede_voto else "Sin sede",
                        voto.carrera_voto or "Sin carrera",
                        voto.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    ]
                    if self.validated_data.get("incluir_justificaciones"):
                        row.append(voto.justificacion)
                    writer.writerow(row)
        
        return output.getvalue()


class PollAnalyticsSerializer(serializers.ModelSerializer):
    """Serializa analytics de encuestas."""
    
    class Meta:
        model = PollAnalytics
        fields = [
            "total_participantes", "distribucion_sedes", "distribucion_carreras",
            "ultima_actualizacion"
        ]


class SimpleStatusSerializer(serializers.Serializer):
    """Respuesta simple de estado."""
    
    status = serializers.CharField()
    message = serializers.CharField(required=False)