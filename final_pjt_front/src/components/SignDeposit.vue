<!-- DepositProductDetail.vue -->
<template>
    <div class="card-overlay" @click.self="closeCard">
      <div class="card">
        <h3 class="text-center mb-4">{{ product.fin_prdt_nm }}</h3>
        <p><strong>해당은행:</strong> {{ product.kor_co_nm }}</p>
        <p><strong>공시시작일:</strong> {{ product.dcls_strt_day }}</p>
        <p><strong>가입방법:</strong> {{ product.join_way }}</p>
        <p><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
        <p><strong>만기 후 이자율:</strong> {{ product.mtrt_int }}</p>
        <p><strong>기타 유의사항:</strong> {{ product.etc_note }}</p>
        <hr>
        <CharDeposit :product="product"></CharDeposit>
        <p @click="closeCard" id="close" class=text-center><strong>[닫기]</strong></p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useDepositStore } from '@/stores/deposit';
  import CharDeposit from './CharDeposit.vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const product = JSON.parse(route.query.product);


  const emit = defineEmits(['close']);

  
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
  </style>
  