import random
from faker import Faker
from django.core.management.base import BaseCommand
from accounts.models import User, Profile, FinInfo
import string
from finlife.models import DepositProducts, SavingProducts

fake = Faker()

# 은행 리스트
banks = [
    "우리은행", "신한은행", "하나은행", "부산은행", "광주은행", "제주은행", "전북은행", "경남은행","중소기업은행", "한국산업은행","국민은행",
    "농협은행주식회사", "주식회사 케이뱅크", "수협은행", "주식회사 카카오뱅크", "토스뱅크 주식회사", "한국스탠다드차타드은행", "아이엠뱅크"
]

nicknames = [
"피카츄1", "피카츄2", "라이츄1", "라이츄2", "파이리1", "파이리2", "리자드1", "리자드2", "리자몽1", "리자몽2", 
"꼬부기1", "꼬부기2", "어니부기1", "어니부기2", "거북왕1", "거북왕2", "이상해씨1", "이상해씨2", "이상해풀1", "이상해풀2", 
"이상해꽃1", "이상해꽃2", "캐터피1", "캐터피2", "단데기1", "단데기2", "버터플1", "버터플2", "뿔충이1", "뿔충이2", 
"딱충이1", "딱충이2", "독침붕1", "독침붕2", "구구1", "구구2", "피죤1", "피죤2", "피죤투1", "피죤투2", "꼬렛1", 
"꼬렛2", "레트라1", "레트라2", "깨비참1", "깨비참2", "알통몬1", "알통몬2", "근육몬1", "근육몬2", "괴력몬1", "괴력몬2", 
"질퍽이1", "질퍽이2", "질뻐기1", "질뻐기2", "샐러리1", "샐러리2", "야도란1", "야도란2", "야돈1", "야돈2", "골뱃1", 
"골뱃2", "푸린1", "푸린2", "푸크린1", "푸크린2", "롱스톤1", "롱스톤2", "코터스1", "코터스2", "니드킹1", "니드킹2", 
"니드퀸1", "니드퀸2", "삐삐1", "삐삐2", "픽시1", "픽시2", "포니타1", "포니타2", "날쌩마1", "날쌩마2", "슬리프1", 
"슬리프2", "슬리퍼1", "슬리퍼2", "아라리1", "아라리2", "나시1", "나시2", "뿔카노1", "뿔카노2", "뿔카푸스1", "뿔카푸스2", 
"투구1", "투구2", "투구푸스1", "투구푸스2", "프테라1", "프테라2", "암나이트1", "암나이트2", "암스타1", "암스타2", 
"카이리1", "카이리2", "킹크랩1", "킹크랩2", "메타몽1", "메타몽2", "프리져1", "프리져2", "썬더1", "썬더2", "파이어1", 
"파이어2", "미뇽1", "미뇽2", "신뇽1", "신뇽2", "망나뇽1", "망나뇽2", "요가랑1", "요가랑2", "내루미1", "내루미2", 
"블래키1", "블래키2", "샤크니아1", "샤크니아2", "가디1", "가디2", "윈디1", "윈디2", "에브이1", "에브이2", "쥬피썬더1", 
"쥬피썬더2", "쥬레곤1", "쥬레곤2", "아보1", "아보2", "아보크1", "아보크2", "코뿌리1", "코뿌리2", "코리갑1", "코리갑2", 
"딱구리1", "딱구리2", "꼬마돌1", "꼬마돌2", "롱스톤1", "롱스톤2", "가이오가1", "가이오가2", "그란돈1", "그란돈2", 
"레쿠쟈1", "레쿠쟈2", "디아루가1", "디아루가2", "펄기아1", "펄기아2", "기라티나1", "기라티나2", "잉어킹1", "잉어킹2", 
"갸라도스1", "갸라도스2", "캔곰1", "캔곰2", "루기아1", "루기아2", "후파1", "후파2", "캡싸리1", "캡싸리2", "도나리1", 
"도나리2", "토게피1", "토게피2", "토게틱1", "토게틱2", "키링키1", "키링키2", "노공룡1", "노공룡2", "깜까미1", "깜까미2", 
"깜갈기1", "깜갈기2", "메가자리1", "메가자리2", "팬텀1", "팬텀2", "고오스1", "고오스2", "고우스트1", "고우스트2", 
"뽀뽀라1", "뽀뽀라2", "에레브1", "에레브2", "마그마1", "마그마2", "루브도1", "루브도2", "히포포타스1", "히포포타스2", 
"히포포타스킹1", "히포포타스킹2", "꼬리선1", "꼬리선2", "토대부기1", "토대부기2", "폴리곤1", "폴리곤2", "폴리곤2-1", "폴리곤2-2", 
"폴리곤Z1", "폴리곤Z2", "입치트1", "입치트2", "릴링1", "릴링2", "빙크고래1", "빙크고래2", "쉘곤1", "쉘곤2", 
"보만다1", "보만다2", "타만타1", "타만타2", "배루키1", "배루키2", "시라칸1", "시라칸2", "루카리오1", "루카리오2", 
"다크라이1", "다크라이2", "디안시1", "디안시2", "제크로무1", "제크로무2", "레시라무1", "레시라무2", "큐레무1", "큐레무2"
]


# 직업 리스트
jobs = [
    "직장인", "프리랜서", "자영업자", "학생", "전문직", "기타", "최강백수", "건물주", "포켓몬마스터" , "포켓몬" , "로켓단" , "관장"
]

# 목표 유형
goal_types = ["주택", "목돈", "결혼", "자녀"]

# MBTI 리스트
mbtis = ["ISTJ", "ISTP", "ISFJ", "ISFP", "INTJ", "INTP", "INFJ", "INFP", "ESTJ", "ESTP", "ESFJ", "ESFP", "ENTJ", "ENTP", "ENFJ", "ENFP"]

preference_types = ["복리" , "비대면" , "인터넷뱅킹" , "우대금리" ]

# 한글 2글자 랜덤 생성 함수
def generate_nickname():
    hangul_start = ord('가')
    hangul_end = ord('힣')
    return chr(random.randint(hangul_start, hangul_end)) + chr(random.randint(hangul_start, hangul_end))

# 더미 사용자 이름 생성
def generate_username(index):
    return f'user{index}'

# 더미 토큰 생성
def generate_token():
    return ''.join(random.choices(string.hexdigits.lower(), k=40))

# 더미 데이터를 생성하는 커맨드 클래스
class Command(BaseCommand):
    help = 'Generate dummy user data'

    def handle(self, *args, **kwargs):
        available_nicknames = nicknames[:]
        for i in range(1, 101):  # user1부터 user100까지 생성
            # User 모델 생성
            username = generate_username(i)
            while User.objects.filter(username=username).exists():
                username += str(random.randint(1000, 2000))
            user = User.objects.create_user(
                username=username,
                password='qwer1234!',
                # token=generate_token()
            )
            nickname = random.choice(available_nicknames)  # 랜덤으로 닉네임 선택
            available_nicknames.remove(nickname)


            # Profile 모델 생성
            profile = Profile.objects.create(
                user=user,
                age=random.randint(20, 50),
                money=random.uniform(1000000, 100000000),
                # nickname=generate_nickname(),
                nickname=nickname,
                desiredSubscriptionPeriod=random.choice([12, 24, 36]),
                mainBank=random.choice(banks),
            )
            
            # monthly_income 값 생성
            monthly_income = random.uniform(100000, 500000)
            
            # FinInfo 모델 생성
            fin_info = FinInfo.objects.create(
                user=user,
                job=random.choice(jobs),
                monthly_income=monthly_income,
                annual_income=monthly_income * 12,  # annual_income은 monthly_income * 12
                current_assets=random.uniform(1000000, 50000000),
                monthly_savings=random.uniform(10000, monthly_income * 0.4),  # monthly_savings는 monthly_income의 40% 이내로 설정
                fixed_expenses=random.uniform(10000, monthly_income * 0.3),  # fixed_expenses는 monthly_income의 30% 이내로 설정
                variable_expenses=random.uniform(10000, monthly_income * 0.3),  # variable_expenses는 monthly_income의 30% 이내로 설정
                goal_type=random.choice(goal_types),
                goal_amount=random.uniform(10000000, 50000000),
                goal_date=random.randint(1, 48),
                prefers_stability=random.choice([True, False]),
                preference_type=random.choice(preference_types),
                mbti=random.choice(mbtis),
            )

            # monthly_income보다 `monthly_savings + fixed_expenses + variable_expenses`의 합이 넘지 않도록 수정
            total_expenses = fin_info.monthly_savings + fin_info.fixed_expenses + fin_info.variable_expenses
            if total_expenses > fin_info.monthly_income:
                diff = total_expenses - fin_info.monthly_income
                fin_info.monthly_savings -= diff  # 초과된 금액만큼 monthly_savings에서 차감

            self.add_random_data_to_profiles([profile])
            # 출력 예시
            self.stdout.write(self.style.SUCCESS(f"Created user {username}"))

    

    def add_random_data_to_profiles(self, profiles):
        # DepositProducts와 SavingProducts에서 ID 목록을 가져옴
        deposit_ids = list(DepositProducts.objects.values_list('id', flat=True))
        saving_ids = list(SavingProducts.objects.values_list('id', flat=True))

        # Profiles에 대해 반복
        for profile in profiles:
            # Deposit에서 랜덤으로 20개 선택
            liked_deposit_ids = random.sample(deposit_ids, min(20, len(deposit_ids)))
            love_deposit_ids = random.sample(deposit_ids, min(20, len(deposit_ids)))

            # Saving에서 랜덤으로 20개 선택
            liked_saving_ids = random.sample(saving_ids, min(20, len(saving_ids)))
            love_saving_ids = random.sample(saving_ids, min(20, len(saving_ids)))

            # ManyToManyField에 추가
            profile.liked_products_deposit.add(*liked_deposit_ids)
            profile.love_deposit.add(*love_deposit_ids)
            profile.liked_products_saving.add(*liked_saving_ids)
            profile.love_saving.add(*love_saving_ids)

            for deposit_id in love_deposit_ids:
                deposit = DepositProducts.objects.get(id=deposit_id)
                deposit.love_count += 1
                deposit.save()

            for saving_id in love_saving_ids:
                saving = SavingProducts.objects.get(id=saving_id)
                saving.love_count += 1
                saving.save()