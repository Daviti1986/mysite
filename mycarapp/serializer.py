from rest_framework import serializers
from suggestapp.models import Suggest

class SuggestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Suggest
        fields = ['name', 'date']


