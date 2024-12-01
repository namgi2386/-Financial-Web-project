from django.contrib.auth import get_user_model #
from rest_framework.decorators import api_view ,  permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render , get_object_or_404
# from django.contrib.auth.models import User
from accounts.models import Profile , FinInfo
from accounts.serializers import ProfileSerializer , FinInfoSerializer
from rest_framework.permissions import IsAuthenticated

from finlife.models import DepositProducts ,SavingProducts
from finlife.serializers import DepositProductsSerializer  , SavingProductsSerializer

User = get_user_model() #

@api_view(['POST'])
def custom_signup(request):
    print(request.data)
    username = request.data.get('username')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    age = request.data.get('age')
    money = request.data.get('money')
    nickname = request.data.get('nickname')
    desiredSubscriptionPeriod = request.data.get('desiredSubscriptionPeriod')
    mainBank = request.data.get('mainBank')
    profile_img = request.FILES.get('profile')

    if password1 != password2:
        return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    if not username or not password1:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password1)

    Profile.objects.create(user=user, age=age, money=money, nickname=nickname, desiredSubscriptionPeriod=desiredSubscriptionPeriod ,mainBank=mainBank , profile_img=profile_img )
    FinInfo.objects.create(user=user)

    return Response({"message": "User and Profile created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def user_delete(request, username):
    if request.method == 'DELETE':
        if request.user.username == username:
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def getmyprofile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def getmyfininfo(request):
    fininfo = FinInfo.objects.get(user=request.user )
    if request.method == 'GET':
        serializer = FinInfoSerializer(fininfo)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FinInfoSerializer(fininfo, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PUT'])
def getDetailprofile(request , user_id):
    print('---')
    print('---')
    # profile = Profile.objects.get(user=request.user)
    print(user_id)
    profile = get_object_or_404(Profile, user=user_id)
    print(profile)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


########################################## 여기서부터 예금상품 ####################################

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product_deposit(request, fin_prdt_cd): ##################### 찜!!! 하기
    try:
        profile = Profile.objects.get(user=request.user)
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if profile.liked_products_deposit.filter(fin_prdt_cd=product.fin_prdt_cd).exists():
            return Response({"error": "Product already liked"}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.liked_products_deposit.add(product)
        return Response({"message": f"Product {product.fin_prdt_nm} added to liked_products_deposit"}, status=status.HTTP_200_OK)
    
    except DepositProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_product_deposit(request, fin_prdt_cd):  ##################### 찜!!! 제거하기
    try:
        profile = Profile.objects.get(user=request.user)
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if not profile.liked_products_deposit.filter(fin_prdt_cd=product.fin_prdt_cd).exists():
            return Response({"error": "Product is not in liked_products_deposit"}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.liked_products_deposit.remove(product)
        return Response({"message": f"Product {product.fin_prdt_nm} removed from liked_products_deposit"}, status=status.HTTP_200_OK)
    
    except DepositProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) ################### 찜 조회하기
def get_liked_products_deposit(request):
    try:
        profile = Profile.objects.get(user=request.user)
        liked_products_deposit = profile.liked_products_deposit.all()
        serializer = DepositProductsSerializer(liked_products_deposit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_love(request, fin_prdt_cd): ################### 좋아요 추가 제거
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        profile = request.user.profile

        if profile.love_deposit.filter(fin_prdt_cd=fin_prdt_cd).exists():
            profile.love_deposit.remove(product)
            product.love_count -= 1
            product.save()
            return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)
        else:
            profile.love_deposit.add(product)
            product.love_count += 1
            product.save()
            return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)

    except DepositProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_love_products(request): ####################### 현재 사용자가 좋아요한 상품 리스트 조회
    try:
        profile = request.user.profile
        love_deposits = profile.love_deposit.all()
        data = [
            {"id": product.id, "name": product.fin_prdt_nm, "love_count": product.love_count}
            for product in love_deposits
        ]
        return Response(data, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_product_loves(request, fin_prdt_cd): ############## 특정 상품의 좋아요 수 조회
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)

    except DepositProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

########################################## 여기서부터 적금상품 ####################################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product_saving(request, fin_prdt_cd): ##################### 찜!!! 하기
    try:
        profile = Profile.objects.get(user=request.user)
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if profile.liked_products_saving.filter(fin_prdt_cd=product.fin_prdt_cd).exists():
            return Response({"error": "Product already liked"}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.liked_products_saving.add(product)
        return Response({"message": f"Product {product.fin_prdt_nm} added to liked_products_saving"}, status=status.HTTP_200_OK)
    
    except SavingProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_product_saving(request, fin_prdt_cd):  ##################### 찜!!! 제거하기
    try:
        profile = Profile.objects.get(user=request.user)
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if not profile.liked_products_saving.filter(fin_prdt_cd=product.fin_prdt_cd).exists():
            return Response({"error": "Product is not in liked_products_saving"}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.liked_products_saving.remove(product)
        return Response({"message": f"Product {product.fin_prdt_nm} removed from liked_products_saving"}, status=status.HTTP_200_OK)
    
    except SavingProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) ################### 찜 조회하기
def get_liked_products_saving(request):
    try:
        profile = Profile.objects.get(user=request.user)
        liked_products_saving = profile.liked_products_saving.all()
        serializer = SavingProductsSerializer(liked_products_saving, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_love_saving(request, fin_prdt_cd): ################### 좋아요 추가 제거
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        profile = request.user.profile

        if profile.love_saving.filter(fin_prdt_cd=fin_prdt_cd).exists():
            profile.love_saving.remove(product)
            product.love_count -= 1
            product.save()
            return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)
        else:
            profile.love_saving.add(product)
            product.love_count += 1
            product.save()
            return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)

    except SavingProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_love_products_saving(request): ####################### 현재 사용자가 좋아요한 상품 리스트 조회
    try:
        profile = request.user.profile
        love_savings = profile.love_saving.all()
        data = [
            {"id": product.id, "name": product.fin_prdt_nm, "love_count": product.love_count}
            for product in love_savings
        ]
        return Response(data, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_product_loves_saving(request, fin_prdt_cd): ############## 특정 상품의 좋아요 수 조회
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        return Response({"love_count": product.love_count}, status=status.HTTP_200_OK)

    except SavingProducts.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)