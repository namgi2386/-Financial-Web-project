<template>
  <div class="container">
    <h1 class="text-center title"></h1>
    <div class="profile-container">
      <!-- 사용자 정보 -->
      <div class="profile-info">
        <div class="mb-3 text-center">
          <img :src="profileImageUrl" alt="프로필 사진" class="profile-preview" />
        </div>
        <div class="info-group">
          <h5 class="mb-3"><strong style="font-size: 23px; color: #6f42c1;">{{ userStore.profileData.nickname }}</strong>님 (만{{ userStore.profileData.age }}세)</h5>
          <h5 v-if="!userStore.finInfoData.current_assets"><strong>재산</strong>: {{ formatMoney(userStore.profileData.money) }}원</h5>
          <h5><strong>재산</strong>: {{ formatMoney(userStore.finInfoData.current_assets) }}원</h5>
          <h5><strong>희망 가입 기간</strong>: {{ userStore.profileData.desiredSubscriptionPeriod }}개월</h5>
          <h5><strong>주거래 은행</strong>: {{ userStore.profileData.mainBank }}</h5>
          <div class="inline-info">
            <h5><strong>MBTI</strong>: {{ userStore.finInfoData.mbti }}</h5>
            <h5><strong>목표 금액</strong>: {{ formatMoney(userStore.finInfoData.goal_amount) }}원</h5>
          </div>
        </div>
        <div>
          <button @click="temp_show" class="insta-button m-2">금융정보추가</button>
          <TestAddInformation v-if="showModal" @close=temp_unshow />
          <button @click="goUpdateSignup" class="insta-button">회원정보수정</button>
        </div>
        <div>
          <button class="delete-button" @click="delUser">회원탈퇴</button>
        </div>
      </div>

      <!-- 찜한 상품 -->
      <div class="jjim-container">
        <div class="jjim-list">
          <h2 class="title">찜한 예금 상품</h2>
          <div v-if="myjjimData.length > 0" class="product-list">
            <div v-for="product in myjjimData" :key="product.id" class="product-item hover-effect" >
              <span>
                <img :src="bankimg(product)" alt="은행 사진" class="profile-preview-bankimg" />
                <h4>{{ product.fin_prdt_nm }}</h4> 
              </span>
              <p><strong>해당은행:</strong> {{ product.kor_co_nm }}</p>
              <p><strong>상품설명:</strong> {{ product.etc_note }}</p>
              <p><strong>만기후 이자율:</strong> {{ product.mtrt_int }}</p>
              <button @click="confirmRemoveFromJjim(product.fin_prdt_cd)">찜 취소</button>
            </div>
          </div>
          <p v-else>찜한 상품이 없습니다.</p>
        </div>

        <div class="jjim-list">
          <h2 class="title">찜한 적금 상품</h2>
          <div v-if="saving_myjjimData.length > 0" class="product-list">
            <div v-for="product in saving_myjjimData" :key="product.id" class="product-item hover-effect">
              <img :src="bankimg(product)" alt="은행 사진" class="profile-preview-bankimg" />
              <h4>{{ product.fin_prdt_nm }}</h4>
              <p><strong>해당은행:</strong> {{ product.kor_co_nm }}</p>
              <p><strong>상품설명:</strong> {{ product.etc_note }}</p>
              <p><strong>만기후 이자율:</strong> {{ product.mtrt_int }}</p>
              <button @click="confirmRemoveFromJjim_saving(product.fin_prdt_cd)">찜 취소</button>
            </div>
          </div>
          <p v-else>찜한 상품이 없습니다.</p>
          
        </div>
      </div>
    </div>

  </div>
  
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from "@/stores/userStore.js";
import { useDepositStore } from '@/stores/deposit';
import { useSavingStore } from '@/stores/saving';
import { useRouter } from 'vue-router';
import defaultProfileImage from '@/assets/profile.png'; // 기본 이미지 경로 설정
import axios from 'axios';
import TestAddInformation from '@/components/TestAddInformation.vue';
import swal from 'sweetalert'; // sweetalert을 임포트합니다.


const depositStore = useDepositStore();
const savingStore = useSavingStore()
const userStore = useUserStore();
const myjjimData = ref([]) // deposit
const saving_myjjimData = ref([])
const router = useRouter()


// 금융정보추가 변수
const showModal = ref(false);
const temp_show = function(){
  console.log('eee');
  showModal.value = true
}
const temp_unshow = function(){
  console.log('uneee');
  showModal.value = false
}

const goUpdateSignup = () => {
  router.push('/updatesignup');
};

// 숫자를 천 단위로 쉼표를 추가하고 소수점 제거
const formatMoney = (amount) => {
  return Math.floor(amount).toLocaleString(); // 소수점 제거 및 천 단위 쉼표 추가
};


// 찜 취소 확인 후 실행하는 함수
const confirmRemoveFromJjim = function(finPrdtCd) {
  swal({
    title: "상품을 삭제하시겠습니까?", 
    icon: "warning", // 경고 아이콘 표시
    buttons: ["취소", "삭제"], // 취소, 삭제 버튼 표시
    dangerMode: true, // 삭제 버튼을 빨간색으로 강조
  }).then((willDelete) => {
    if (willDelete) {
      removeFromJjim(finPrdtCd); // 확인 시 상품 삭제 실행
      swal("삭제되었습니다.", {
        icon: "success", // 성공 아이콘 표시
        button: "확인",
      });
    }
  });
};

const confirmRemoveFromJjim_saving = function(finPrdtCd) {
  swal({
    title: "상품을 삭제하시겠습니까?", 
    icon: "warning", // 경고 아이콘 표시
    buttons: ["취소", "삭제"], // 취소, 삭제 버튼 표시
    dangerMode: true, // 삭제 버튼을 빨간색으로 강조
  }).then((willDelete) => {
    if (willDelete) {
      removeFromJjim_saving(finPrdtCd); // 확인 시 상품 삭제 실행
      swal("삭제되었습니다.", {
        icon: "success", // 성공 아이콘 표시
        button: "확인",
      });
    }
  });
};


// 찜 취소 기능 (deposit)
const removeFromJjim = function(finPrdtCd) {
  // API 호출을 통해 서버에서 찜 삭제
  depositStore.unjjim_deposit(finPrdtCd);
  
  // 화면에서 해당 상품 제거
  myjjimData.value = myjjimData.value.filter(product => product.fin_prdt_cd !== finPrdtCd);
};

// 찜 취소 기능 (saving)
const removeFromJjim_saving = function(finPrdtCd) {
  // API 호출을 통해 서버에서 찜 삭제
  savingStore.unjjim_saving(finPrdtCd);
  
  // 화면에서 해당 상품 제거
  saving_myjjimData.value = saving_myjjimData.value.filter(product => product.fin_prdt_cd !== finPrdtCd);
};


// 찜조회 jjimcheck_deposit()를 onMount해서 먼저 가져와놓기 이후 depositStore.myjjimData 로 보여주면 됨

const jjimcheck_deposit = function(){
  const token = localStorage.getItem('token');
  axios({
    method : 'GET',
    url : 'http://localhost:8000/get_liked_products/deposit/',
    headers: {Authorization: `Token ${token}`}
  }).then((res)=>{
    console.log(res.data);
    myjjimData.value = res.data.sort((a, b) => {
        // 여기서 정렬 기준을 설정합니다. 
        // 아래는 기본적으로 배열의 역순 정렬 (a와 b의 순서를 반대로)
        return b.id - a.id; // 예: `id` 속성을 기준으로 역순 정렬
      });
  }).catch(err => console.log(err)
)}

const jjimcheck_saving = function(){
  const token = localStorage.getItem('token');
  axios({
    method : 'GET',
    url : 'http://localhost:8000/get_liked_products/saving/',
    headers: {Authorization: `Token ${token}`}
  }).then((res)=>{
    console.log(res.data);
    saving_myjjimData.value = res.data.sort((a, b) => {
        // 여기서 정렬 기준을 설정합니다. 
        // 아래는 기본적으로 배열의 역순 정렬 (a와 b의 순서를 반대로)
        return b.id - a.id; // 예: `id` 속성을 기준으로 역순 정렬
      });
  }).catch(err => console.log(err)
)}


const locusername = localStorage.getItem('locusername');
const delUser = function () {
  swal({
    title: "어디가?",
    text: "나는?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then( res => {
    if (res) {
      swal("ㅠㅠ", {
        icon: "success",
      });
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/accounts/delete/${locusername}/`,
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      })
        .then((ress) => {
          console.log(ress.data);
          userStore.logOut()
        })
        .catch(err => console.log(err))
    } else {
      swal("헿");
    }
  });
};

const removeBankNameList = ['주식회사', '뱅크', '저축', '은행'];

const cleanedName = function(product) {
  let name = product.kor_co_nm;
  if (name.includes('저축')) {
    return '저축';
  }
  if (name.includes('아이엠')) {
    return '대구';
  }
  if (name.includes('한국스탠다드차타드')) {
    return '제일';
  }
  removeBankNameList.forEach(str => {
    const regex = new RegExp(str, 'g');
    name = name.replace(regex, '');
  });
  return name.trim();
};
function bankimg(product) {
  const rrname = cleanedName(product)
  return new URL(`/src/assets/banklogo/${rrname}.png`, import.meta.url).href
}



// 컴포넌트가 마운트될 때 찜한 상품 목록 가져오기
onMounted(() => {
  userStore.getProfile();
  jjimcheck_saving();
  jjimcheck_deposit();
});


// 프로필 이미지 URL, 값이 없을 경우 기본 이미지 사용
const profileImageUrl = computed(() => {
  if (userStore.profileData.profile_img) {
    return `http://localhost:8000${userStore.profileData.profile_img}`
  } else {
    return defaultProfileImage
  }
});

</script>

<style scoped>
/* 프로필 이미지 스타일 */
.profile-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd; /* 테두리 추가 */
  margin: 0 auto;
}

/* 프로필 컨테이너 레이아웃 */
.profile-container {
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  align-items: center; /* 중앙 정렬 */
  gap: 20px;
  margin: 0 auto;
  max-width: 750px;
}

/* 사용자 정보 카드 스타일 */
.profile-info {
  text-align: center;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  width: 100%;
}

/* 텍스트 스타일 */
.info-group h5 {
  margin: 10px 0;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

/* 찜한 상품 그리드 레이아웃 */
.jjim-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  width: 100%;
}

/* 찜한 상품들 사이 간격 추가 */
.product-item {
  border: 1px solid #ddd; /* 상품 테두리 */
  padding: 15px; /* 상품 아이템 내부 여백 */
  margin-bottom: 20px; /* 상품 간 간격 */
  border-radius: 10px; /* 상품 아이템 모서리 둥글게 */
  transition: transform 0.2s ease; /* 상품 hover 시 확대 효과 */
  text-align: center; /* 글씨 중앙 정렬 */
}

.product-item:hover {
  border-color: #6f42c1; /* 보라색 테두리 */
  background-color: #f9f9f9; /* 선택적으로 배경색 추가 */
}

.product-item:hover {
  transform: translateY(-5px); /* 마우스를 올리면 약간 위로 떠오르는 효과 */
}

/* 상품 정보 텍스트 */
.product-item h4 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.product-item p {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

/* 버튼 스타일 */
.product-item button {
  background-color: #6f42c1; /* 보라색 배경 */
  color: white; /* 흰색 글씨 */
  padding: 8px 16px; /* 버튼 크기 조정 */
  border: none; /* 테두리 제거 */
  cursor: pointer;
  font-size: 14px;
  border-radius: 5px; /* 버튼 모서리 둥글게 */
  transition: background-color 0.3s ease; /* 배경 색상 전환 효과 */
}

.product-item button:hover {
  background-color: #5a34b2; /* 호버 시 진한 보라색 */
}

/* 헤더 스타일 */
h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
  text-align: center;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .profile-container {
    padding: 0 15px;
  }

  .jjim-container {
    grid-template-columns: 1fr;
  }
}

.button-group {
  display: flex;
  justify-content: center;
  margin: 20px;
}

.insta-button {
  background-color: #d4a5f7; /* 연한 보라색 배경 */
  border: none;
  color: white; /* 글씨 색상 흰색 */
  padding: 5px 10px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 30px; /* 둥근 버튼 모양 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s, box-shadow 0.2s;
}

.insta-button:hover {
  background-color: #c38bf4; /* 조금 더 진한 보라색으로 변경 */
  transform: scale(1.05); /* 살짝 확대 효과 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.insta-button:active {
  transform: scale(0.95); /* 눌렀을 때 살짝 줄어듦 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.delete-button {
  background: none; /* 배경 제거 */
  border: none; /* 테두리 제거 */
  color: #6f42c1; /* 진한 보라색 글씨 */
  font-size: 16px;
  font-weight: bold;
  text-decoration: underline; /* 밑줄 추가 */
  cursor: pointer;
  padding: 5px 10px;
}

.delete-button:hover {
  text-decoration: none; /* 호버 시 밑줄 제거 */
  color: #5a34b2; /* 더 진한 보라색으로 변경 */
}

/* 찜한 상품 제목 스타일 */
.jjim-list h2 {
  color: #6f42c1; /* 보라색 */
  font-weight: bold; /* 글씨 굵게 */
  margin-bottom: 10px; /* 아래 간격 추가 */
}

.product-item strong {
  color: #5a34b2; /* 보라색으로 변경 */
}
.profile-preview-bankimg {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  /* border: 2px solid #ddd; */
   /* 테두리 추가 */
  margin-bottom: 3px;
}

.title {
  font-family: 'Godo', sans-serif;
}

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}

.inline-info {
  display: flex;
  justify-content: center;
  gap: 10px; /* 두 항목 간 간격 */
  margin-bottom: 10px;
}

.inline-info h5 {
  margin: 0; /* 간격 없애기 */
}
</style>
