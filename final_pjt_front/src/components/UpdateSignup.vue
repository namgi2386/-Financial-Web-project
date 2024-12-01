<template>
  <div class="container">
    <div v-if="isDefaultImgTag">
      <button @click="turnDefualtImagTag" style="border: none"><strong>기본이미지 선택</strong></button>
    </div>
    <div class="form-grid" >
      <div>
        <button @click="turnDefualtImagTag" v-if="!isDefaultImgTag" class="product-item">프로필 선택</button>
      </div>
      <div v-if="isDefaultImgTag" class="form-grid">
        <img :src="proDog1" alt="proDog1" class="profile-preview-DefaultImg " @click="getTempProfileImg(1)" :class="{ChoicedImgBorder : isChoicedImgDog === 1 , unChoicedImgBorder : isChoicedImgDog !== 1}" >
        <img :src="proDog2" alt="proDog2" class="profile-preview-DefaultImg " @click="getTempProfileImg(2)" :class="{ChoicedImgBorder : isChoicedImgDog === 2 , unChoicedImgBorder : isChoicedImgDog !== 2}">
        <img :src="proDog3" alt="proDog3" class="profile-preview-DefaultImg " @click="getTempProfileImg(3)" :class="{ChoicedImgBorder : isChoicedImgDog === 3 , unChoicedImgBorder : isChoicedImgDog !== 3}">
        <img :src="proDog4" alt="proDog4" class="profile-preview-DefaultImg " @click="getTempProfileImg(4)" :class="{ChoicedImgBorder : isChoicedImgDog === 4 , unChoicedImgBorder : isChoicedImgDog !== 4}">
        <img :src="proDog5" alt="proDog5" class="profile-preview-DefaultImg " @click="getTempProfileImg(5)" :class="{ChoicedImgBorder : isChoicedImgDog === 5 , unChoicedImgBorder : isChoicedImgDog !== 5}">
        <img :src="proDog6" alt="proDog6" class="profile-preview-DefaultImg " @click="getTempProfileImg(6)" :class="{ChoicedImgBorder : isChoicedImgDog === 6 , unChoicedImgBorder : isChoicedImgDog !== 6}">
        <img :src="proDog7" alt="proDog7" class="profile-preview-DefaultImg " @click="getTempProfileImg(7)" :class="{ChoicedImgBorder : isChoicedImgDog === 7 , unChoicedImgBorder : isChoicedImgDog !== 7}">
        <img :src="proDog8" alt="proDog8" class="profile-preview-DefaultImg " @click="getTempProfileImg(8)" :class="{ChoicedImgBorder : isChoicedImgDog === 8 , unChoicedImgBorder : isChoicedImgDog !== 8}">
        <img :src="proDog9" alt="proDog9" class="profile-preview-DefaultImg " @click="getTempProfileImg(9)" :class="{ChoicedImgBorder : isChoicedImgDog === 9 , unChoicedImgBorder : isChoicedImgDog !== 9}">
        <img :src="proDog10" alt="proDog10" class="profile-preview-DefaultImg " @click="getTempProfileImg(10)" :class="{ChoicedImgBorder : isChoicedImgDog === 10 , unChoicedImgBorder : isChoicedImgDog !== 10}">
      </div>
    </div>

    <form  @submit.prevent="updateInfo">
      <!-- <div v-if="profileImageUrl" class="mb-3">
        <img :src="profile.png" alt="프로필 사진 미리보기" class="profile-preview">
      </div> -->
  
      <!-- 두 개씩 한 줄에 배치할 폼 그룹 -->
      <div class="form-grid">
        <div class="mb-3">
          <label for="profileImage" class="form-label">프로필 사진</label>
          <input type="file" class="form-control" id="profileImage" @change="onFileChange" >
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">닉네임<span class="required">*</span></label>
          <input type="text" class="form-control" id="nickname" v-model="form.nickname" placeholder="닉네임 입력(1-20자)" onfocus="this.placeholder=''" onblur="this.placeholder='닉네임 입력(1-20자)'">
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">이메일 주소</label>
          <input type="text" class="form-control" id="email"   placeholder="ex) wjdtndus23@naver.com" onfocus="this.placeholder=''" onblur="this.placeholder='ex) wjdtndus23@naver.com'">
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">전화번호</label>
          <input type="text" class="form-control" id="phone" placeholder="000-0000-0000" onfocus="this.placeholder=''" onblur="this.placeholder='000-0000-0000'">
        </div>
      </div>
  
      <hr>
      <div id="emailHelp" class="form-text text-center mb-3">정확한 금융상품을 추천받기 위해 작성해주세요!!</div>
      
      <!-- 추가 정보도 두 개씩 한 줄에 배치 -->
      <div class="form-grid">
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">나이(세)<span class="required">*</span></label>
          <input type="number" class="form-control" v-model="form.age" id="age" min="0" placeholder="0">
        </div>
        <div class="mb-3">
            <label for="property" class="form-label">재산(만원)<span class="required">*</span></label>
            <input type="number" class="form-control" id="money" v-model="form.money" min="0" placeholder="0">
        </div>
        <div class="mb-3">
          <label for="desiredSubscriptionPeriod" class="form-label">희망 가입 기간<span class="required">*</span></label>
          <select class="form-control" id="desiredSubscriptionPeriod" v-model="form.desiredSubscriptionPeriod">
            <option value="" disabled>기간을 선택하세요</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
        <div class="mb-3">
        <label for="mainBank" class="form-label">주거래 은행<span class="required">*</span></label>
        <select class="form-control" id="mainBank" v-model="form.mainBank">
          <option value="" disabled>은행을 선택하세요</option>
          <option value="우리은행">우리은행</option>
          <option value="신한은행">신한은행</option>
          <option value="하나은행">하나은행</option>
          <option value="부산은행">부산은행</option>
          <option value="광주은행">광주은행</option>
          <option value="제주은행">제주은행</option>
          <option value="전북은행">전북은행</option>
          <option value="경남은행">경남은행</option>
          <option value="중소기업은행">중소기업은행</option>
          <option value="한국산업은행">한국산업은행</option>
          <option value="국민은행">국민은행</option>
          <option value="농협은행주식회사">농협은행주식회사</option>
          <option value="주식회사 케이뱅크">주식회사 케이뱅크</option>
          <option value="수협은행">수협은행</option>
          <option value="주식회사 카카오뱅크">주식회사 카카오뱅크</option>
          <option value="토스뱅크 주식회사">토스뱅크 주식회사</option>
          <option value="한국스탠다드차타드은행">한국스탠다드차타드은행</option>
          <option value="아이엠뱅크">아이엠뱅크</option>
        </select>
        </div>
      </div>
  
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary mt-4">회원정보수정</button>   
      </div>
    </form>
  </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
//   import { useUserStore } from "@/stores/userStore.js";
  import axios from 'axios'
  import { useRouter } from 'vue-router';
  import swal from "sweetalert";

  // 기본이미지 불러오기 
  import proDog1 from '@/assets/profile/proDog1.png';
  import proDog2 from '@/assets/profile/proDog2.png';
  import proDog3 from '@/assets/profile/proDog3.png';
  import proDog4 from '@/assets/profile/proDog4.png';
  import proDog5 from '@/assets/profile/proDog5.png';
  import proDog6 from '@/assets/profile/proDog6.png';
  import proDog7 from '@/assets/profile/proDog7.png';
  import proDog8 from '@/assets/profile/proDog8.png';
  import proDog9 from '@/assets/profile/proDog9.png';
  import proDog10 from '@/assets/profile/proDog10.png';
  // 기본이미지 변경하기
  const isDefaultImgTag = ref(false);
  const turnDefualtImagTag = function(){
    isDefaultImgTag.value = !isDefaultImgTag.value
    isChoicedImgDog.value = 0
  }
  // 기본이미지 선택하기
  const isChoicedImgDog = ref(0)
  const getTempProfileImg = function(n){
    isChoicedImgDog.value = n
  }
//######################################################
//   const userStore = useUserStore();
  const profileImageUrl = ref(null);
  const router = useRouter()
  
  const onFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      profileImageUrl.value = URL.createObjectURL(file);
    }
  };

  const token = localStorage.getItem('token');
  const form = ref({
     age : '',
     profile_img : profileImageUrl.value,
     money : '',
     nickname :' ',
     desiredSubscriptionPeriod : '',
     mainBank : '',
  })

  const updateInfo =async  () => {
    const token = localStorage.getItem('token');
    const formData = new FormData()

    formData.append('age', form.value.age);
    formData.append('money', Number(form.value.money) * 1000);
    formData.append('nickname', form.value.nickname);
    formData.append('desiredSubscriptionPeriod', form.value.desiredSubscriptionPeriod);
    formData.append('mainBank', form.value.mainBank);

    const fileInput = document.getElementById('profileImage');
    if (fileInput.files[0]) {
      formData.append('profile_img', fileInput.files[0]);
      
    } else if (isChoicedImgDog.value !== 0){
      
      const tempImgLink =  `accounts/proDog${isChoicedImgDog.value}.png`
      
      // try {
      //   const response = await fetch(tempImgLink); // 이미지 로드
      //   const blob = await response.blob(); // Blob 객체 생성
      //   const file = new File([blob], `proDog${isChoicedImgDog.value}.png`, { type: blob.type });
      //   formData.append('profile_img', file); // 변환된 파일 추가
      // } catch (error) {
      //   console.error('이미지 파일 변환 중 에러 발생:', error);
      // }
    }
    // for (let [key, value] of formData.entries()) {
    //   console.log(`${key}: ${value}`);
    // }

    axios
      .put('http://localhost:8000/accounts/profile/', formData, {
        headers: { Authorization: `Token ${token}` },
        'Content-Type': 'multipart/form-data',
      })
      .then(() => {
        swal({
          icon: 'success',
          title: '회원가입 정보가 수정되었습니다.',
          showConfirmButton: false,
          timer: 1500,
        });
        router.push({ name: 'profile' });
      })  
      .catch((err) => {
        console.error(err);
        swal({
          icon: 'error',
          title: '정보 수정에 실패했습니다.',
          text: '잠시 후 다시 시도해주세요.',
        });
      });
  };

// 회원정보 불러오기
const loadUserInfo = () => {
  axios
    .get('http://localhost:8000/accounts/profile/', {
      headers: { Authorization: `Token ${token}` },
    })
    .then((response) => {
      const data = response.data;
      form.value.username = data.username;
      form.value.nickname = data.nickname;
      form.value.age = data.age;
      form.value.money = parseInt(Number(data.money)/1000) ;
      form.value.desiredSubscriptionPeriod = data.desiredSubscriptionPeriod;
      form.value.mainBank = data.mainBank;
    })
    .catch((err) => {
      console.error(err);
      alert('회원정보를 불러오는데 실패했습니다.');
    });
};

// 페이지 로드 시 회원정보 불러오기 실행
onMounted(() => {
  loadUserInfo();
});
  </script>
  
  <style scoped>
/* 프로필 사진 스타일 */
.profile-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  margin: 20px auto;
  display: block;
  border: 3px solid #6f42c1; /* 강조 색 추가 */
}

/* form-grid: 두 개씩 한 줄에 배치 */
.form-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.form-grid .mb-3 {
  flex: 1 1 calc(50% - 20px); /* 두 개가 한 줄에 배치되도록 설정 */
}


/* 라벨 스타일 */
.form-label {
  font-weight: bold;
  color: #333;
}

/* 입력 필드 스타일 */
.form-control {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  font-size: 14px;
}

.form-control:focus {
  border-color: #6f42c1;
  box-shadow: 0 0 5px rgba(111, 66, 193, 0.5);
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #6f42c1;
  border-color: #6f42c1;
  padding: 10px 15px;
  font-size: 18px;
  border-radius: 8px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;

  font-weight: bold;
}

.btn-primary:hover {
  background-color: #5a32a3;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 안내 문구 스타일 */
.form-text {
  font-size: 14px;
  color: #555;
}

/* 필수 항목 스타일 */
.required {
  color: red;
  font-weight: bold;
}

/* 컨테이너 스타일 */
.container {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f9f9f9; /* 밝은 배경 */
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 기본 텍스트 색상 */
body {
  color: #333;
}

/* 텍스트 가운데 정렬 */
.text-center {
  text-align: center;
}

/* 파일 업로드 버튼 스타일 */
input[type="file"] {
  border: none;
  padding: 5px;
  font-size: 14px;
}

/* 전반적인 공간 조정 */
.mb-3 {
  margin-bottom: 20px;
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
  margin: 5px;
}
.profile-preview-DefaultImg {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  /* border: 2px solid #ddd; */
   /* 테두리 추가 */
  margin: 0 auto;
}
.unChoicedImgBorder {
  border: 3px solid #6f42c1;
}
.ChoicedImgBorder {
  width: 110px;
  height: 110px;
  border: 4px solid #ca2f5d;
}
</style>

  