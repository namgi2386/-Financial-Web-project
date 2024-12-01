from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your models here.
class User(AbstractUser): # username 은 4글자 이하로 작성하며 비밀번호는 qwer1234! 로 통일 token 값은 fd379c618eec97253b23133f1ce53f890eed8950 와 유사한 40자 길이의 16진수 문자열로 중복되지 않게 순차적으로 작성
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True) # 20세 ~ 50세 사이 선택
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # 현재자산

    nickname = models.CharField(max_length=30, default='nickname_none') # 2rm
    desiredSubscriptionPeriod = models.IntegerField(default=12) # 12 or 24 or 36
    mainBank = models.CharField(max_length=30, default='bank_none') # "SC제일은행", "경남은행", "광주은행", "국민은행", "기업은행", "농협은행", "대구은행", "부산은행", "수협은행", "신한은행", "외환은행", "우리은행", "전북은행", "제주은행", "하나은행", "한국산업은행", "한국시티은행" 중에서 선택
    profile_img = models.ImageField(upload_to='accounts/', null=True, blank=True)

    liked_products_deposit = models.ManyToManyField('finlife.DepositProducts', blank=True, related_name="liked_by_users_deposit") # 1~180 사이의 랜덤 자연수 값 20개가 포함되도록
    love_deposit = models.ManyToManyField('finlife.DepositProducts', blank=True, related_name="loved_by_users_deposit") # 1~180 사이의 랜덤 자연수 값 20개가 포함되도록

    liked_products_saving = models.ManyToManyField('finlife.SavingProducts', blank=True, related_name="liked_by_users_saving") # 1~180 사이의 랜덤 자연수 값 20개가 포함되도록
    love_saving = models.ManyToManyField('finlife.SavingProducts', blank=True, related_name="loved_by_users_saving") # 1~180 사이의 랜덤 자연수 값 20개가 포함되도록


    def __str__(self):
        return f"{self.user.username}'s Profile"

class FinInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fininfo")
    job = models.CharField(max_length=50, null=True, blank=True)  # 직업 한글작성
    monthly_income = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # 월 소득
    annual_income = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # 연 소득
    current_assets = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )  # 현재 자산 규모
    monthly_savings = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # 월별 저축 가능 금액
    fixed_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # 고정지출금액
    variable_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # 변동지출금액
    goal_type = models.CharField(max_length=100, null=True, blank=True)  # 목표 유형 : 주택 , 목돈 , 결혼 , 자녀 중에서 하나 선택할 예정
    goal_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )  # 목표 금액
    goal_date = models.IntegerField(null=True, blank=True)  # 목표 시점까지의 개월수 : 1~48 사이의 자연수로 작성 
    prefers_stability = models.BooleanField(default=False)  # 안정성 선호 여부
    preference_type = models.CharField(max_length=100, null=True, blank=True)  # 추가 사항 적는 칸 (고금리선호 좋은혜택 복리선호 등등 자유롭게 키워드형태로 적는칸)
    mbti = models.CharField(max_length=4, null=True, blank=True)  # MBTI의 종류중에서 선택 "ISTJ,ISTP,ISFJ,ISFP,INTJ,INTP,INFJ,INFP,ESTJ,ESTP,ESFJ,ESFP,ENTJ,ENTP,ENFJ,ENFP" 

    def __str__(self):
        return f"{self.user.username}'s Financial Info"
    