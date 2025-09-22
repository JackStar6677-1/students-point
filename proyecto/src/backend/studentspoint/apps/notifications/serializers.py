"""Serializers for push notification subscriptions."""

from rest_framework import serializers
from .models import PushSub, Notificacion


class PushSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSub
        fields = ["endpoint", "p256dh", "auth"]

    def create(self, validated_data):
        user = self.context["request"].user
        sub, _ = PushSub.objects.update_or_create(
            usuario=user,
            endpoint=validated_data["endpoint"],
            defaults={
                "p256dh": validated_data["p256dh"],
                "auth": validated_data["auth"],
                "activo": True,
            },
        )
        return sub


class NotificationStatusSerializer(serializers.Serializer):
    """Serializer for notification status responses."""

    status = serializers.CharField()


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    
    class Meta:
        model = Notificacion
        fields = [
            'id', 'titulo', 'mensaje', 'tipo', 'leida', 
            'created_at', 'data_extra'
        ]
        read_only_fields = ['id', 'created_at']
