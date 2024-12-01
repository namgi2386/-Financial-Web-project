<template>
    <div class="container">
      <h1 class="title mb-4">근처 은행 찾기</h1>
      <div>
        <!-- 시/도와 구/군 검색 창 -->
        <div class="row mb-3">
          <select name="province" id="province" v-model="province" class="form-control col">
            <option value="" selected disabled hidden> 시/도 선택 </option>
            <option :value="pr" v-for="pr in provinceInput" :key="pr">{{ pr }}</option>
          </select>
          <select name="country" id="country" v-model="country" class="form-control col">
            <option value="" selected disabled hidden> 구/군 선택 </option>
            <option :value="ct" v-for="ct in countryInput[prIdx]" :key="ct">{{ ct }}</option>
          </select>
          <select name="bank" id="bank" v-model="bank" class="form-control col">
            <option value="" selected disabled hidden>은행 선택</option>
            <option :value="bk" v-for="bk in bankList" :key="bk">{{ bk }}</option>
          </select>
          
        </div>
        <!-- 은행 선택 창 -->
        <div class="m-3 text-center">
          <button @click="selectedLocation(address)" class="custom-btn col me-3">선택한 지역으로 이동</button>
          <button @click="searchBank(bank)" class="custom-btn col me-3">은행 검색</button>
          <button @click="currentLocation" class="custom-btn col">현재 위치로 이동</button>
        </div>
      </div>
      <div>
        <Map ref="mapRef" />
      </div>
    </div>
  </template>
  
  <script setup>
  import Map from "@/components/Map/Map.vue";
  import { ref, watch, computed } from "vue";
  
  const provinceInput = ["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도", "강원특별자치도"];
  const countryInput = {
    0: ['강남구','강동구','강북구','강서구','관악구','광진구','구로구',
    '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구',
    '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구',
    '은평구', '종로구', '중구', '중랑구'],
    1: ['강서구','금정구','기장군','남구','동구','동래구','부산진구','북구','사상구',
    '사하구','서구','수영구','연제구','영도구','중구','해운대구'],
    2: ['군위군','남구','달서구','달성군','동구','북구','서구','수성구','중구'],
    3: ['강화군','계양구','남동구','동구','미추홀구','부평구','서구','연수구','옹진군','중구'],
    4: ['광산구','남구','동구','북구','서구'],
    5: ['대덕구','동구','서구','유성구','중구'],
    6: ['남구','동구','북구','울주군','중구'],
    7: [''],
    8: ['가평군','고양시 덕양구','고양시 일산동구','고양시 일산서구','과천시','광명시','광주시','구리시','군포시','김포시','남양주시','동두천시','부천시','성남시 분당구','성남시 수정구','성남시 중원구','수원시 권선구','수원시 영통구','수원시 장안구','수원시 팔달구','시흥시','안산시 단원구','안산시 상록구','안성시','안양시 동안구','안양시 만안구','양주시','양평군','여주시','연천군','오산시','용인시 기흥구','용인시 수지구','용인시 처인구','의왕시','의정부시','이천시','파주시','평택시','포천시','하남시','화성시'],
    9: ['괴산군','단양군','보은군','영동군','옥천군','음성군','제천시','증평군','진천군','청주시 상당구','청주시 서원구','청주시 청원구','청주시 흥덕구','충주시'],
    10: ['계롱시','공주시','금산군','논산시','당진시','보령시','부여군','서산시','서천군','아산시','예산군','천안시 동남구','천안시 서북구','청양군','태안군','홍성군'],
    11: ['고창군','군산시','김제시','남원시','무주군','부안군','순창군','완주군','익산시','임실군','장수군','전주시 덕진구','전주시 완산구','정읍시','진안군'],
    12: ['강진군','고흥군','곡성군','광양시','구례군','나주시','단양군','목포시','무안군','보성군','순천시','신안군','여수시','영광군','영암군','완도군','장성군','장흥군','진도군','함평군','해남군','화순군'],
    13: ['경산시','경주시','고령군','구미시','김천시','문경시','봉화군','상주시','성주군','안동시','영덕군','영양군','영주시','영천시','예천군','울릉군','울진군','의성군','청도군','청송군','칠곡군','포항시 남구','포항시 북구'],
    14: ['거제시','거창군','고성군','김해시','남해군','밀양시','사천시','산청군','양산시','의령군','진주시','창녕군','창원시 마산합포구','창원시 마산회원구','창원시 성산구','창원시 의창구','창원시 진해구','통영시','하동군','함안군','함양군','합천군'],
    15: ['서귀포시','제주시'],
    16: ['강릉시','고성군','동해시','삼척시','속초시','양구군','양양군','영월군','원주시','인제군','정선군','철원군','춘천시','태백시','평창군','홍천군','화천군','횡성군']
}
  const bankList = ["SC제일은행", "경남은행", "광주은행", "국민은행", "기업은행", "농협은행", "대구은행", "부산은행", "수협은행", "신한은행", "외환은행", "우리은행", "전북은행", "제주은행", "하나은행", "한국산업은행", "한국시티은행"];
  
  const province = ref("");
  const country = ref("");
  const pointInfo = ref(null);
  const bank = ref("");
  
  const prIdx = computed(() => provinceInput.findIndex((item) => item === province.value));
  const address = computed(() => province.value + " " + country.value);
  
  const mapRef = ref(null);
  const lat = ref('');
  const lon = ref('');
  
  const currentLocation = () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        lat.value = position.coords.latitude;
        lon.value = position.coords.longitude;
        mapRef.value.setCenter(lat.value, lon.value);
        console.log(`현재 위치: 위도 ${lat.value}, 경도 ${lon.value}`);
      }, () => {
        window.alert("위치 정보를 불러올 수 없습니다.");
      });
    } else {
      window.alert("현재 위치 기능을 지원하지 않습니다.");
    }
  };
  
  const selectedLocation = (address) => {
    mapRef.value.moveSelectedLocation(address);
    console.log("지도 중심 이동");
  };
  
  const searchBank = (bank) => {
    mapRef.value.markBank(address.value ,bank);
    console.log(address.value);
    
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
  
  /* 제목 스타일 */
  .title {
  color: #333;
  margin-bottom: 10px;
  letter-spacing: -0.5px;
  text-align: center;
  font-family: 'Godo', sans-serif;
  font-weight: bold;
}
  
  /* 버튼 스타일 */
  .custom-btn {
    background: #7a6db3; /* 보라색 배경 */
    color: white;
    border: none;
    border-radius: 30px;
    padding: 10px 20px; /* 버튼 크기 줄이기 */
    font-size: 14px; /* 글자 크기 조정 */
    font-weight: bold;
    cursor: pointer;
    width: auto; /* 버튼 크기를 내용에 맞게 자동으로 설정 */
    transition: all 0.3s ease;
    text-align: center;
  }
  
  .custom-btn:hover {
    background: #5a34a2;
    transform: scale(1.01); /* hover 시 살짝 확대 */
  }
  
  .custom-btn:focus {
    outline: none;
  }
  
  /* select 태그 스타일 */
  select {
    background-color: #f8f9fa; /* 연한 회색 배경 */
    border: 1px solid #ced4da;
    border-radius: 30px;
    padding: 8px 12px; /* padding 크기 줄이기 */
    font-size: 14px; /* 글자 크기 조정 */
    color: #495057;
    transition: border-color 0.3s ease;
  }
  
  select:focus {
    border-color: #8e44ad; /* 보라색 포커스 색상 */
    box-shadow: 0 0 4px rgba(142, 68, 173, 0.5);
  }
  
  /* row 스타일 (입력창, 버튼 배치) */
  .row {
    display: flex; 
    justify-content: space-between;  
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  /* 폼 컨트롤 스타일 (입력창) */
  .form-control {
    flex: 1;
    border-radius: 8px;
    padding: 8px 12px; /* padding 크기 줄이기 */
    border: 1px solid #ced4da;
    font-size: 14px; /* 글자 크기 조정 */
    color: #495057;
  }
  
  /* 지도 스타일 */
  #map {
    width: 100%;
    height: 400px; /* 지도 높이 조정 */
    border-radius: 15px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  }

  @font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}
</style>

  
  