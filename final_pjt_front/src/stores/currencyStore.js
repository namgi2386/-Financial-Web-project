import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

export const useCurrencyStore = defineStore('currency', () => {
  const curName = ref({}) // 국가이름
  const currencyInfo = ref({}); // 환율 정보
  const BASE_URL = 'http://localhost:8000'

  // 최신 환율 정보를 가져오는 함수
  const getcurrencyInfo = () => {
    axios({
      url: `${BASE_URL}/exchange_rate/`,
      method: 'GET',
    })
    .then(response => {
      // console.log(response.data)
      currencyInfo.value = response.data.response
      curName.value = response.data.response.map(item => item.cur_nm)
      console.log(curName.value)
      console.log(currencyInfo.value)
    })
    .catch(error => {
      console.error('환율 정보를 가져오는 데 실패했습니다:', error);
    });
  };

  
  return {
    currencyInfo,
    getcurrencyInfo,
    curName,
    BASE_URL
  };
});
