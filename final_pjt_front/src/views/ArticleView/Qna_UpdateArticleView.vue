<template>
  <div class="container">
    <div class="text-center main-title pb-3">
      <h1 style="font-weight: bold;">Update Post</h1>
    </div>
    <div class="row justify-content-center">
        <div class="card" style="width: 80%;">
          <form @submit.prevent="updateArticle" ref="form">
            <div class="form-group">
              <label for="title" class="mb-1">Title</label>
              <input
                type="text"
                id="title"
                class="form-control"
                v-model="updatetitle"
                maxlength="40"
              />
              <small class="form-text text-muted">40자 이내로 작성해주세요.</small>
            </div>
            <div class="form-group">
              <label for="content" class="mb-1">Content</label>
              <textarea
                id="content"
                class="form-control"
                v-model="updatecontent"
                rows="4"
              ></textarea>
            </div>
            <button
              type="submit"
              class="btn btn-warning "
            >
              SAVE
            </button>
          </form>
        </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useArticleStore } from "@/stores/article.js";
import { useRoute, useRouter } from "vue-router";
import swal from "sweetalert";

const articleStore = useArticleStore();
const updatetitle = ref("");
const updatecontent = ref("");
const route = useRoute();
const router = useRouter();

watch(
() => articleStore.Article,
(pastData) => {
  updatetitle.value = pastData.title;
  updatecontent.value = pastData.content;
}
);
const article_temp_idx = Number(route.params.id)
// 입장 시 데이터 불러오기
onMounted(() => {
articleStore.ReadDetailArticle('qna', route.params.id);

});

// 제출 시 데이터 수정
const updateArticle = function () {
swal({
  title: "수정할까요?",
  icon: "info",
  buttons: true,
}).then((willUpdate) => {
  if (willUpdate) {
    const databox = {
      title: updatetitle.value,
      content: updatecontent.value,
    };
    articleStore.UpdateDetailArticle('qna',route.params.id, databox);
    console.log(databox , route.params.id);
    
    swal("성공적으로 수정되었습니다!", {
      icon: "success",
    });
    // communityView.vue로 이동
    router.push({ name: "qna_detailarticle", params: { id: route.params.id } ,     
    query : {
      nickname: route.query.nickname,
      img: route.query.img,
      creatorId: route.query.creatorId,
    },
  });
  }
});
};
</script>

<style scoped>
 .container {
  width: 100%;
  max-width: 800px; /* 최대 너비 설정 */
  padding: 20px;
  margin: 0 auto; /* 화면 중앙 정렬 */
}

.main-title {
  text-align: center;
  color: #7a6db3; /* 보라색 타이틀 */
  margin-bottom: 30px; /* 타이틀과 폼 간의 간격 */
}

.row {
  display: flex;
  justify-content: center;
}

.card {
  padding: 25px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  border-radius: 12px; /* 둥근 카드 모서리 */
  background-color: #fff;
  width: 100%;
  max-width: 700px; /* 카드 너비 제한 */
}

.form-group {
  margin-bottom: 20px; /* 입력란 간의 간격 */
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px; /* 입력란 둥글게 */
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #7a6db3; /* 포커스 시 보라색 테두리 */
  outline: none; /* 포커스 시 아웃라인 제거 */
}

.btn-warning {
  width: 100%;
  padding: 15px;
  background-color: #7a6db3; /* 보라색 배경 */
  color: white;
  border: none;
  border-radius: 6px; /* 둥근 버튼 */
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-warning:hover {
  background-color: #5a34a2; /* 버튼 hover 시 어두운 보라색 */
}

.btn-warning:active {
  background-color: #4a2b82; /* 버튼 클릭 시 더 어두운 보라색 */
}

/* SweetAlert 타이틀 스타일 */
.swal-title {
  font-size: 20px;
  color: #6f42c1; /* 보라색 */
  font-weight: bold;
}

/* SweetAlert 텍스트 스타일 */
.swal-text {
  font-size: 16px;
  color: #333; /* 어두운 회색 */
}

/* SweetAlert 버튼 스타일 */
.swal-button {
  background-color: #6f42c1 !important;/* 보라색 */
  color: white !important;
  border-radius: 6px !important;
  padding: 10px 20px !important;
  font-size: 16px !important;
  transition: background-color 0.3s !important;
}
</style>

