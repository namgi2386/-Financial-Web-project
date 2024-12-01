from django.db import models
from django.db.models import Count, Case, When, Value, CharField , Q ,OuterRef, Subquery , IntegerField
from rest_framework.decorators import api_view
from rest_framework.response import Response
from finlife.models import DepositProducts , DepositOptions , SavingOptions, SavingProducts
from accounts.models import FinInfo
from decimal import Decimal

@api_view(['GET'])
def recommendByAge(request):
    user_current_assets = request.user.fininfo.current_assets
    user_goal_date = request.user.fininfo.goal_date
    # 나이대를 구간으로 분류 (20대, 30대, 40대)
    age_groups = (
        Case(
            When(liked_by_users_deposit__age__gte=20, liked_by_users_deposit__age__lt=30, then=Value('20대')),
            When(liked_by_users_deposit__age__gte=30, liked_by_users_deposit__age__lt=40, then=Value('30대')),
            When(liked_by_users_deposit__age__gte=40, liked_by_users_deposit__age__lt=50, then=Value('40대')),
            default=Value('기타'),
            output_field=CharField(),
        )
    )

    # DepositProducts와 연결된 Profile 정보로 나이대별 찜 수 계산
    liked_products = (
        DepositProducts.objects.annotate(
            age_group=age_groups,  # 나이대 필드 추가
        )
        .values('age_group', 'id', 'fin_prdt_nm' , "kor_co_nm" , "etc_note")  # 나이대, 상품 ID, 상품명
        .annotate(like_count=Count('liked_by_users_deposit'))  # 찜한 수 계산
        .order_by('age_group', '-like_count')  # 나이대별로 정렬
    )
    result = []
    for product in liked_products:
        best_option = DepositOptions.objects.filter(
            product=product['id'],
            save_trm__lte=user_goal_date
        ).order_by('-save_trm').first()

        if best_option:
            final_savings = calculate_monthly_deposit(
                user_current_assets , best_option, best_option.save_trm
            )
            product_data = {
                'id': product['id'],
                'kor_co_nm': product['kor_co_nm'],
                'fin_prdt_nm': product['fin_prdt_nm'],
                'age_group' : product['age_group'],
                'like_count' : product['like_count'],
                'etc_note' : product['etc_note'],
                'best_option': {
                    'id': best_option.id,
                    'intr_rate_type_nm': best_option.intr_rate_type_nm,
                    'save_trm': best_option.save_trm,
                    'intr_rate': best_option.intr_rate,
                    'final_savings': final_savings
                }
            }
            result.append(product_data)

    return Response(result)

#spcl_cnd , etc_note , fin_prdt_nm
#user_goal_type , user_preference_type
########################################## 테스트용 ###########################
@api_view(['GET'])
def recommendByGoalType(request):
    user_goal_type = request.user.fininfo.goal_type
    user_preference_type = request.user.fininfo.preference_type
    goaltype_products = (
        DepositProducts.objects.filter(Q(fin_prdt_nm__icontains=user_goal_type) | Q(spcl_cnd__icontains=user_goal_type) | Q(etc_note__icontains=user_goal_type) | 
                                        Q(fin_prdt_nm__icontains=user_preference_type) | Q(spcl_cnd__icontains=user_preference_type) | Q(etc_note__icontains=user_preference_type))  # goal_type 포함 필터
        .annotate(like_count=Count('liked_by_users_deposit'))  # 찜 수 계산
        .order_by('-like_count')  # 찜 수 내림차순 정렬
        .values('id','kor_co_nm', 'fin_prdt_nm', 'like_count')  # 필요한 필드만 반환
    )
    return Response(list(goaltype_products))
########################################## 테스트용 ###########################



@api_view(['GET'])
def recommendByMBTI(request):
    user_mbti = request.user.fininfo.mbti  # MBTI 값 가져오기
    user_goal_date = request.user.fininfo.goal_date
    current_assets = request.user.fininfo.current_assets

    # 각 MBTI 유형에 따라 필터링 조건 설정
    mbti_type1_ip = ["ISTP", "ISFP", "INTP", "INFP"]  # 비대면 + 기간 짧은걸로
    mbti_type2_ij = ["ISTJ", "ISFJ", "INTJ", "INFJ"]  # 비대면 + 기간 긴걸로
    mbti_type3_ep = ["ESTP", "ESFP", "ENTP", "ENFP"]  # 대면 + 기간 짧은걸로
    mbti_type4_ej = ["ESTJ", "ESFJ", "ENTJ", "ENFJ"]  # 대면 + 기간 긴걸로

    filtered_products = DepositProducts.objects.all()

    if user_mbti in mbti_type1_ip:
        # 비대면 + 기간 짧은 걸로
        filtered_products = DepositProducts.objects.filter(
            Q(spcl_cnd__icontains="비대면") |
            Q(etc_note__icontains="비대면") |
            Q(fin_prdt_nm__icontains="비대면")
        ).annotate(
            min_save_trm=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("save_trm")
                .values("save_trm")[:1]
            ),
            max_intr_rate2=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-intr_rate2")
                .values("intr_rate2")[:1]
            )
        ).order_by("min_save_trm", "-max_intr_rate2")

    elif user_mbti in mbti_type2_ij:
        # 비대면 + 기간 긴 걸로
        filtered_products = DepositProducts.objects.filter(
            Q(spcl_cnd__icontains="비대면") |
            Q(etc_note__icontains="비대면") |
            Q(fin_prdt_nm__icontains="비대면")
        ).annotate(
            max_save_trm=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-save_trm")
                .values("save_trm")[:1]
            ),
            max_intr_rate2=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-intr_rate2")
                .values("intr_rate2")[:1]
            )
        ).order_by("-max_save_trm", "-max_intr_rate2")

    elif user_mbti in mbti_type3_ep:
        # 대면 + 기간 짧은 걸로
        filtered_products = DepositProducts.objects.annotate(
            min_save_trm=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("save_trm")
                .values("save_trm")[:1]
            ),
            max_intr_rate2=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-intr_rate2")
                .values("intr_rate2")[:1]
            )
        ).order_by("min_save_trm", "-max_intr_rate2")

    elif user_mbti in mbti_type4_ej:
        # 대면 + 기간 긴 걸로
        filtered_products = DepositProducts.objects.annotate(
            max_save_trm=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-save_trm")
                .values("save_trm")[:1]
            ),
            max_intr_rate2=Subquery(
                DepositOptions.objects.filter(product=models.OuterRef("pk"))
                .order_by("-intr_rate2")
                .values("intr_rate2")[:1]
            )
        ).order_by("-max_save_trm", "-max_intr_rate2")

    # 가장 최상의 옵션 하나만 선택
    result = []
    for product in filtered_products:
        # MBTI 유형에 맞춰 정렬 기준 설정
        if user_mbti in mbti_type1_ip or user_mbti in mbti_type3_ep:  # 기간 짧은 걸로
            best_option = DepositOptions.objects.filter(product=product) \
                .order_by('save_trm' ,'-intr_rate2'  ).first()  # save_trm 오름차순, intr_rate2 내림차순
        else:  # 기간 긴 걸로
            best_option = DepositOptions.objects.filter(product=product) \
                .order_by('-save_trm','-intr_rate2' ).first()  # save_trm 내림차순, intr_rate2 내림차순

        if best_option:
            final_savings = calculate_monthly_deposit(
                current_assets , best_option, best_option.save_trm
            )

            product_data = {
                "id": product.id,
                "kor_co_nm": product.kor_co_nm,
                "fin_prdt_nm": product.fin_prdt_nm,
                "spcl_cnd": product.spcl_cnd,
                "etc_note": product.etc_note,
                "best_option": {
                    'id' : best_option.id,
                    'intr_rate_type_nm': best_option.intr_rate_type_nm,
                    'save_trm': best_option.save_trm,
                    'intr_rate': best_option.intr_rate,
                    'final_savings': final_savings
                }
            }
            result.append(product_data)

    return Response(result)


# DepositProducts
# DepositOptions
@api_view(['GET'])
def recommendByPrivateDeposit(request):
    user_goal_type = request.user.fininfo.goal_type
    user_preference_type = request.user.fininfo.preference_type
    user_goal_date = request.user.fininfo.goal_date  # 사용자가 설정한 목표 저축기간 (개월수)
    current_assets = request.user.fininfo.current_assets
    user_mainbank = request.user.profile.mainBank
    filtered_products = DepositProducts.objects.filter(
        # Q(kor_co_nm__icontains=user_mainbank) |
        # Q(fin_prdt_nm__icontains=user_goal_type) | 
        # Q(spcl_cnd__icontains=user_goal_type) |
        # Q(etc_note__icontains=user_goal_type) |
        # Q(fin_prdt_nm__icontains=user_preference_type) |
        # Q(spcl_cnd__icontains=user_preference_type) |
        # Q(etc_note__icontains=user_preference_type)
    ).annotate(
        max_save_trm=Subquery(
            DepositOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)  # 목표 저축기간 이하로 필터
            .order_by('-save_trm')
            .values('save_trm')[:1]
        ),
        best_intr_rate=Subquery(
            DepositOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)  # 목표 저축기간 이하로 필터
            .order_by('-intr_rate')  # 금리가 높은 순으로 정렬
            .values('intr_rate')[:1]
        ),
        best_option_id=Subquery(
            DepositOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)
            .order_by('-intr_rate')  # 금리가 높은 순으로 정렬
            .values('id')[:1]
        )
    ).order_by(
        Case(
            When(kor_co_nm=user_mainbank, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
    ),'-best_intr_rate')  # 금리가 높은 순으로 정렬
    # 상품에 대한 최적 옵션을 포함하여 반환
    result = []
    for product in filtered_products:
        try:
            best_option = DepositOptions.objects.get(id=product.best_option_id)  # 최적의 옵션
        except DepositOptions.DoesNotExist:
            continue
        best_option = DepositOptions.objects.get(id=product.best_option_id)  # 최적의 옵션
        final_savings = calculate_monthly_deposit(current_assets,best_option, best_option.save_trm)  # 최종 저축액 계산
        if all([product.id, product.kor_co_nm, product.fin_prdt_nm, best_option.id, 
            best_option.intr_rate_type_nm, best_option.save_trm, best_option.intr_rate]):
            product_data = {
                'id': product.id,
                'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm,
                'best_option': {
                    'id': best_option.id,
                    'intr_rate_type_nm' : best_option.intr_rate_type_nm,
                    'save_trm': best_option.save_trm,
                    'intr_rate': best_option.intr_rate,
                    'final_savings': final_savings
                }
            }
            result.append(product_data)
    return Response(result)




@api_view(['GET'])
def recommendByPrivateSaving(request):
    user_goal_type = request.user.fininfo.goal_type
    user_preference_type = request.user.fininfo.preference_type
    user_goal_date = request.user.fininfo.goal_date  # 사용자가 설정한 목표 저축기간 (개월수)
    monthly_savings = request.user.fininfo.monthly_savings
    user_mainbank = request.user.profile.mainBank
    current_assets = request.user.fininfo.current_assets
    # 조건에 맞는 DepositProducts 필터링
    # SavingProducts
    # SavingOptions
    filtered_products = SavingProducts.objects.filter(
        # Q(fin_prdt_nm__icontains=user_goal_type) | 
        # Q(spcl_cnd__icontains=user_goal_type) |
        # Q(etc_note__icontains=user_goal_type) |
        # Q(fin_prdt_nm__icontains=user_preference_type) |
        # Q(spcl_cnd__icontains=user_preference_type) |
        # Q(etc_note__icontains=user_preference_type)
    ).annotate(
        max_save_trm=Subquery(
            SavingOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)  # 목표 저축기간 이하로 필터
            .order_by('-save_trm')
            .values('save_trm')[:1]
        ),
        best_intr_rate=Subquery(
            SavingOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)  # 목표 저축기간 이하로 필터
            .order_by('-intr_rate')  # 금리가 높은 순으로 정렬
            .values('intr_rate')[:1]
        ),
        best_option_id=Subquery(
            SavingOptions.objects.filter(product=models.OuterRef('pk'))
            .filter(save_trm__lte=user_goal_date)
            .order_by('-intr_rate')  # 금리가 높은 순으로 정렬
            .values('id')[:1]
        )
    ).order_by(
        Case(
            When(kor_co_nm=user_mainbank, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
    ), '-best_intr_rate')  # 금리가 높은 순으로 정렬

    # 상품에 대한 최적 옵션을 포함하여 반환
    result = []
    for product in filtered_products:
        try:
            best_option = DepositOptions.objects.get(id=product.best_option_id)  # 최적의 옵션
        except DepositOptions.DoesNotExist:
            continue
        best_option = SavingOptions.objects.get(id=product.best_option_id)  # 최적의 옵션
        final_savings = calculate_monthly_savings(current_assets,monthly_savings,best_option, best_option.save_trm)  # 최종 저축액 계산
        
        product_data = {
            'id': product.id,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'best_option': {
                'id': best_option.id,
                'intr_rate_type_nm' : best_option.intr_rate_type_nm,
                'save_trm': best_option.save_trm,
                'intr_rate': best_option.intr_rate,
                'final_savings': final_savings
            }
        }
        result.append(product_data)
    return Response(result)
















from decimal import Decimal

def calculate_monthly_savings(current_assets,monthly_savings, option, goal_date):
    """
    매월마다의 원금, 누적 이자, 실수령액을 계산하여 리스트로 반환하는 함수
    - 단리와 복리 계산 방식에 따라 달라짐
    """
    
    result = []  # 결과를 저장할 리스트

    # 초기 값 설정
    principal = Decimal(0)  # 해당 월까지의 누적 원금
    revenue = Decimal(0)    # 해당 월까지의 누적 이자
    monthly_interest_rate = Decimal(option.intr_rate) / Decimal(12) / Decimal(100)  # 월 이자율

    for month in range(1, goal_date + 1):
        # 매월 저축한 금액을 원금에 추가
        principal += Decimal(monthly_savings)

        if option.intr_rate_type_nm == '단리':  # 단리 계산
            # 단리 누적 이자: 원금 * 월 이자율 * 경과 월수
            revenue = principal * monthly_interest_rate * Decimal(month)
        elif option.intr_rate_type_nm == '복리':  # 복리 계산
            # 복리 누적 이자: 매월 복리 계산으로 총 누적 금액을 기준으로 업데이트
            total_savings = (principal + revenue) * (Decimal(1) + monthly_interest_rate)
            revenue = total_savings - principal  # 누적된 이자만 계산
        else:
            revenue = Decimal(0)
        
        total_savings = principal + revenue  # 실수령액: 원금 + 누적 이자

        # 해당 월의 원금, 누적 이자, 실수령액 기록
        result.append({
            'month': month,
            'principal': principal,
            'revenue': revenue,
            'final': total_savings + current_assets - monthly_savings
        })

    return result


def calculate_monthly_deposit(current_assets, option, goal_date):
    # 예금방식으로 단리 복리에 따라 계산
    result = []  # 결과를 저장할 리스트

    # 초기 값 설정
    principal = Decimal(current_assets)  # 해당 월까지의 누적 원금
    revenue = Decimal(0)    # 해당 월까지의 누적 이자
    monthly_interest_rate = Decimal(option.intr_rate) / Decimal(12) / Decimal(100)  # 월 이자율

    for month in range(1, goal_date + 1):
        
        if option.intr_rate_type_nm == '단리':  # 단리 계산
            # 단리 누적 이자: 원금 * 월 이자율 * 경과 월수
            revenue = principal * Decimal(option.intr_rate) * Decimal(month) / Decimal(12) / Decimal(100)
        elif option.intr_rate_type_nm == '복리':  # 복리 계산
            # 복리 누적 이자: 매월 복리 계산으로 총 누적 금액을 기준으로 업데이트
            total_savings = principal * ((Decimal(1) + monthly_interest_rate) ** Decimal(month))
            revenue = total_savings - principal  # 누적된 이자만 계산
        else:
            revenue = Decimal(0)
        
        total_savings = principal + revenue  # 실수령액: 원금 + 누적 이자
        # 해당 월의 원금, 누적 이자, 실수령액 기록
        result.append({
            'month': month,
            'principal': principal,
            'revenue': revenue,
            # 'final': total_savings
            'final': revenue
        })
    return result


