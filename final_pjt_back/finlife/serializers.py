from rest_framework import serializers
from .models import DepositProducts, DepositOptions , SavingProducts , SavingOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)

class DepositTotalSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True, source='depositoptions_set')  
    # `depositoptions_set`는 역참조 이름 (ForeignKey 기본값)
    class Meta:
        model = DepositProducts
        fields = '__all__'

class SavingTotalSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True, source='savingoptions_set')  
    # `depositoptions_set`는 역참조 이름 (ForeignKey 기본값)
    class Meta:
        model = SavingProducts
        fields = '__all__'