// deposit.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import { useUserStore } from './userStore';

export const useDepositStore = defineStore('deposit', () => {
  const userStore = useUserStore()
  const BASE_URL = "http://localhost:8000/finlife"
  const depositProductsData = ref([])  //deposit상품전체
  const DepositDetail = ref([]) // 특정 상품의 상세정보
  const DepositOptions = ref({}) // 특정 상품의 옵션들

  // 상품목록 불러오는 함수
  const getDepositData = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/deposit/products/`, {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      });
      console.log(response.data);
      
      depositProductsData.value = response.data;
      console.log(depositProductsData.value);
    } catch (error) {
      console.error("상품 데이터 로드 실패:", error);
    }
  };

  // 특정 상품의 상세 정보를 불러오는 함수
  const getDepositDetail = async (fin_prdt_cd) => {
    try {
      const response = await axios.get(`${BASE_URL}/deposit/product/${fin_prdt_cd}/`, {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      });
      DepositDetail.value = response.data;
      console.log(DepositDetail.value)
    } catch (error) {
      console.error("상품 상세 정보 로드 실패:", error);
    }
  };

  // 특정상품의 옵션들 불러오는 함수
  const getDepositOptions = function (fin_prdt_cd) {
    axios({
      method: "get",
      url: `${BASE_URL}/deposit/product/${fin_prdt_cd}/options`,
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    })
      .then((res) => {
        DepositOptions.value = res.data;
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err);
      });
  };


  
  // 최고 우대 금리를 포함한 상품 데이터를 불러오는 함수
  const getDepositProductsWithHighestRate = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/deposit/total/`, {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      });
      // API 응답 데이터를 depositProductsData에 저장
      depositProductsData.value = response.data.map(product => {
        // 최고 우대 금리와 저장 기간을 구함
        const highestRateOption = product.options.reduce((maxOption, option) => 
          option.intr_rate2 > maxOption.intr_rate2 ? option : maxOption, 
          product.options[0]
        );
        
        return {
          ...product,
          highestRateOption: {
            intr_rate2: highestRateOption ? highestRateOption.intr_rate2 : "데이터 없음",
            save_trm: highestRateOption ? highestRateOption.save_trm : ""
          }
        };
      });
    } catch (error) {
      console.error("상품 데이터 로드 실패:", error);
    }
  };

  // 상품 좋아요 토글
  const toggleLove = async (fin_prdt_cd) => {
    try {
      const response = await axios.post(
        `http://localhost:8000/like-product/deposit/${fin_prdt_cd}/`,
        {},
        {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        }
      );
      console.log(response);
      
      return response; // 좋아요 수가 업데이트된 response 반환
    } catch (error) {
      console.error("좋아요 토글 실패:", error);
      throw error;
    }
  };

  // ############################################# 찜

  // 찜하기 jjim_deposit(fin_prdt_cd) 실행하면 return으로 완료 메시지만 옴
  const jjim_deposit = function(fin_prdt_cd){ 
    const token = localStorage.getItem('token');
    axios({
      method : 'POST',
      url : `http://localhost:8000/like_product/deposit/${fin_prdt_cd}/`,
      headers: {Authorization: `Token ${token}`}
    }).then((res)=>{
      console.log(res.data);
    }).catch((err) => {
      console.log(err)
    }
  )}

  // 찜 취소하기 unjjim_deposit(fin_prdt_cd) 실행하면 return으로 완료 메시지만 옴
  const unjjim_deposit = function(fin_prdt_cd){
    const token = localStorage.getItem('token');
    axios({
      method : 'POST',
      url : `http://localhost:8000/unlike_product/deposit/${fin_prdt_cd}/`,
      headers: {Authorization: `Token ${token}`}
    }).then((res)=>{
      console.log(res.data);
    }).catch( (err)=>{
      console.log(err);
    }
  )}

  // 찜조회 jjimcheck_deposit()를 onMount해서 먼저 가져와놓기 이후 depositStore.myjjimData 로 보여주면 됨
  const myjjimData = ref([])
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

  // ############################################# 찜

  
  return { userStore, 
    BASE_URL, 
    depositProductsData, 
    DepositDetail, getDepositData,
    getDepositDetail, DepositOptions, getDepositOptions,
     getDepositProductsWithHighestRate, toggleLove,
     jjim_deposit,unjjim_deposit,jjimcheck_deposit, myjjimData
  }
})