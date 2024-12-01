from rest_framework import serializers
from .models import ArticleFree , FreeRecommend 
from accounts.models import User , Profile



class ArticleFreeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class RecommendSerializerFree(serializers.ModelSerializer):
        class Meta:
            model = FreeRecommend
            exclude = ('articlefree',)
    freerecommend_set  = RecommendSerializerFree(many=True , read_only=True)
    class Meta:
        model = ArticleFree
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        # exclude = ('articlefree',)

class ArticleFreeListSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source='user.profile')
    class Meta:
        model = ArticleFree
        fields = ['id', 'title', 'content', 'created_at','updated_at', 'category', 'user', 'user_profile']



# class FreeRecommendedSerializer(serializers.ModelSerializer):
#     recommend_user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = FreeRecommend
#         fields = '__all__'
#         read_only_fields = ('articlefree', 'recommend_user')
#         # fields = ('content',)
class FreeRecommendedSerializer(serializers.ModelSerializer):
    recommend_user_nickname = serializers.CharField(source='recommend_user.profile.nickname', read_only=True)
    recommend_user_profile_img = serializers.ImageField(source='recommend_user.profile.profile_img', read_only=True)

    class Meta:
        model = FreeRecommend
        fields = '__all__'
        read_only_fields = ('articlefree', 'recommend_user')
