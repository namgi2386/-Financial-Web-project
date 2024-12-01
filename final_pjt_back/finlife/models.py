from django.db import models

class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 데이터유형 unique로, 금융 상품 코드
    kor_co_nm = models.TextField() # 금융회사명
    fin_prdt_nm = models.TextField() # 금융 상품명
    etc_note = models.TextField() # 금융 상품 설명
    join_deny = models.IntegerField() # 가입제한(1:제한없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입 방법
    spcl_cnd = models.TextField() # 우대조건
    mtrt_int = models.TextField(null=True, blank=True) # 만기후이자율
    max_limit = models.IntegerField(null=True, blank=True) # 최고한도
    dcls_strt_day = models.TextField(null=True, blank=True) # 공시 시작일
    dcls_end_day = models.TextField(null=True, blank=True) # 공시 종료일
    love_count = models.PositiveIntegerField(default=0)  # 좋아요 수

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE) # 외래키
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) # 저축금리 유형명
    intr_rate = models.FloatField() # 저축금리
    intr_rate2 = models.FloatField() # 최고우대금리
    save_trm = models.IntegerField() #저축기간(단위:개월)

# gpt가 수정해준 더미데이타 파이썬 코드 지금코드랑 비교해서 실행해봐야댐

class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 데이터유형 unique로, 금융 상품 코드
    kor_co_nm = models.TextField() # 금융회사명
    fin_prdt_nm = models.TextField() # 금융 상품명
    etc_note = models.TextField() # 금융 상품 설명
    join_deny = models.IntegerField() # 가입제한(1:제한없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입 방법
    spcl_cnd = models.TextField() # 우대조건
    mtrt_int = models.TextField(null=True, blank=True) # 만기후이자율
    max_limit = models.IntegerField(null=True, blank=True) # 최고한도
    dcls_strt_day = models.TextField(null=True, blank=True) # 공시 시작일
    dcls_end_day = models.TextField(null=True, blank=True) # 공시 종료일
    love_count = models.PositiveIntegerField(default=0)  # 좋아요 수

class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE) # 외래키
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) # 저축금리 유형명
    rsrv_type_nm = models.CharField(max_length=100) # 적립유형명
    intr_rate = models.FloatField() # 저축금리
    intr_rate2 = models.FloatField() # 최고우대금리
    save_trm = models.IntegerField() #저축기간(단위:개월)
