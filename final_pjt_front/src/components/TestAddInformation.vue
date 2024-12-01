<template>
  <div class="card-overlay">
    <div class="card">
      <h3 class="text-center title"><strong>금융 정보 추가</strong></h3>
      <form @submit.prevent="submitForm">

        <div class="form-row">
          <div class="form-group">
            <label for="job">직업</label>
            <input v-model="formData.job" type="text" id="job" placeholder="직업을 입력하세요" />
          </div>
          <div class="form-group">
            <label for="monthly_income">월 소득</label>
            <input v-model="formData.monthly_income" type="number" id="monthly_income" placeholder="월 소득" />
          </div>
          <div class="form-group">
            <label for="annual_income">연 소득</label>
            <input v-model="formData.annual_income" type="number" id="annual_income" placeholder="연 소득" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="current_assets">현재 자산</label>
            <input v-model="formData.current_assets" type="number" id="current_assets" placeholder="현재 자산" />
          </div>
          <div class="form-group">
            <label for="monthly_savings">월별 저축</label>
            <input v-model="formData.monthly_savings" type="number" id="monthly_savings" placeholder="월별 저축" />
          </div>
          <div class="form-group">
            <label for="fixed_expenses">고정 지출</label>
            <input v-model="formData.fixed_expenses" type="number" id="fixed_expenses" placeholder="고정 지출" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="variable_expenses">변동 지출</label>
            <input v-model="formData.variable_expenses" type="number" id="variable_expenses" placeholder="변동 지출" />
          </div>
          <div class="form-group">
            <label for="goal_amount">목표 금액</label>
            <input v-model="formData.goal_amount" type="number" id="goal_amount" placeholder="목표 금액" />
          </div>
          <div class="form-group">
            <label for="goal_date">목표 시점까지의 개월 수</label>
            <input v-model="formData.goal_date" type="number" id="goal_date" placeholder="목표 시점까지의 개월 수" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
          <label for="goalType">목표 유형</label>
          <select id="goalType" v-model="formData.goal_type" class="form-control">
            <option value="" disabled>선택하세요</option>
            <option value="주택">주택</option>
            <option value="목돈">목돈</option>
            <option value="결혼">결혼</option>
            <option value="자녀">자녀</option>
          </select>
        </div>
        

          <div class="form-group">
            <label for="mbti">MBTI</label>
            <select id="mbti" v-model="formData.mbti" class="form-control">
              <option value="" disabled>선택하세요</option>
              <option value="ISTJ">ISTJ</option>
              <option value="ISTP">ISTP</option>
              <option value="ISFJ">ISFJ</option>
              <option value="ISFP">ISFP</option>
              <option value="INTJ">INTJ</option>
              <option value="INTP">INTP</option>
              <option value="INFJ">INFJ</option>
              <option value="INFP">INFP</option>
              <option value="ESTJ">ESTJ</option>
              <option value="ESTP">ESTP</option>
              <option value="ESFJ">ESFJ</option>
              <option value="ESFP">ESFP</option>
              <option value="ENTJ">ENTJ</option>
              <option value="ENTP">ENTP</option>
              <option value="ENFJ">ENFJ</option>
              <option value="ENFP">ENFP</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="preference_type">선호사항</label>
            <input v-model="formData.preference_type" type="text" id="preference_type" placeholder="예: 고금리 선호" />
          </div>
          <div class="form-group">
          <label for="prefers_stability">안정성 선호</label>
          <input v-model="formData.prefers_stability" type="checkbox" id="prefers_stability" />
        </div>
        </div>
        
        <div class="form-actions">
          <button type="submit"><strong>[저장]</strong></button>
          <button type="button" @click="closeModal"><strong>[닫기]</strong></button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref ,defineEmits , onMounted, computed } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/userStore";
import swal from "sweetalert";

const emit = defineEmits(['close']);
const userStore = useUserStore()

//parseInt(Number(data.money)/1000)

const formData = computed(() => ({
  job: userStore.finInfoData.job,
  monthly_income: parseInt(Number(userStore.finInfoData.monthly_income)/10000),
  annual_income: parseInt(Number(userStore.finInfoData.annual_income)/10000),
  current_assets: parseInt(Number(userStore.finInfoData.current_assets)/10000),
  monthly_savings: parseInt(Number(userStore.finInfoData.monthly_savings)/10000),
  fixed_expenses: parseInt(Number(userStore.finInfoData.fixed_expenses)/10000),
  variable_expenses: parseInt(Number(userStore.finInfoData.variable_expenses)/10000),
  goal_type: userStore.finInfoData.goal_type,
  goal_amount: parseInt(Number(userStore.finInfoData.goal_amount)/10000),
  goal_date: userStore.finInfoData.goal_date,
  prefers_stability: userStore.finInfoData.prefers_stability,
  preference_type: userStore.finInfoData.preference_type,
  mbti: userStore.finInfoData.mbti,
}));


const submitForm = () => {
  const token = localStorage.getItem("token");
  const formDataValues = formData.value
  const axiosformData = new FormData()
  axiosformData.append('job',formDataValues.job);
  axiosformData.append('monthly_income', parseInt(Number(formDataValues.monthly_income)*10000));
  axiosformData.append('annual_income', parseInt(Number(formDataValues.annual_income)*10000));
  axiosformData.append('current_assets', parseInt(Number(formDataValues.current_assets)*10000));
  axiosformData.append('monthly_savings', parseInt(Number(formDataValues.monthly_savings)*10000));
  axiosformData.append('fixed_expenses', parseInt(Number(formDataValues.fixed_expenses)*10000));
  axiosformData.append('variable_expenses', parseInt(Number(formDataValues.variable_expenses)*10000));
  axiosformData.append('goal_type', formDataValues.goal_type);
  axiosformData.append('goal_amount', parseInt(Number(formDataValues.goal_amount)*10000));
  axiosformData.append('goal_date', formDataValues.goal_date);
  axiosformData.append('prefers_stability', formDataValues.prefers_stability);
  axiosformData.append('preference_type', formDataValues.preference_type);
  axiosformData.append('mbti',formDataValues.mbti );
  console.log(axiosformData);
  
  axios
    .put("http://localhost:8000/accounts/fininfo/", axiosformData, {
      headers: { Authorization: `Token ${token}` },
    })
    .then(() => {
      swal({
        title: '금융 정보가 저장되었습니다.',
        icon: 'success',
        imageUrl: `http://localhost:8000/vueimage/profile.png`, // 이미지 추가
        imageWidth: 100,
        imageHeight: 100,
        imageAlt: "Custom Image",  // 이미지 설명
        showConfirmButton: false,
      });
      userStore.getFinInfo(); // 저장 후 최신 데이터 가져오기
      closeModal();
    })
    .catch((err) => {
      swal({
        icon: 'error',
        title: '금융 정보를 저장하는 데 실패했습니다.',
        text: '잠시 후 다시 시도해주세요.',
      });
    });
};

const closeModal = () => {
  console.log('ttt');
  emit("close");

};

onMounted(() => {
  userStore.getFinInfo();
});

// return { formData, submitForm, closeModal };

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
  overflow: hidden; /* 화면 스크롤 숨김 */
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  text-align: center;
  overflow-y: auto; /* 내부 스크롤 유지 */
  scrollbar-width: none; /* Firefox용 스크롤 숨기기 */
  -ms-overflow-style: none; /* IE 및 Edge용 스크롤 숨기기 */
}

.card::-webkit-scrollbar {
  display: none; /* Chrome, Safari용 스크롤 숨기기 */
}

.card h3 {
  color: #5a32a3; /* 어두운 텍스트 */
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
  justify-content: space-between; /* 행 내 요소 가운데 정렬 */
}

.form-group {
  flex: 1;
  min-width: 0; 
  /* 최소 너비 제거 */
  text-align: center; 
  /* 글씨 가운데 정렬 */
  min-width: calc(33.33% - 13.33px); 
  /* 한 줄에 3개씩 배치 */
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold; 
  /* 라벨 가독성을 위해 강조 */
  
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #495057;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #6f42c1;
  box-shadow: 0 0 4px rgba(111, 66, 193, 0.2);
}

.form-actions {
  margin-top: 25px;
  text-align: center;
}

/* 버튼 스타일 수정 */
button {
  padding: 12px 25px;
  margin: 0 10px;
  border: none;
  cursor: pointer;
  background-color: transparent; /* 배경 투명화 */
  color: #6f42c1; /* 글자색 보라색 */
  font-size: 1rem;
  border-radius: 8px;
  transition: color 0.3s ease, transform 0.2s ease;
  font-size: 18px;
  font-weight: bold;
}

button:hover {
  color: #5a34b2; /* 글자 호버 시 더 어두운 보라색 */
}

button:active {
  color: #4c2d99; /* 클릭 시 더 어두운 색 */
  transform: translateY(0);
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
</style>
