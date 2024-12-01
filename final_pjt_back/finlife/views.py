from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.conf import settings

from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer , DepositTotalSerializer , SavingTotalSerializer
from rest_framework import status


FIN_API_KEY = settings.FIN_API_KEY
BASE_URL = 'http://finlife.fss.or.kr/'

topFinGrpNoForDB = '020000'
# 030300 , 020000
pageNoForDB = '1'

@api_view(['GET'])
def api_test(request):
    URL = BASE_URL + 'finlifeapi/depositProductsSearch.json'
    params = {
        'auth' : settings.FIN_API_KEY,
        'topFinGrpNo' : topFinGrpNoForDB,
        'pageNo' : pageNoForDB
    }
    response = requests.get(URL, params=params).json()
    return JsonResponse({'response': response['result']})


@api_view(['GET'])
def save_deposit_products(request): # DB 저장함수
    # print('-----------')
    # print('---eeee-----')
    # 1. api로부터 데이터 가져오기
    URL = BASE_URL + 'finlifeapi/depositProductsSearch.json'
    params = {
        'auth' : settings.FIN_API_KEY,
        'topFinGrpNo' : topFinGrpNoForDB,
        'pageNo' : pageNoForDB
    }
    response = requests.get(URL, params=params).json()

    # # 2. 원하는 필드 가져오기
    for dic in response['result']['baseList'] :
        fin_prdt_nm = dic.get('fin_prdt_nm')
        kor_co_nm = dic.get('kor_co_nm')
        fin_prdt_cd = dic.get('fin_prdt_cd')
        etc_note = dic.get('etc_note')
        join_deny = dic.get('join_deny')
        join_member = dic.get('join_member')
        join_way = dic.get('join_way')
        spcl_cnd = dic.get('spcl_cnd')
        mtrt_int = dic.get('mtrt_int')
        max_limit = dic.get('max_limit')
        dcls_strt_day = dic.get('dcls_strt_day')
        dcls_end_day = dic.get('dcls_end_day')

        if DepositProducts.objects.filter(fin_prdt_nm=fin_prdt_nm, 
                                            kor_co_nm=kor_co_nm,  
                                            fin_prdt_cd= fin_prdt_cd, 
                                            etc_note=etc_note, 
                                            join_deny=join_deny, 
                                            join_member=join_member,
                                            join_way=join_way, 
                                            spcl_cnd=spcl_cnd,
                                            mtrt_int=mtrt_int,
                                            max_limit=max_limit,
                                            dcls_strt_day=dcls_strt_day,
                                            dcls_end_day=dcls_end_day).exists():
            continue
        if DepositProducts.objects.filter(fin_prdt_cd= fin_prdt_cd).exists():
            continue
        # print('+++++++++++++')
        save_data = {
            'fin_prdt_nm': fin_prdt_nm,
            'kor_co_nm' :kor_co_nm,
            'fin_prdt_cd' : fin_prdt_cd,
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd,
            'mtrt_int' : mtrt_int,
            'max_limit' : max_limit,
            'dcls_strt_day' : dcls_strt_day,
            'dcls_end_day' : dcls_end_day,
        }
        # print('-------------^^^^-----------')
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    for dic in response['result']['optionList'] : 
        # print('-----///////////---')
        fin_prdt_cd = dic.get('fin_prdt_cd')
        intr_rate_type_nm = dic.get('intr_rate_type_nm')
        intr_rate = dic.get('intr_rate')
        intr_rate2 = dic.get('intr_rate2')
        save_trm = dic.get('save_trm')

        if DepositOptions.objects.filter( fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm = intr_rate_type_nm, intr_rate = intr_rate, intr_rate2 = intr_rate2, save_trm = save_trm ).exists():
            continue
        if not intr_rate:
            intr_rate = -1
        save_data = {
        'fin_prdt_cd' : fin_prdt_cd,
        'intr_rate_type_nm' : intr_rate_type_nm,
        'intr_rate' : intr_rate,
        'intr_rate2' : intr_rate2,
        'save_trm' : save_trm
        }
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer.save(product = product)
    return JsonResponse({'message' :'성공!' })


@api_view(['GET', 'POST'])
def deposit_products(request):
    # 전체 정기예금 상품
    if request.method == "GET":
        DepositProducts_list = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(DepositProducts_list, many=True)
        return Response(serializer.data)

    # 정기 예금 상품 추가하기
    elif request.method == "POST":
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': f'이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def deposit_options(request):
    # 전체 정기예금 옵션
    if request.method == "GET":
        options_list = DepositOptions.objects.all()
        serializer = DepositOptionsSerializer(options_list, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def deposit_product(request , fin_prdt_cd): # 특정 상품
    if request.method == "GET":
        # print('----------------')
        print()
        DepositProduct = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializer = DepositProductsSerializer(DepositProduct)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd): # 5. 특정 상품 옵션 리스트 출력
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_products_filter_bank(request, kor_co_nm):
    if request.method == "GET":
        DepositProduct = DepositProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositProductsSerializer(DepositProduct , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_products_filter_period(request, save_trm):
    if request.method == "GET":
        save_trm = int(save_trm)  # save_trm 값을 정수로 변환
        
        # save_trm 값과 정확히 일치하는 DepositOptions 필터링
        options = DepositOptions.objects.filter(save_trm=save_trm)
        
        # 관련된 DepositProducts를 가져오기 위해 fin_prdt_cd를 사용
        fin_prdt_cds = options.values_list('fin_prdt_cd', flat=True).distinct()
        products = DepositProducts.objects.filter(fin_prdt_cd__in=fin_prdt_cds)
        
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)



################################################## 여기부터 적금 ##########################


@api_view(['GET'])
def api_test_saving(request):
    URL = BASE_URL + 'finlifeapi/savingProductsSearch.json'
    params = {
        'auth' : settings.FIN_API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : '1'
    }
    response = requests.get(URL, params=params).json()
    return JsonResponse({'response': response['result']})

@api_view(['GET'])
def save_saving_products(request):
    # 1. api로부터 데이터 가져오기
    URL = BASE_URL + 'finlifeapi/savingProductsSearch.json'
    params = {
        'auth' : settings.FIN_API_KEY,
        'topFinGrpNo' : topFinGrpNoForDB,
        'pageNo' : pageNoForDB
    }
    response = requests.get(URL, params=params).json()

    # # 2. 원하는 필드 가져오기
    for dic in response['result']['baseList'] :
        fin_prdt_nm = dic.get('fin_prdt_nm')
        kor_co_nm = dic.get('kor_co_nm')
        fin_prdt_cd = dic.get('fin_prdt_cd')
        etc_note = dic.get('etc_note')
        join_deny = dic.get('join_deny')
        join_member = dic.get('join_member')
        join_way = dic.get('join_way')
        spcl_cnd = dic.get('spcl_cnd')
        mtrt_int = dic.get('mtrt_int')
        max_limit = dic.get('max_limit')
        dcls_strt_day = dic.get('dcls_strt_day')
        dcls_end_day = dic.get('dcls_end_day')

        if SavingProducts.objects.filter(fin_prdt_nm=fin_prdt_nm , 
                                            kor_co_nm=kor_co_nm ,  
                                            fin_prdt_cd= fin_prdt_cd , 
                                            etc_note=etc_note , 
                                            join_deny=join_deny , 
                                            join_member=join_member ,
                                            join_way=join_way , 
                                            spcl_cnd=spcl_cnd,
                                            mtrt_int=mtrt_int,
                                            max_limit=max_limit,
                                            dcls_strt_day=dcls_strt_day,
                                            dcls_end_day=dcls_end_day).exists():
            continue # 
        if SavingProducts.objects.filter(fin_prdt_cd= fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_nm': fin_prdt_nm,
            'kor_co_nm' :kor_co_nm,
            'fin_prdt_cd' : fin_prdt_cd,
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd,
            'mtrt_int' : mtrt_int,
            'max_limit' : max_limit,
            'dcls_strt_day' : dcls_strt_day,
            'dcls_end_day' : dcls_end_day,
        }
        serializer = SavingProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    for dic in response['result']['optionList'] : 
        fin_prdt_cd = dic.get('fin_prdt_cd')
        intr_rate_type_nm = dic.get('intr_rate_type_nm')
        rsrv_type_nm = dic.get('rsrv_type_nm')
        intr_rate = dic.get('intr_rate')
        intr_rate2 = dic.get('intr_rate2')
        save_trm = dic.get('save_trm')

        if SavingOptions.objects.filter( fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm = intr_rate_type_nm,rsrv_type_nm=rsrv_type_nm, intr_rate = intr_rate, intr_rate2 = intr_rate2, save_trm = save_trm ).exists():
            continue
        if not intr_rate:
            intr_rate = -1
        save_data = {
        'fin_prdt_cd' : fin_prdt_cd,
        'intr_rate_type_nm' : intr_rate_type_nm,
        'rsrv_type_nm':rsrv_type_nm,
        'intr_rate' : intr_rate,
        'intr_rate2' : intr_rate2,
        'save_trm' : save_trm
        }
        serializer = SavingOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer.save(product = product)
    return JsonResponse({'message' :'성공!' })

@api_view(['GET', 'POST'])
def saving_products(request):
    # 전체 정기예금 상품
    if request.method == "GET":
        SavingProducts_list = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(SavingProducts_list, many=True)
        return Response(serializer.data)

    # 정기 예금 상품 추가하기
    elif request.method == "POST":
        serializer = SavingProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': f'이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def saving_options(request):
    # 전체 정기예금 옵션
    if request.method == "GET":
        options_list = SavingOptions.objects.all()
        serializer = SavingOptionsSerializer(options_list, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def saving_product(request , fin_prdt_cd): # 특정 상품
    if request.method == "GET":
        SavingProduct = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializer = SavingProductsSerializer(SavingProduct)
    return Response(serializer.data)

@api_view(['GET'])
def saving_product_options(request, fin_prdt_cd): # 5. 특정 상품 옵션 리스트 출력
    options = SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_products_filter_bank(request, kor_co_nm): # 은행 필터링
    if request.method == "GET":
        SavingProduct = SavingProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingProductsSerializer(SavingProduct , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def saving_products_filter_period(request, save_trm):
    if request.method == "GET":
        save_trm = int(save_trm)  # save_trm 값을 정수로 변환
        
        # save_trm 값과 정확히 일치하는 DepositOptions 필터링
        options = SavingOptions.objects.filter(save_trm=save_trm)
        
        # 관련된 DepositProducts를 가져오기 위해 fin_prdt_cd를 사용
        fin_prdt_cds = options.values_list('fin_prdt_cd', flat=True).distinct()
        products = SavingProducts.objects.filter(fin_prdt_cd__in=fin_prdt_cds)
        
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def saving_products_filter_type(request , rsrv_type_nm):
    if request.method == "GET":
        
        options = SavingOptions.objects.filter(rsrv_type_nm=rsrv_type_nm)
        fin_prdt_cds = options.values_list('fin_prdt_cd', flat=True).distinct()
        products = SavingProducts.objects.filter(fin_prdt_cd__in=fin_prdt_cds)
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)
    

############# test

@api_view(['GET'])
def deposit_products_with_options(request):
    if request.method == "GET":
        deposit_products = DepositProducts.objects.prefetch_related('depositoptions_set').all()
        serializer = DepositTotalSerializer(deposit_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def saving_products_with_options(request):
    if request.method == "GET":
        saving_products = SavingProducts.objects.prefetch_related('savingoptions_set').all()
        serializer = SavingTotalSerializer(saving_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

