<template>
    <form class="container" @submit.prevent="logIn">
        <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label" >Username</label>
            <input type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="아이디" v-model="username">
        </div>
        <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label" >Password</label>
            <input type="password" class="form-control" id="exampleInputPassword1" placeholder="비밀번호" v-model="password">
        </div>
        <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary">LOG IN</button>   
        </div>
        <RouterLink :to="{name:'signup'}" class="signup-link">회원가입</RouterLink>
    </form>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue'
import {useUserStore} from "@/stores/userStore.js";
import swal from 'sweetalert';

const userStore = useUserStore();
const username = ref('');
const password = ref('');

const logIn = async () => {
  if (!username.value || !password.value) {
    swal({
        icon: 'warning',
        title: '로그인 실패',
        text: '다시 시도해주세요.',
    });
    return;
  }

  const payload = {
    username: username.value,
    password: password.value,
  };

  try {
    // 사용자 인증 요청
    await userStore.logIn(payload);
  } catch (error) {
    // 인증 실패 시 경고 메시지
    console.log(err);
  }
};

</script>

<style scoped>
/* 컨테이너 중앙 정렬 및 폭 조정 */
.container {
    max-width: 400px; /* 페이지 중앙에 적당한 크기 */
    margin: 50px auto; /* 중앙 정렬과 상단 여백 */
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px; /* 부드러운 모서리 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 약간의 그림자 추가 */
    background-color: #fff; /* 흰색 배경 */
}

/* 라벨 스타일 */
.form-label {
    font-weight: bold;
    color: #444; /* 기본 글자 색상 */
}

/* 입력 필드 스타일 */
.form-control {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1); /* 입력 필드 내부 그림자 */
}

.form-control:focus {
    border-color: #6f42c1;
    box-shadow: 0 0 5px rgba(111, 66, 193, 0.5); /* 보라색 포커스 효과 */
}

/* 버튼 스타일 */
.btn-primary {
    background-color: #6f42c1; /* 보라색 배경 */
    border-color: #6f42c1; /* 보라색 테두리 */
    font-size: 16px; /* 버튼 글씨 크기 */
    font-weight: bold;
    border-radius: 5px; /* 부드러운 모서리 */
}

.btn-primary:hover {
    background-color: #5a32a3; /* hover 시 색상 변경 */
    border-color: #5a32a3;
}

/* 회원가입 링크 스타일 */
.signup-link {
    color: #6f42c1; /* 보라색 글자 */
    text-decoration: none; /* 밑줄 없애기 */
    text-align: center; /* 가운데 정렬 */
    display: block; /* 블록 요소로 만들어서 가운데 정렬되도록 설정 */
    margin-top: 15px; /* 위쪽 여백 추가 */
    font-size: 16px;
    font-weight: bold;
}

.signup-link:hover {
    color: #5a32a3; /* hover 시 색상 변경 */
}

/* 전체적인 여백과 균형 */
.mb-3 {
    margin-bottom: 20px; /* 입력 필드 간격 조정 */
}

/* 반응형 스타일 */
@media (max-width: 576px) {
    .container {
        margin: 20px auto; /* 화면이 작아질 때 상단 여백 축소 */
        padding: 15px;
    }
    .btn-primary {
        font-size: 16px; /* 버튼 크기 축소 */
    }
    .signup-link {
        font-size: 14px; /* 링크 크기 축소 */
    }
}
</style>
