<template>
  <div class="container">
    <div class="no1box">
      <div class="target d-none d-xl-flex">
        <div v-if="!userStore.isLogin"> 
          <!-- 로그인 안한상태 -->
          <button class="product-item" @click="pushToLogin">목표설정 하러가기</button>
          <p class="custom-text">금융정보 입력하고 목표분석하러 가볼까요??</p>
          <img :src="dog1" alt="강아지" class="right-align_1" width="45%;" height="auto" @click="pushToLogin">
        </div>
        <div v-else-if="!is_fin && userStore.isLogin">
          <!-- 금융정보 없음 -->
          <button class="product-item" @click="pushToProfile">목표설정 하러가기</button>
          <p class="custom-text">금융정보 입력하고 목표분석하러 가볼까요??</p>
          <img :src="dog1" alt="강아지" class="right-align_1" width="45%;" height="auto" @click="pushToProfile">
        </div>
        <div v-else id="resultchartbox">
          <!-- 로그인ok 금융정보ok -->
          <ResultRecommend :myCart="my_cart" @add-to-cart="addToCart" ></ResultRecommend>
        </div>
      </div>
  
      <div class="submenu" v-if="userStore.isLogin && is_fin">
        <div class="submenu-top">
          <div class="submenu-top-1">
            <div class="profile-container text-center p-2">
              <img :src="profileImageUrl" alt="프로필 사진" class="profile-preview" />
            </div>
            <div class="welcome-message text-center mb-2">
              <span class="highlighted">{{ userStore.profileData.nickname }}</span>
              <span>님 환영합니당</span>
            </div>
            <div class="hashtag-container">
              <span class="hashtag"><span style="font-size: 14px; color: #072448;">주거래은행</span> <br> #{{ userStore.profileData.mainBank }}</span>
              <span class="hashtag"><span style="font-size: 14px; color: #072448;">현재 자산</span> <br> #{{ formatMoney(userStore.finInfoData.current_assets) }}원</span>
            </div>
            <div class="hashtag-container">
              <span class="hashtag"><span style="font-size: 14px; color: #072448;">목표 개월수</span> <br> #{{ userStore.finInfoData.goal_date }}개월</span>
              <span class="hashtag"><span style="font-size: 14px; color: #072448;">월별 저축</span> <br> #{{ formatMoney(userStore.finInfoData.monthly_savings) }}원</span>
            </div>
          </div>
          <div class="submenu-top-2">
            <div class="submenu-top-3">
              <router-link to="exchangerate">
                <img :src="moneyImage" alt="환율" width="50%;" height="auto">
              </router-link>
            </div>
            <!-- <div class="submenu-top-3"></div> -->
            <div class="submenu-top-3">
              <router-link to="/bank">
                <img :src="mapImage" alt="지도" width="50%" height="auto">
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <div class="submenu" v-else>
        <div class="submenu-item hover-effect" @click="pushToExchange">
          <h4 class="title"><strong>환율 계산</strong></h4>
          <p style="color: #979797;">해외 송금시 비용을 절약하세요. <br>환율을 알아보러 갈까요??</p>
          <img :src="moneyImage" alt="환율" class="right-align" width="20%;" height="auto">
        </div>
        <div class="submenu-item hover-effect" @click="pushToMap">
          <h4 class="title"><strong>은행 찾기</strong></h4>
          <p style="color: #979797;">현재위치, 내가 원하는 위치에서 <br>가까운 은행을 찾아보세요.</p>
          <img :src="mapImage" alt="지도" class="right-align" width="20%" height="auto">
        </div>
      </div>
    </div>
    
    <div class="product" >
      <button @click="turn_reco_togle(0)" class="product-item" >🔥Best Pick🔥</button>
      <button @click="turn_reco_togle(1)" class="product-item" >
        <div v-if="userStore.isLogin && is_fin" style="display: flex">
          <!-- 로그인ok 금융정보ok -->
          <span>Personalized for</span>&nbsp;
          <span class="mbtiButtonColor">{{ userStore.finInfoData.mbti}}</span>
        </div>
        <!-- 로그인안됨 혹은 금융정보 없음 -->
        <div v-else>MBTI</div>
      </button>
      <button @click="turn_reco_togle(2)" class="product-item" >❤️All in One❤️</button>
    </div>
    
    <div class="gift" v-if="userStore.isLogin && is_fin">
      <!-- 로그인ok 금융정보ok -->
      <div></div>
      <AgeRecommend v-if="reco_togle===0" :myCart="my_cart" @add-to-cart="addToCart"></AgeRecommend>
      <MbtiRecommend v-if="reco_togle===1" :myCart="my_cart" @add-to-cart="addToCart"></MbtiRecommend>
      <PrivateRecommend v-if="reco_togle===2" :myCart="my_cart" @add-to-cart="addToCart"></PrivateRecommend>
    </div>
    <div class="gift" v-else-if="!userStore.isLogin">
      <!-- 로그인 안한상태 -->
      <div>
        <button @click="pushToLogin" class="product-item">DOGEBANK의 상품 추천을 만나보세요</button>
        <p class="product-text">나이, MBTI, 나의 목표에 맞는 상품을 추천받아보세요.</p>
      </div>
      <div class="right-align_2">
        <img :src="dog2" alt="강아쥐"  width="25%;" height="auto" @click="pushToLogin">
      </div>
    </div>
    <div class="gift" v-else-if="userStore.isLogin && !is_fin">
      <!-- 금융정보 없음 -->
      <div>
        <button @click="pushToProfile" class="product-item">추천상품 보러가기</button>
        <p class="product-text">나이, MBTI, 나의 목표에 맞는 상품을 추천받아보세요.</p>
      </div>
      <div class="right-align_2">
        <img :src="dog2" alt="강아쥐"  width="25%;" height="auto" @click="pushToProfile">
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { useRouter ,useRoute, RouterLink , RouterView} from 'vue-router';
import { ref , onMounted ,watch , computed } from 'vue'
import AgeRecommend from '@/components/Recommend/AgeRecommend.vue'
import MbtiRecommend from '@/components/Recommend/MbtiRecommend.vue'
import PrivateRecommend from '@/components/Recommend/PrivateRecommend.vue'
import { useUserStore } from '@/stores/userStore';
import ResultRecommend from '@/components/Recommend/ResultRecommend.vue';
import mapImage from '@/assets/map.gif'; // 기본 이미지 경로 설정
import moneyImage from '@/assets/money.gif'; // 기본 이미지 경로 설정
import defaultProfileImage from '@/assets/profile.png';
import dog1 from '@/assets/dogicon1.png'
import dog2 from '@/assets/dogicon2.png'
import dog1ani from '@/assets/dogicon1_animation.gif'

const router = useRouter()
const userStore = useUserStore()

const pushToLogin = function(){
  router.push({name : 'login'})
}
const pushToProfile = function(){
  router.push({name : 'profile'})
}
const pushToExchange = function(){
  router.push({name : 'exchangerate'})
  console.log(import.meta.env.VITE_APP_API_URL)
  console.log(import.meta.env.VITE_APP_mapKey)
  console.log(import.meta.env.VITE_APP_restAPIKey)
}
const pushToMap = function(){
  router.push({name : 'bank'})
}

const reco_togle = ref(0)
const turn_reco_togle = function(t){
  reco_togle.value = t
  if (!userStore.isLogin){
    pushToLogin()
  }
}

const formatMoney = (amount) => {
  return Math.floor(amount).toLocaleString(); // 소수점 제거 및 천 단위 쉼표 추가
};


const is_fin = ref(false)
const is_finInfoData = function () {
  const user_finInfo = userStore.finInfoData;
  console.log(user_finInfo);
  if (Object.keys(user_finInfo).length === 0) {
    console.log("user_finInfo가 비어 있습니다. 데이터를 다시 불러옵니다.");
    userStore.getFinInfo(); // 데이터를 다시 불러오는 메서드 호출 (예: API 요청)
    return; // 함수 종료
  }


  const result = Object.values(user_finInfo).every(value => value !== null )
  console.log(is_fin.value);
  console.log(result);
  
  is_fin.value = result
  console.log(is_fin.value);
};


const my_cart = ref([])
function addToCart(product) {
  const productIndex = my_cart.value.findIndex(item => item.id === product.id)
  if (productIndex === -1) {
    // 상품이 없으면 추가
    my_cart.value.push(product)
  } else {
    // 상품이 있으면 제거
    my_cart.value.splice(productIndex, 1)
  }
}


const profileImageUrl = computed(() => {
  if (userStore.profileData.profile_img) {
    return `http://localhost:8000${userStore.profileData.profile_img}`
  } else {
    return defaultProfileImage
  }
});

onMounted(async ()=>{
  console.log("33");
  
  userStore.getProfile()
  userStore.getFinInfo()
  is_finInfoData()
})

</script>

<style scoped>
.container {
  width: 1200px;
  margin: 0 auto;
}

.no1box {
  display: flex;
}

.target, .submenu {
  display: flex;
  /* 세로로 가운데 정렬 */
  height: 400px; /* 높이를 동일하게 맞추기 위해 설정 */
}
.target {
  /* align-items: center;  */
  width: 65%;
  text-align: left; /* 글씨 왼쪽 정렬 */
}
.submenu {
  align-items: self-end; 
  width: 35%;
  text-align: left; /* 글씨 왼쪽 정렬 */
}


.target, .product, .gift {
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 10px;
}

.target, .gift {
  font-weight: bold;
  color: #9b4dca;
}

.custom-text {
  color: #979797;
  font-weight: lighter;
  margin-left: 10px;
  margin-top: 10px;
}

.submenu {
  display: flex;
  flex-direction: column;
  gap: 20px;
  
}

.gift {
  /* padding-bottom: 100px; */
  text-align: left;
}

.submenu-item {
  display: block; /* 세로로 배열되게 */
  /* border: 1px solid black; */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  padding: 10px;
  /* margin: 10px; */
  border-radius: 8px;
  height: 50%;
  width: 90%;
}
.submenu-top {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 90%;
}
.submenu-top-1 {
  /* display: block; */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  padding: 5px;
  margin-bottom: auto;
  /* margin: 10px; */
  border-radius: 8px;
  height: 70%;
  width: 100%;
}
.submenu-top-2 {
  margin-top: auto;
  /* margin: 10px; */
  height: 27%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap : 2rem;
}
.submenu-top-3 {
  flex: 1; /* 각 div가 균등하게 공간을 차지하도록 설정 */
  text-align: center; /* 가운데 정렬 */
  align-content: center;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;

}

.product-item {
  border: none;
  display: inline-block;
  padding: 5px 10px;
  background-color: #e0b0ff; /* 연한 보라색 */
  color: white;
  text-align: center;
  font-weight: bold;
  border-radius: 20px;
  text-decoration: none;
  box-shadow: 2px 2px 8px gray;
  transition: background-color 0.3s ease;
  margin: 5px;
}

.product {
  display: flex;
  justify-content: center;
  gap : 3rem;
}

.container > .target, .container > .submenu {
  display: inline-block;
  margin-right: 20px;
}

@keyframes gradientColor {
  0% {
    color: #FFF9BF; /* 초기 색상 FFF9BF*/
  }
  20% {
    color: #FDDBBB; /* 중간 색상 */
  }
  40% {
    color: #F0C1E1; /* 끝 색상 F0C1E1*/
  }
  60% {
    color: #FDDBBB; /* 중간 색상 */
  }
  80% {
    color: #FFF9BF; /* 끝 색상 */
  }
}

.mbtiButtonColor {
  animation: gradientColor 2s infinite ease-in-out; /* 3초마다 색상이 은은하게 변함 */
}

#resultchartbox {
    /* background-color: aqua; */
    display: flex;
    /* flex-direction: column; */
    
    justify-content: center;
    width: 100%; 
    height: 100%; 
    margin: 0;
    padding: 0;
    box-sizing: border-box; /* 패딩 포함 크기 계산 */
}

.hashtag {
  font-weight: bold;
  color: #9b4dca; /* 인스타그램 해시태그와 비슷한 파란색 */
  font-size: 16px;
  padding: 0px 8px;
  border-radius: 15px;
  background-color: #f4e1f7; /* 배경색을 연한 회색으로 설정 */
  margin-right: 4px;
  margin-bottom: 4px;
}
.profile-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd; /* 테두리 추가 */
  margin: 0 auto;
}

.hashtag-container {
    display: flex;
    justify-content: center;
    margin-bottom: 5px;
    text-align: center;
  }
.hashtag {
    margin: 0 3px; /* 태그 사이 간격 */
  }

.highlighted {
  color: #9b4dca; /* 보라색 */
  font-weight: bold; /* 굵게 */
}

.right-align {
  float: right; /* 오른쪽 정렬 */
  margin-left: 5px; /* 텍스트와의 간격 */
  margin-right: 10px;
}

.right-align_1 {
  float: right; /* 오른쪽 정렬 */
  margin-left: 5px; /* 텍스트와의 간격 */
  margin-right: 3px;
}

.right-align_2 {
  /* background-color: #9b4dca; */
  display: flex;
  justify-content: end;
}


.product-text {
  font-weight: lighter;
  color: #979797;
  margin-left: 10px;
  margin-top: 10px;
}

.title {
  font-family: 'Godo', sans-serif;
  font-weight: bold;
}

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}

/* 마우스 커서가 포인터로 바뀌도록 스타일 추가 */
.hover-effect {
  cursor: pointer; /* 클릭 가능한 영역 표시 */
}

</style>
