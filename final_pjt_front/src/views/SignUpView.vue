<template>
    <form class="container" @submit.prevent="Signup">
      <!-- <div class="mb-3">
        <label for="profileImage" class="form-label">프로필 사진</label>
        <input type="file" class="form-control" id="profileImage" @change="onFileChange">
      </div>
  
      <div v-if="profileImageUrl" class="mb-3">
        <img :src="profile.png" alt="프로필 사진 미리보기" class="profile-preview">
      </div> -->
  
      <!-- 두 개씩 한 줄에 배치할 폼 그룹 -->
      <div class="form-grid">
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label">Username<span class="required">*</span></label>
          <input type="text" class="form-control" id="username" v-model="username" placeholder="아이디 입력(6-20자)" onfocus="this.placeholder=''" onblur="this.placeholder='아이디 입력(6-20자)'">
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">닉네임<span class="required">*</span></label>
          <input type="text" class="form-control" id="nickname" v-model="nickname" placeholder="닉네임 입력(1-20자)" onfocus="this.placeholder=''" onblur="this.placeholder='닉네임 입력(1-20자)'">
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Password<span class="required">*</span></label>
          <input type="password" class="form-control" v-model="password1" id="password1" 
          placeholder="비밀번호 입력(문자, 숫자, 특수문자 포함 8-20자)" onfocus="this.placeholder=''" onblur="this.placeholder='비밀번호 입력(문자, 숫자, 특수문자 포함 8-20자)'" @input="validatePassword">
          <p v-if="isPasswordInvalid" class="error-message">8자 이상으로 입력해주세요</p>
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Check Password<span class="required">*</span></label>
          <input type="password" class="form-control" v-model="password2" id="password2" placeholder="비밀번호 재입력" onfocus="this.placeholder=''" onblur="this.placeholder='비밀번호 재입력'">
          <small v-if="password1 !== password2" class="text-danger">비밀번호가 일치하지 않습니다.</small>
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">이메일 주소</label>
          <input type="text" class="form-control" id="email" placeholder="ex) wjdtndus23@naver.com" onfocus="this.placeholder=''" onblur="this.placeholder='ex) wjdtndus23@naver.com'">
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
          <input type="number" class="form-control" v-model="age" id="age" min="0" placeholder="0">
        </div>
        <div class="mb-3">
            <label for="property" class="form-label">재산<span class="required">*</span></label>
            <input type="number" class="form-control" id="money" v-model="money" min="0" placeholder="0">
        </div>
        <div class="mb-3">
          <label for="desiredSubscriptionPeriod" class="form-label">희망 가입 기간<span class="required">*</span></label>
          <select class="form-control" id="desiredSubscriptionPeriod" v-model="desiredSubscriptionPeriod">
            <option value="" disabled>기간을 선택하세요</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
        <div class="mb-3">
        <label for="mainBank" class="form-label">주거래 은행<span class="required">*</span></label>
        <select class="form-control" id="mainBank" v-model="mainBank">
          <option value="" disabled>은행을 선택하세요</option>
          <option value="KB국민은행">우리은행</option>
          <option value="신한은행">신한은행</option>
          <option value="우리은행">하나은행</option>
          <option value="하나은행">부산은행</option>
          <option value="NH농협은행">광주은행</option>
          <option value="카카오뱅크">제주은행</option>
          <option value="토스뱅크">전북은행</option>
          <option value="토스뱅크">경남은행</option>
          <option value="토스뱅크">중소기업은행</option>
          <option value="토스뱅크">한국산업은행</option>
          <option value="토스뱅크">국민은행</option>
          <option value="토스뱅크">농협은행주식회사</option>
          <option value="토스뱅크">주식회사 케이뱅크</option>
          <option value="토스뱅크">수협은행</option>
          <option value="토스뱅크">주식회사 카카오뱅크</option>
          <option value="토스뱅크">토스뱅크 주식회사</option>
          <option value="토스뱅크">한국스탠다드차타드은행</option>
          <option value="토스뱅크">아이엠뱅크</option>
        </select>
        </div>
      </div>
  
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary mt-4">회원가입!</button>   
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useUserStore } from "@/stores/userStore.js";
  import swal from 'sweetalert';
  
  
  const userStore = useUserStore();
  const profileImageUrl = ref(null);
  
  const onFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      profileImageUrl.value = URL.createObjectURL(file);
    }
  };

    const username = ref('')
    const password1 = ref('');
    const password2 = ref('');
    const age = ref('');
    const money = ref('');
    const nickname = ref('')
    const desiredSubscriptionPeriod = ref('')
    const mainBank = ref('')
    const isPasswordInvalid = ref(false); // 유효성 검사 상태

    // 비밀번호 유효성 검사 함수
    const validatePassword = () => {
      isPasswordInvalid.value = password1.value.length > 0 && password1.value.length <= 8;
    };

    const Signup = () => {
      if (!username.value || !password1.value || !password2.value || !age.value || !money.value || !nickname.value || !desiredSubscriptionPeriod.value || !mainBank.value) {
        swal({
          icon: 'warning',
          title: '입력 오류',
          text: '모든 필수 항목을 입력해주세요!',
        });
        return;
      }
      if (password1.value !== password2.value) {
        swal({
          icon: 'error',
          title: '비밀번호 불일치',
          text: '비밀번호가 일치하지 않습니다!',
        });
        return;
      }
      
      const payload = {
        username: username.value,
        password1: password1.value,
        password2: password2.value,
        age : age.value,
        money : money.value,
        nickname : nickname.value,
        desiredSubscriptionPeriod : desiredSubscriptionPeriod.value,
        mainBank : mainBank.value,
      }

      userStore.signUp(payload);
  }

  </script>
  
  <style scoped>
/* 공통 스타일 */
.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 프로필 사진 스타일 */
.profile-preview {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin: 10px auto;
  display: block;
}

/* form-grid: 두 개씩 한 줄에 배치 */
.form-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.form-grid .mb-3 {
  flex: 1 1 calc(50% - 20px);
}

.mb-3 label {
  font-weight: bold;
  color: #333;
}

.mb-3 input,
.mb-3 select {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  font-size: 14px;
}

.mb-3 input:focus,
.mb-3 select:focus {
  outline: none;
  border-color: #6f42c1;
  box-shadow: 0 0 5px rgba(111, 66, 193, 0.3);
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #6f42c1;
  border-color: #6f42c1;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #5a32a3;
  border-color: #5a32a3;
}

/* 안내 텍스트 스타일 */
.form-text {
  font-size: 14px;
  color: #555;
}

/* 필수 항목 스타일 */
.required {
  color: red;
  font-weight: bold;
}

/* 회원가입 링크 */
.signup-link {
  color: #6f42c1;
  text-decoration: none;
  text-align: center;
  display: block;
  margin-top: 20px;
  font-size: 14px;
}

.signup-link:hover {
  color: #5a32a3;
}

/* 입력 오류 메시지 스타일 */
.text-danger {
  font-size: 12px;
  color: red;
  margin-top: 5px;
}

/* 반응형 디자인 */
@media (max-width: 576px) {
  .form-grid {
    flex-direction: column;
    gap: 15px;
  }

  .form-grid .mb-3 {
    flex: 1 1 100%;
  }
}

.error-message {
  color: red;
  font-size: 0.75rem; /* 작은 글씨 크기 */
  margin-top: 0.3rem; /* 입력창과의 간격 */
}
</style>

  