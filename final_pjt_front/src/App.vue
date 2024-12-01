<template>
  <div class="container">
    <nav>
      <ul class="nav nav-pills center-nav" >
        <!-- <li class="nav-item">
          <RouterLink class="nav-link custom-link" :class="{ active: isActive('/RecommendView/agerecommend') }" to="/RecommendView/agerecommend">상품추천</RouterLink>
        </li> -->
        <li class="nav-item">
          <RouterLink to="/">
            <img :src="doge" alt="로고" class="nav-logo" >
          </RouterLink>
        </li>
        <li class="nav-item dropdown" @mouseenter="showDropdown">
          <RouterLink class="nav-link custom-link custom-dropdown" to="/deposit" role="button" aria-expanded="false">
            <img :src="bankImage" alt="" width="35px;" height="auto;">
          </RouterLink>
          <ul class="dropdown-menu dropdown-animated" v-show="dropdownVisible" @mouseleave="hideDropdown">
            <li><RouterLink class="dropdown-item custom-dropdown-item-1" to="/deposit">예금</RouterLink></li>
            <li><RouterLink class="dropdown-item custom-dropdown-item-1" to="/saving">적금</RouterLink></li>
            <!-- <li><RouterLink class="dropdown-item custom-dropdown-item-1" to="/recommendByAge">나이별 추천상품</RouterLink></li>
            <li><RouterLink class="dropdown-item custom-dropdown-item-1" to="/goalTypeRecommendView">목표별 추천상품</RouterLink></li> -->
          </ul>
        </li>
        <li class="nav-item dropdown" @mouseenter="showDropdown">
          <RouterLink class="nav-link custom-link custom-dropdown" to="/ArticleView/community" role="button" aria-expanded="false">
            <img :src="articleImage" alt="" width="35px;" height="auto;">
          </RouterLink>
          <ul class="dropdown-menu dropdown-animated" v-show="dropdownVisible" @mouseleave="hideDropdown">
            <li><RouterLink class="dropdown-item custom-dropdown-item-2" to="/ArticleView/community">커뮤니티</RouterLink></li>
            <li><RouterLink class="dropdown-item custom-dropdown-item-2" to="/ArticleView/goal_community">목표</RouterLink></li>
            <li><RouterLink class="dropdown-item custom-dropdown-item-2" to="/ArticleView/qna_community">Q&A</RouterLink></li>
            
          </ul>
        </li>
        
        <li class="nav-item">
          <RouterLink class="nav-link custom-link" :class="{ active: isActive('/exchangerate') }" to="/exchangerate">
            <img :src="main_moneyImage" alt="" width="35px;" height="auto;">
          </RouterLink>
        </li>
        <li class="nav-item dropdown" @mouseenter="showDropdown">
          <RouterLink class="nav-link custom-link custom-dropdown" to="/bank" role="button" aria-expanded="false">
            <img :src="main_mapImage" alt="" width="35px;" height="auto;">
          </RouterLink>
          <ul class="dropdown-menu dropdown-animated" v-show="dropdownVisible" @mouseleave="hideDropdown">
            <li><RouterLink class="dropdown-item custom-dropdown-item-3" to="/bank">은행</RouterLink></li>
            <li><RouterLink class="dropdown-item custom-dropdown-item-3" to="/atm">ATM</RouterLink></li>
          </ul>
        </li>
        <template v-if="userStore.isLogin">
          <li class="nav-item">
            <form @submit.prevent="logOut">
              <button type="submit" class="nav-link" style="background: none; border: none; padding: 0;">
                <img :src="logoutImage" alt="로그아웃" style="width: 50px; height: auto;">
              </button>
            </form>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" :class="{ active: isActive('/profile') }" to="/profile">
              <img :src="profileImage" alt="" width="35px;" height="auto;">
            </RouterLink>
          </li>
        </template>
        <template v-else>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" :class="{ active: isActive('/login') }" to="/login">
              <img :src="loginImage" alt="" width="35px;" height="auto;">
            </RouterLink>
          </li>
        </template>
      </ul>
    </nav>
  </div>
  <div style="margin-bottom: 10px;"></div>
  <RouterView />
  <!-- <UpdateSignup/> -->
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { useUserStore } from './stores/userStore';
import UpdateSignup from '@/components/UpdateSignup.vue';
import bankImage from '@/assets/bank.gif'; // 기본 이미지 경로 설정
import articleImage from '@/assets/article.gif';
import main_moneyImage from '@/assets/main_money.gif';
import loginImage from '@/assets/login.gif';
import main_mapImage from '@/assets/main_map.gif';
import profileImage from '@/assets/profile.gif';
import logoutImage from '@/assets/logout.gif';
import doge from '@/assets/dogebank.png'

const userStore = useUserStore()

const route = useRoute();
const dropdownVisible = ref(false);

function showDropdown() {
  dropdownVisible.value = true;
}

function hideDropdown() {
  dropdownVisible.value = false;
}

function isActive(path) {
  return route.path === path;
}

const logOut = function() {
  userStore.logOut()
}

</script>

<style scoped>
nav {
  padding: 10px 5px 15px 5px;
  font-weight: bold;
  border-bottom: 5px solid purple;
  margin-bottom: 10px;
}

.nav-item {
  margin: 0 10px; /* 양쪽 여백을 15px로 설정하여 간격 넓히기 */
  align-items: center; /* 아이템 내 요소들 가운데 정렬 */
}

/* 공통 링크 스타일: 글자 색 검정색, 배경색 제거 */
.custom-link {
  color: black !important;
  background-color: transparent !important;
}

.custom-link:hover {
  color: purple !important; /* 원하는 색으로 변경 */
}

/* 드롭다운 옆 화살표 제거 */
.custom-dropdown::after {
  content: none;
}

/* 드롭다운 메뉴 박스 크기를 텍스트에 맞추도록 설정 */
.dropdown-menu {
  min-width: auto;
  padding: 0px;
  margin-top: 0;
  border-top: 5px solid purple;
  border-radius: 0;
  white-space: nowrap;
}

/* 드롭다운 항목 기본 스타일 */
.custom-dropdown-item-1 {
  color: black !important;
  background-color: transparent !important;
  transition: color 0.3s;
  text-align: center; /* 글씨를 가운데 정렬 */
  padding: 5px 20px 5px 20px; /* 상하 5px, 좌우 10px으로 설정 */
  /* transform: translateX(10%); */
}

/* 드롭다운 항목 기본 스타일 */
.custom-dropdown-item-2 {
  color: black !important;
  background-color: transparent !important;
  transition: color 0.3s;
  text-align: center; /* 글씨를 가운데 정렬 */
  padding: 5px 10px 5px 11px; /* 상하 5px, 좌우 10px으로 설정 */
}

/* 드롭다운 항목 기본 스타일 */
.custom-dropdown-item-3 {
  color: black !important;
  background-color: transparent !important;
  transition: color 0.3s;
  text-align: center; /* 글씨를 가운데 정렬 */
  padding: 5px 20px 5px 20px; /* 상하 5px, 좌우 10px으로 설정 */
}

/* 드롭다운 항목 마우스 오버 시 글자색 보라색 */
.custom-dropdown-item-1:hover {
  color: purple !important;
  font-weight: bold;
}

.custom-dropdown-item-2:hover {
  color: purple !important;
  font-weight: bold;
}

/* 드롭다운 메뉴 애니메이션 설정 */
.dropdown-animated {
  display: block;
  opacity: 0;
  /* transform: translateY(-50px); */
  /* transition: opacity 0.3s ease, transform 0.3s ease; */
  margin-top: 15px;
  border-top: 5px solid purple;
  width: auto;
  white-space: nowrap;
  border-radius: 0; /* 모서리 둥근 부분 제거 */
}

/* 드롭다운 메뉴가 활성화될 때 서서히 나타나도록 설정 */
.nav-item.dropdown:hover .dropdown-menu {
  opacity: 1;
  transform: translateY(0);
}

/* 네비게이션 바 가운데 정렬 */
.center-nav {
  display: flex;
  justify-content: center;
  margin-top: 1px;
}

input[type="submit"] {
  color: black !important;
  background-color: transparent !important;
  border: none;
  padding: 8px 0px; /* 적절한 패딩값 추가 */
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem; /* 글씨 크기 설정 */
  line-height: 0.5; /* 다른 nav-link와 높이를 맞추기 위해 추가 */
  width: 70px;
  border-radius: 5px; /* 버튼에 둥근 모서리 추가 (선택사항) */
}

.nav-logo {
  width: 150px; /* 원하는 너비로 조절 */
  height: 100%; /* 비율 유지 */
  padding: 0;
  margin: 0;
}


</style>
