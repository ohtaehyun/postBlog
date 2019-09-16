from rest_framework import serializers
from .models import troloCard, troloList


class cardSerializer(serializers.ModelSerializer):
    class Meta:
        model = troloCard
        fields = ('id',
                  'cardTitle', 'cardDescription', 'targetList')
