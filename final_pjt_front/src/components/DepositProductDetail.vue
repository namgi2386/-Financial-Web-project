<template>
  <div class="card-overlay" @click.self="closeCard">
    <div class="card">
      <div id="head01">
        <span>
          <img :src="bankimg()" alt="은행 사진" class="profile-preview" />
        </span>
        <span>
          <h3 class="text-center mb-4"><strong>{{ product.fin_prdt_nm }}</strong></h3>
        </span>
      </div>
      <p><strong>해당은행:</strong> {{ product.kor_co_nm }}</p>
      <!-- <img src="@/assets/profile.png" alt="은행 사진" class="profile-preview" /> -->
      <!-- {{ bankimg }} -->

      <p><strong>공시시작일:</strong> {{ product.dcls_strt_day }}</p>
      <p v-if="product.dcls_end_day"><strong>공시종료일:</strong> {{ product.dcls_end_day }}</p>
      <p><strong>가입방법:</strong> {{ product.join_way }}</p>
      <p><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
      <p><strong>만기 후 이자율:</strong> {{ product.mtrt_int }}</p>
      <p><strong>기타 유의사항:</strong> {{ product.etc_note }}</p>
      <div class="button-container">
        <button class="save-button" @click="saveProduct">찜</button>
        <button class="like-button" @click="likeProduct" :class="{ 'liked': isLiked }">
          <i class="fas fa-heart" :style="{ color: isLiked ? 'red' : 'white' }"></i> 좋아요 ({{ loveCount }})
        </button>
      </div>
      <hr>
      <CharDeposit :product="product"></CharDeposit>
      <p @click="closeCard" id="close" class=text-center><strong>[닫기]</strong></p>
    </div>
  </div>
</template>

<script setup>
import { useDepositStore } from '@/stores/deposit';
import { ref, onMounted , computed} from 'vue';
import axios from 'axios';
import CharDeposit from './CharDeposit.vue';




const depositStore = useDepositStore()

const props = defineProps({
  product: Object,
});
const emit = defineEmits(['close']);

const loveCount = ref(props.product.love_count);
const isLiked = ref(false); // 좋아요 여부
const isJjim = ref(false) // 찜 여부


const getMyLoveProducts = async function() {
  try {
    const token = localStorage.getItem('token');

    const lovedProductsResponse = await axios({
      method: 'get',
      url: `http://localhost:8000/liked-products/deposit/`,
      headers: { Authorization: `Token ${token}` },
    });
    const lovedProducts = lovedProductsResponse.data;
    isLiked.value = lovedProducts.some(product => product.id === props.product.id);
    loveCount.value = await getpropslovecount();
  } catch (error) {
    console.error('사용자가 좋아요한 상품을 가져오는 데 실패했습니다:', error);
  }
};

const getpropslovecount = async function() {
  try {
    const token = localStorage.getItem('token');
    const response = await axios({
      method: 'get',
      url: `http://localhost:8000/product-likes/deposit/${props.product.fin_prdt_cd}/`,
      headers: { Authorization: `Token ${token}` },
    });
    return response.data.love_count;
  } catch (error) {
    console.error('좋아요 수를 가져오는 데 실패했습니다:', error);
  }
};

const likeProduct = function(){
  const token = localStorage.getItem('token');
  axios({
    method : 'get',
    url : `http://localhost:8000/product-likes/deposit/${props.product.fin_prdt_cd}/`,
    headers: {Authorization: `Token ${token}`},
  }).then(async(response) => {
    const togg = await depositStore.toggleLove(props.product.fin_prdt_cd)
    console.log(togg.data);
    console.log(togg.data.love_count);
    loveCount.value = togg.data.love_count;
    isLiked.value = !isLiked.value;
  })
  .catch(err => console.log(err)
  )
}

// 찜 상태 가져오기
const getMyJjimProducts = async function() {
  try {
    const token = localStorage.getItem('token');

    const jjimProductsResponse = await axios({
      method: 'get',
      url: `http://localhost:8000/liked-products/deposit/`,
      headers: { Authorization: `Token ${token}` },
    });
    isJjim.value = jjimProductsResponse.data.some(product => product.id === props.product.id);
  } catch (error) {
    console.error('사용자가 찜한 상품을 가져오는 데 실패했습니다:', error);
  }
};

// 찜 버튼 클릭 시 처리
const saveProduct = async function () {
  // // 찜 상태를 서버에서 다시 확인
  // await getMyJjimProducts();

  if (isJjim.value) {
    swal("이미 찜한 상품입니다!", {
      icon: "warning",
    });
    return;
  }

  // const isConfirmed = confirm('상품을 찜! 하시겠습니까?');

  swal({
    title: "상품을 찜하시겠습니까?",
    icon: "info",
    buttons: ["취소", "확인"],
  }).then(async (willSave) => {
    if (willSave) {
      if (isJjim.value) {
        // 찜 취소
        await depositStore.unjjim_deposit(props.product.fin_prdt_cd);
      } else {
        // 찜 추가
        await depositStore.jjim_deposit(props.product.fin_prdt_cd);
      }
      isJjim.value = !isJjim.value;

      // 찜 상태 업데이트 메시지
      swal("상품이 프로필에 저장되었습니다!", {
        icon: "success",
      });
    }
  });
};


const removeBankNameList = ['주식회사', '뱅크', '저축', '은행'];

const cleanedName = function() {
  let name = props.product.kor_co_nm;
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
function bankimg() {
  const rrname = cleanedName()
  return new URL(`/src/assets/banklogo/${rrname}.png`, import.meta.url).href
}

// 상세페이지를 다시 열었을 때 상태 업데이트
onMounted(() => {
  getMyJjimProducts(); // 찜 상태 확인
  getMyLoveProducts(); // 좋아요 상태 확인
});

// 상세페이지 닫기 함수
const closeCard = () => {
  emit('close'); // 부모 컴포넌트에 'close' 이벤트를 전달하여 상세페이지 닫기
};
</script>

<style scoped>
.card-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  text-align: left;
  max-height: 80vh; /* 최대 높이를 80%로 설정 */
  overflow-y: auto; /* 내용이 많으면 세로 스크롤이 나타나도록 설정 */
}

.card::-webkit-scrollbar {
  display: none; /* 스크롤 바 숨기기 */
}

.button-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px; /* 버튼 사이 간격 */
}

.save-button,
.like-button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button {
  background-color: #6f42c1; /* 보라색 */
  color: white;
  border: none;
}

.save-button:hover {
  background-color: #5a34b2;
}

/* 좋아요 버튼 스타일 */
.like-button {
  background-color: #ff4081; /* 기본 핑크색 */
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.like-button.liked {
  background-color: #e33b6f; /* 좋아요가 눌린 상태 */
}

.like-button:hover {
  background-color: #e33b6f; /* 더 어두운 핑크색 */
}

.like-button i {
  margin-right: 8px; /* 아이콘과 글자 간의 간격 */
  font-size: 18px; /* 하트 아이콘 크기 조정 */
}

#close {
  cursor: pointer; /* 마우스 포인터로 변경 */
  transition: color 0.3s; /* 색상 전환 효과 추가 */
  margin-top: 2px;
}

#close :hover {
  color: #6f42c1; /* 보라색으로 변경 */
}

.profile-preview {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  /* border: 2px solid #ddd; */
   /* 테두리 추가 */
  margin: 0 auto;
}

#head01 {
display: flex;
justify-content: center;
gap: 10px;
}


</style>
