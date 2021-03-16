from rest_framework import serializers
from exercise_1.models import Numbers


class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = ['text', 'number', 'found', 'type']
