from rest_framework import serializers
from .models import LatexRenderCache

class LatexRenderCacheSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LatexRenderCache
        fields = ['id', 'expression', 'svg']