from rest_framework import serializers
from .models import ViolationHistory, UnsureViolationHistory

class ViolationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationHistory
        fields = ('id','description', 'image')

class UnsureViolationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnsureViolationHistory
        fields = ('id','description', 'image')