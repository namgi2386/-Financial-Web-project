from rest_framework import serializers
from .models import Profile , FinInfo


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    def update(self, instance, validated_data):
        profile_img = validated_data.pop('profile_img', None)
        if profile_img:
            instance.profile_img = profile_img
        return super().update(instance, validated_data)

class FinInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinInfo
        fields = '__all__'