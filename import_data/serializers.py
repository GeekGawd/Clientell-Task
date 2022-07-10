from .models import *
from rest_framework import serializers
from django.db.models import Count


class OpportunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opportunity
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    number_of_opportunities = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_number_of_opportunities(self, instance):
        return instance.number_of_opportunities

class UserSerializer(serializers.ModelSerializer):
    opportunity_strictly_greater_than_100000 = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'opportunity_strictly_greater_than_100000']
    
    def get_opportunity_strictly_greater_than_100000(self, instance):
        return instance.opporutinty_gt_100000
    
    
    