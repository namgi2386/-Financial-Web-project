<template>
    <div align="center">
      <!-- 자유적립식 차트 -->
      <div v-if="chartDataS.labels.length" class="chart-container">
        <Bar class="chart" :options="chartOptionsS" :data="chartDataS" />
      </div>
  
      <!-- 차트 구분선 -->
      <hr v-if="chartDataS.labels.length && chartDataF.labels.length" />
  
      <!-- 정액적립식 차트 -->
      <div v-if="chartDataF.labels.length" class="chart-container">
        <Bar class="chart" :options="chartOptionsF" :data="chartDataF" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from "vue";
  import { Bar } from "vue-chartjs";
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from "chart.js";
  import colors from "vuetify/lib/util/colors";
  
  // Chart.js를 위한 플러그인 등록
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
  
  const props = defineProps({
    product: Object,
  });
  
  // 데이터셋을 만드는 함수
  const createChartData = (data, type) => {
    const filteredData = data.filter((item) => item.rsrv_type_nm === type);
    const sortedData = filteredData.sort((a, b) => a.save_trm - b.save_trm);
  
    const labels = sortedData.map((item) => `${item.save_trm}개월 금리`);
    return {
      labels,
      datasets: [
        {
          label: "저축 금리",
          data: sortedData.map((item) => item.intr_rate),
          backgroundColor: "#1089FF",
          stack: "Stack 1",
        },
        {
          label: "최고 우대 금리",
          data: sortedData.map((item) => item.intr_rate2),
          backgroundColor: colors.red.accent2,
          stack: "Stack 2",
        },
      ],
    };
  };
  
  // 차트 데이터 및 평균 계산
  const chartDataS = computed(() => createChartData(props.product.options, "자유적립식"));
  const chartDataF = computed(() => createChartData(props.product.options, "정액적립식"));
  
  // 차트 옵션
  const chartOptionsS = ref({
    plugins: {
      title: {
        display: true,
        text: `자유적립식 저축 금리`,
        font: {
          size: 18, // 제목의 글꼴 크기 설정
        },
      },
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        ticks: {
          maxRotation: 0,
          minRotation: 0,
          font: {
            size: 10,
          },
        },
      },
      y: {
        stacked: true,
        beginAtZero: true,
        title: {
          display: true,
          text: "금리 (%)",
        },
      },
    },
  });
  
  const chartOptionsF = ref({
    plugins: {
      title: {
        display: true,
        text: `정액적립식 저축 금리`,
        font: {
          size: 18, // 제목의 글꼴 크기 설정
        },
      },
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        ticks: {
          maxRotation: 0,
          minRotation: 0,
          font: {
            size: 10,
          },
        },
      },
      y: {
        stacked: true,
        beginAtZero: true,
        title: {
          display: true,
          text: "금리 (%)",
        },
      },
    },
  });
  </script>
  
  <style scoped>
  .chart-container {
    margin-bottom: 40px; /* 그래프 간 간격 */
    width: 80%;
  }
  
  .chart {
    font-family: "ibm-plex-sans-kr-regular"; /* 그래프 글씨체 */
  }
  
  .averages {
    display: flex;
    justify-content: space-between;
    width: 70%;
    margin: 20px auto;
    font-family: "ibm-plex-sans-kr-regular"; /* 평균 값 글씨체 */
  }
  
  hr {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 100px;
    margin-right: 100px;
    box-shadow: 1px 1px 1px rgba(193, 193, 193, 0.435);
    border: 1px solid rgba(255, 255, 255, 0);
  }
  </style>
  