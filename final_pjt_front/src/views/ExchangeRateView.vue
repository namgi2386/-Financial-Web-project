<template>
  <div class="container">
    <h1 class="title">환율 계산기</h1>
    <form @submit.prevent>
      <div class="form-group">
        <label for="state">기준</label>
        <select id="state" v-model="state">
          <option class="placeholder" disabled value="">기준을 선택해주세요.</option> <!-- 기본 옵션 추가 -->
          <option v-for="item in states" :key="item" :value="item">
            {{ item }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="country">통화 선택</label>
        <select id="country" v-model="country">
          <option class="placeholder" value="">통화를 선택해주세요.</option> <!-- 기본 옵션 추가 -->
          <option v-for="item in currencyStore.curName" :key="item" :value="item">
            {{ item }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="amount">금액 입력</label>
        <input
          id="amount"
          type="text"
          v-model="exchangeBefore"
          :placeholder="`₩`"
        />
      </div>
      <div class="result">
        <p v-if="typeof exchangeAfter === 'number'">
          환전 결과는 <strong>{{ formattedExchangeAfter }} {{ exchangeDetail.cur_unit }}</strong> 입니다.
        </p>
        <p v-else>{{ exchangeAfter }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useCurrencyStore } from "@/stores/currencyStore";

const currencyStore = useCurrencyStore()

const states = ["송금 받을 때", "송금 보낼 때", "매매 기준율"];
const state = ref("");
const country = ref("");
const exchangeDetail = ref({});
const exchangeBefore = ref("");
const exchangeAfter = ref("");

const formattedExchangeAfter = computed(() => {
  return new Intl.NumberFormat("ko-KR").format(Math.round(exchangeAfter.value));
});

const updateExchangeDetail = () => {
  exchangeDetail.value =
    currencyStore.currencyInfo.find((item) => item.cur_nm === country.value) || {};
  calculateExchange();
};

const calculateExchange = () => {
  if (state.value === "송금 받을 때" && exchangeDetail.value.ttb) {
    // 원화를 선택한 나라의 화폐로 변환
    exchangeAfter.value =
      Number(exchangeBefore.value) / 
      Number(exchangeDetail.value.ttb.replace(",", ""));
  } else if (state.value === "송금 보낼 때" && exchangeDetail.value.tts) {
    exchangeAfter.value =
      Number(exchangeBefore.value) /
      Number(exchangeDetail.value.tts.replace(",", ""));
  } else if (state.value === "매매 기준율" && exchangeDetail.value.deal_bas_r) {
    exchangeAfter.value =
      Number(exchangeBefore.value) /
      Number(exchangeDetail.value.deal_bas_r.replace(",", ""));
  } else if (!(state.value && country.value && exchangeBefore.value)) {
    exchangeAfter.value = "통화를 선택해주세요.";
  }
};

watch([state , country], updateExchangeDetail);
watch(exchangeBefore, calculateExchange);

onMounted(() => {
  currencyStore.getcurrencyInfo();
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 제목 스타일 */
.title {
  color: #333;
  font-weight: bold;
  margin-bottom: 20px;
  letter-spacing: -0.5px;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* 라벨 스타일 */
label {
  font-weight: bold;
  color: #6f42c1;
  margin-bottom: 8px;
  font-size: 1rem;
  margin-left: 140px;
}

/* 선택, 입력 필드 스타일 */
select, input {
  width: 60%;
  padding: 12px 15px;
  font-size: 1rem;
  margin-top: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f7f7f7;
  transition: background-color 0.3s ease;
  margin-left: auto; /* 왼쪽 여백 제거 */
  margin-right: auto; /* 오른쪽 여백 제거 */
}

select:focus, input:focus {
  border-color: #6f42c1;
  background-color: #fff;
}

/* 결과 영역 스타일 */
.result {
  margin-top: 20px;
  font-size: 1.1rem;
  color: #333;
}

strong {
  color: #6f42c1;
  font-weight: bold;
}

/* 결과가 없는 경우 메시지 스타일 */
.result p {
  color: #999;
  font-size: 1rem;
}

/* 반응형 디자인 */
@media (max-width: 600px) {
  .container {
    max-width: 90%;
    padding: 15px;
  }

  .title {
    font-size: 1.8rem;
  }

  .form-group {
    margin-bottom: 15px;
  }

  select, input {
    padding: 10px 12px;
  }
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

.placeholder {
  color: #979797; /* 원하는 색상으로 변경 */
}
</style>
