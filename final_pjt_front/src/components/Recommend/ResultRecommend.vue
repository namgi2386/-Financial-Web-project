<template>
    <div class="d1">
        <div class="d2">
            <h3><strong>{{ userStore.profileData.nickname }}</strong>
              <span class="d2_title">님의 <strong>목표</strong>그래프</span>
            </h3>
        </div>
        <div class="d3">
            <div class="d4">
                <canvas ref="chartContainer" ></canvas>
            </div>
            <div class="d5">
                    <button v-for="product in myCart" :key="product.id" @click="addProductToCart(product)" class="product-item">
                        {{ getFilteredName(product.fin_prdt_nm) }}
                    </button>
                    <!-- <div v-for="product in myCart" :key="product.id">
                        {{ product.best_option.final_savings }}
                    </div> -->
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref,  defineProps , defineEmits , onMounted , watchEffect} from 'vue'
import { useUserStore } from '@/stores/userStore';
import { Chart } from 'chart.js/auto';

const userStore = useUserStore()
const emit = defineEmits()

const props = defineProps({
    myCart: {
        type: Array,
        required: true
    }
})

function addProductToCart(product) {
    emit('add-to-cart', product)
    console.log("cartupdated");
    updateChart() // myCart 변경 시 차트 업데이트
}
function getFilteredName(productName) {
    return productName.split("(")[0].trim(); 
}

const chartContainer = ref(null)
let chartInstance = null

const updateChart = () => {
  const goalDate = Number(userStore.finInfoData.goal_date)
  const currentAssets = parseFloat(userStore.finInfoData.current_assets)
  const monthlySavings = parseFloat(userStore.finInfoData.monthly_savings)
  const goalAmount = parseFloat(userStore.finInfoData.goal_amount)

  // X축 라벨 (개월수)
  const labels = Array.from({ length: goalDate }, (_, i) => `${i + 1}개월`)

  // Y축 데이터 (자산 증가 값 계산)
  const data = Array.from({ length: goalDate }, (_, i) => currentAssets + monthlySavings * (i))

  // 목표 금액 도달 시점 계산
  const goalMonthIndex = data.findIndex(value => value >= goalAmount)

  const goalMarker = goalMonthIndex !== -1 ? [{
    x: goalMonthIndex, 
    y: goalAmount,
    r: 6, 
    backgroundColor: 'red',
    borderColor: 'white',
    borderWidth: 2,
  }] : []

  // myCart에 추가된 제품들의 누적 이자 데이터 계산
  const additionalInterestData = []
  props.myCart.forEach(product => {
    const productInterest = product.best_option.final_savings.map(item => item.final)
    if (additionalInterestData.length === 0) {
      additionalInterestData.push(...productInterest)
    } else {
      additionalInterestData.forEach((value, index) => {
        additionalInterestData[index] += productInterest[index]
      })
    }
  })

  const totalDataWithInterest = data.map((value, index) =>  value + (additionalInterestData[index] || 0))

  if (chartInstance) {
    // 기존 차트가 있으면 업데이트
    chartInstance.data.datasets[0].data = data
    chartInstance.data.datasets[1].data = additionalInterestData
    chartInstance.data.datasets[2].data = new Array(goalDate).fill(goalAmount)
    chartInstance.update()
  } else {
    // 차트 초기화
    chartInstance = new Chart(chartContainer.value, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: '자산 증가 추이',
            data,
            borderColor: '#8f7bb3',
            backgroundColor: 'rgba(143, 123, 179, 0.2)',
            fill: true,
            tension: 0.4,
            pointStyle: 'circle',
            pointRadius: 5,
            pointBackgroundColor: '#8f7bb3',
          },
          {
            label: '누적 이자',
            data: additionalInterestData,
            borderColor: '#ff5733',
            backgroundColor: 'rgba(255, 87, 51, 0.2)',
            fill: true,
            tension: 0.4,
            pointStyle: 'circle',
            pointRadius: 5,
            pointBackgroundColor: '#ff5733',
          },
          {
            label: '목표 금액',
            data: new Array(goalDate).fill(goalAmount),
            borderColor: 'red',
            borderWidth: 2,
            fill: false,
            borderDash: [5, 5],
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: '개월수',
            },
            grid: {
              display: false,
            },
          },
          y: {
            title: {
              display: true,
              text: '자산 (원)',
            },
            grid: {
              display: false,
            },
            ticks: {
              callback: (value) => `${value.toLocaleString()} 원`,
            },
          },
        },
      },
    })
  }
}

onMounted(() => {
  updateChart() // 컴포넌트가 마운트되면 첫 차트 렌더링
})

watchEffect(() => {
  if (props.myCart && props.myCart.length > 0) {
    console.log("cartupdated");
    updateChart() // myCart 변경 시 차트 업데이트
  }
})

</script>

<style scoped>

.d1 {
    display: flex;
    flex-direction: column;
    /* width: 100%; */
    /* height: 100%;  */
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    /* background-color: blueviolet; */
}

/* d2: 항상 위에 위치 */
.d2 {
    display: flex;
    align-content: center;
    justify-content: center;
    box-sizing: border-box;
}

/* d3: 아래 위치, flex로 자식 요소 배치 */
.d3 {
    display: flex;
    flex-direction: column; /* 세로 정렬 */
    width: 100%;
    flex-grow: 1; /* 남은 공간을 차지 */
}

/* d4: d3의 70% 높이를 차지 */
.d4 {
    flex-grow: 7;
    padding: 10px;
    box-sizing: border-box;
    display: flex; 
    align-items: stretch; 
    justify-content: stretch;
    /* border: 1px solid black; */
    /* box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); */
}

canvas {
    /* background-color: #f8d7da; */
    flex-grow: 1;
    /* width: 100%;  */
    /* height: 100%;  */
    display: block; 
}

/* d5: d3의 30% 높이를 차지 */
.d5 {
    flex-grow: 3; 
    /* width: 100%; */
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 3px;
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap; 
    gap: 10px; 
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
    margin-bottom: 2px;
}

.d2_title {
  font-size: 25px;
}

</style>