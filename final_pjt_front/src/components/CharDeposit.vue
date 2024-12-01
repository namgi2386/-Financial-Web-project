<template>
  <div>
  </div>
    <div align="center">
      <div v-if="chartData.labels.length" class="chart-container">
        <Bar class="chart" :options="chartOptions" :data="chartData" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from "vue";
  import { Bar } from "vue-chartjs";
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from "chart.js";
  import colors from "vuetify/lib/util/colors";
  
  const props = defineProps({
    product: Object,
  });
  
  // Chart.js 플러그인 등록
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
  
  // 데이터셋 생성 함수
  const createChartData = (options) => {
    const sortedData = options.sort((a, b) => a.save_trm - b.save_trm);
  
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
          backgroundColor: "#FF5252", // Vuetify colors 제거
          stack: "Stack 2",
        },
      ],
    };
  };
  
  
  // 차트 데이터 및 평균 계산
  const chartData = computed(() => createChartData(props.product.options));
  
  const chartOptions = ref({
    plugins: {
      title: {
        display: true,
        text: `저축 금리`,
        font: {
          size: 18, // 제목 글꼴 크기
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
    margin-bottom: 50px; /* 그래프 간 간격 */
    width: 80%;
    max-width: 700px; /* 최대 너비 */
  }
  
  .chart {
    font-family: "ibm-plex-sans-kr-regular"; /* 그래프 글씨체 */
  }

  </style>
  