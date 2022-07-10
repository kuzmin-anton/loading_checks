from rest_framework import serializers

from .models import Check


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['check_number', 'check_issuance_time',
                  'total', 'customer_id', 'pos_id']


class PurchoseSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=20)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                {"end_date": "Начальная дата и время должны быть меньше конечной."})
        return data


class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['total', 'customer_id']
