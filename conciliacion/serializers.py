from rest_framework_json_api import serializers
from conciliacion.models import Balance

class BalanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Balance
        fields = ('id', 'Cuenta', 'Nombre', 'RFC')