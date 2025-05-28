from rest_framework import serializers
from .models import PanneResau, Device, Abonne

# Serializer لجهاز Device
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'ip_address', 'device_type']

# Serializer للمشترك Abonne (لو تحتاج ترجع بيانات عنه)
class AbonneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonne
        fields = ['id', 'nom', 'prenom', 'numtel', 'adresse', 'email']

# Serializer للحالة panne réseau
class PanneResauSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)  # لعرض بيانات الجهاز مع الحالة
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), source='device', write_only=True
    )  # لاستقبال الجهاز عن طريق id عند إنشاء panne

    class Meta:
        model = PanneResau
        fields = [
            'id',
            'device',
            'device_id',
            'description',
            'status',
            'date_reported',
            'date_updated',
            'date_resolved',
        ]
