<template>
    <div class="container">
      <h1 class="title">근처 ATM 찾기</h1>
        <div class="row mb-3">
          <button @click="currentLocation" class="custom-btn ">현재 위치 근처 ATM 검색</button>
        </div>
      <div>
        <Map ref="mapRef" />
      </div>
    </div>
  </template>
  
  <script setup>

  import Map from "@/components/Map/Map.vue";
  import { ref, watch, computed } from "vue";

  const mapRef = ref(null);
  
  const currentLocation = () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        mapRef.value.setCenter(lat, lon);
        console.log(`현재 위치: 위도 ${lat}, 경도 ${lon}`);
        search_markATM(lat, lon)
        console.log(mapRef)
      }, () => {
        window.alert("위치 정보를 불러올 수 없습니다.");
      });
    } else {
      window.alert("현재 위치 기능을 지원하지 않습니다.");
    }
  };

  const search_markATM = (lat, lon) => {
    mapRef.value.markATM(lat, lon);
    console.log("선택한 은행 지도에서 마크 표시");
  };


  </script>
  
  <style scoped>
  /* 전체 배경 */
  .container {
    background-color: #ffffff; /* 밝은 흰색으로 변경 */
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    padding: 20px 30px; /* 여백을 조정해 더 균형 있게 설정 */
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15); /* 그림자 강조 */
    max-width: 800px;
    margin: 0 auto;
  }

.title {
  color: #333;
  margin-bottom: 20px;
  letter-spacing: -0.5px;
  text-align: center;
  font-family: 'Godo', sans-serif;
  font-weight: bold
}

/* 제목 스타일 */
/* h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333; /* 어두운 회색 */
  /* text-align: center;
  margin-bottom: 30px; */
/* } */ 


/* 버튼 스타일 */
.custom-btn {
  background: #7a6db3;
  color: white;
  border: none;
  border-radius: 30px; /* 완전 둥근 버튼 */
  padding: 10px 20px;  /* padding 줄이기 */
  font-size: 14px; /* 글씨 크기 줄이기 */
  font-weight: bold;
  cursor: pointer;
  width: auto; /* 버튼 크기를 내용에 맞게 자동으로 설정 */
  transition: all 0.3s ease; /* 부드러운 트랜지션 */
  text-align: center;
}

.custom-btn:hover {
  background: #5a34a2;
  transform: scale(1.01); /* 마우스 올리면 버튼이 약간 커짐 */
}

.custom-btn:focus {
  outline: none; /* 버튼 클릭 시 테두리 없애기 */
}


/* 지도 컨테이너 */
.row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

/* 입력창, form-control 스타일 (필요시) */
.form-control {
  flex: 1;
  border-radius: 5px;
  border: 1px solid #ddd;
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
}

/* 지도 크기 조정 (필요 시) */
#map {
  width: 100%;
  height: 400px; /* 원하는 크기로 지도 설정 */
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin: 0;
}

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}

  </style>
  