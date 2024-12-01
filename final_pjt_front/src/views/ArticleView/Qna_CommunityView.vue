<template>
  <div class="container">
    <div class="text-center main-title pb-0">
      <h1 class="title">Q&A 게시판</h1>
    </div>
    <div class="card my-4 mx-auto" style="max-width: 100%;">
      <div class="row justify-end">
        <div cols="auto" class="d-flex justify-content-end">
          <router-link :to="{name: 'qna_createarticle'}" class="mt-5 btn-new-post">New QUESTION</router-link>
        </div>
      </div>

      <!-- 게시글 테이블 -->
      <table class="table">
        <thead class="table-header">
          <tr>
            <th style="width: 10%;">No</th>
            <th style="width: 45%;">Title</th>
            <th style="width: 25%;">Nickname</th>
            <th style="width: 20%;">Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in paginatedItems" :key="index" @click="detailView(item.id, item.user_profile.nickname, item.user_profile.profile_img , item.user_profile.id)">
            <!-- {{ item }} -->
            <td>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
            <td>
              <span class="link-style">{{ item.title }}</span>
            </td>
            <td>
              <span>
                <img :src="`http://localhost:8000${item.user_profile.profile_img}`" alt="User Profile Image" class="avatar-img" />
              </span>
              <span >
                {{ item.user_profile.nickname }}
              </span>
            </td>
            <td>{{ formatDate(item.created_at) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- 페이지네이션 -->
      <div class="pagination mb-3">
        <button v-for="page in totalPages" :key="page" @click="updatePagination(page)" :class="{ active: currentPage === page }">
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useArticleStore } from "@/stores/article";
import { useRouter } from "vue-router";
import { format } from "date-fns";
import { useUserStore } from "@/stores/userStore";

const userStore = useUserStore();
const articleStore = useArticleStore();
const router = useRouter();

// 초기 데이터 선언
const items = ref([]);

onMounted(() => {
  userStore.getProfile();
});


// 날짜 변환 함수
const formatDate = (date) => {
  return format(new Date(date), "yyyy-MM-dd");
};

// 게시글 가져오기
onMounted(async () => {
  try {
    await articleStore.ReadArticles('qna'); // 비동기 호출
    items.value = articleStore.Articles; // 스토어의 데이터를 로컬 상태로 저장
  } catch (error) {
    console.error("게시글을 가져오는 중 오류 발생:", error);
  }
});

watch(
  () => articleStore.Articles,
  (newArticlesList) => {
    items.value = newArticlesList;
  },
  { immediate: true } // 초기 로드 시에도 업데이트
);

const itemsPerPage = 5;
const currentPage = ref(1);

const reversedItems = computed(() => [...items.value].reverse());
const totalPages = computed(() => Math.ceil(reversedItems.value.length / itemsPerPage));

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return reversedItems.value.slice(start, end);
});

const updatePagination = (page) => {
  currentPage.value = page;
};

const detailView = (articleId, nickname, img , creatorId) => {
  router.push({ name: "qna_detailarticle", params: { id: articleId }, query: { nickname: nickname, img: img , creatorId : creatorId } });
};
</script >

<style scoped>
.container {
    background-color: #ffffff; /* 밝은 흰색으로 변경 */
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    padding: 20px 30px; /* 여백을 조정해 더 균형 있게 설정 */
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15); /* 그림자 강조 */
    max-width: 1100px;
    margin: 0 auto;
  }

.main-title h1 {
  font-size: 2.5rem; /* 타이틀 크기 조정 */
  font-weight: bold;
  color: #333;
  margin-bottom: 20px; /* 상단 마진 추가 */
}

.btn-new-post {
  color: white;
  background-color: #8e7dbe; /* 보라색 버튼 */
  padding: 5px 20px;
  border: none;
  font-size: 15px;
  cursor: pointer;
  border-radius: 25px; /* 둥근 버튼 모양 */
  transition: background-color 0.3s ease;
  text-decoration: none; /* 밑줄 제거 */
  margin-bottom: 10px; /* 버튼과 게시글 간의 간격 추가 */
}

.btn-new-post:hover {
  background-color: #7a6db3; /* 보라색의 어두운 색상으로 변환 */
}


.link-style {
  text-decoration: none;
  color: #333; /* 기본 글자 색은 어두운 회색 */
  font-weight: 600;
  transition: color 0.3s ease;
}

.link-style:hover {
  color: #8e7dbe; /* 보라색으로 변환 */
  cursor: pointer;
}

.nick-color {
  color: #8e7dbe; /* 프로필 페이지와 어울리는 보라색 */
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.pagination button {
  background: none;
  border: none; /* 기존 border 제거 */
  padding: 10px 18px;
  cursor: pointer;
  font-size: 16px;
  color: #8e7dbe; /* 보라색으로 변경 */
  transition: color 0.3s ease; /* 색상 변화 애니메이션 추가 */
  text-align: center; /* 텍스트 중앙 정렬 */
  display: inline-block; /* 버튼을 인라인 블록 요소로 설정 */
}

.pagination button:hover {
  color: #7a6db3; /* 호버 시 보라색의 어두운 색상으로 변경 */
}

.pagination button:focus {
  outline: none; /* 버튼 클릭 시 테두리 없애기 */
}


.avatar-img {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 10px; /* 이미지와 이름 간격 조정 */
}

.table {
  margin-top: 5px;
  margin-bottom: 20px;
  padding: 10px;
  font-size: 15px;
  background-color: #fafafa; /* 테이블 배경색 */
  border-radius: 10px; /* 테이블 모서리 둥글게 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  border-top: 1.5px solid black;
}

.card {
  padding: 1px 20px 5px 20px;
  background-color: #fafafa;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* 카드 그림자 추가 */
}

/* 테이블 헤더 */
.table-header {
  background-color: #f1f1f1; /* 부드러운 그라데이션 느낌 */
  color: #333; /* 진한 텍스트 */
  
}

.table th, .table td {
  text-align: center; /* 테이블 내용 중앙 정렬 */
  vertical-align: middle;
}

.table th {
  background-color: #f0f0f0; /* 헤더 배경색 */
  font-weight: bold;
  color: #333; /* 글자색 */
}

.title {
  font-family: 'Godo', sans-serif;
}

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}

.avatar-img {
  width: 35px; /* 프로필 이미지 크기 */
  height: 35px; /* 프로필 이미지 크기 */
  border-radius: 50%; /* 둥근 모서리 */
  margin-right: 8px; /* 이미지와 닉네임 간의 간격 */
}
</style>
