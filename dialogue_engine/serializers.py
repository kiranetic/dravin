from rest_framework import serializers
from .models import Query

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id', 'text', 'label', 'created_at']
        read_only_fields = ['label', 'created_at']  # Client can't set these
