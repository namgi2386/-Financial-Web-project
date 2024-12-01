import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios"

export const useRecommendStore = defineStore('recommend', () => {
  
  const PrivateProducts = ref([]) // 전체 데이터 저장
  const get_recommendByPrivate = function () {
    const token = localStorage.getItem('token');
    axios({
        method: 'GET',
        url: 'http://localhost:8000/hot/recommendByPrivateDeposit/',
        headers: { Authorization: `Token ${token}` }
    })
    .then((res) => {
        // console.log(res.data);
        PrivateProducts.value = res.data;
    })
    .catch(err => console.log(err))}
  const PrivateProductsForSaving = ref([]) // 전체 데이터 저장
  const get_recommendByPrivateForSaving = function () {
    const token = localStorage.getItem('token');
    axios({
        method: 'GET',
        url: 'http://localhost:8000/hot/recommendByPrivateSaving/',
        headers: { Authorization: `Token ${token}` }
    })
    .then((res) => {
        // console.log(res.data);
        PrivateProductsForSaving.value = res.data;
    })
    .catch(err => console.log(err))}


  return { get_recommendByPrivate,PrivateProducts,get_recommendByPrivateForSaving,PrivateProductsForSaving}
})