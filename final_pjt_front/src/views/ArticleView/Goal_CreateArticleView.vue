<template>
  <div class="container">
    <div class="text-center main-title pb-3">
      <h1 style="font-weight: bold;">목표 공유</h1>
    </div>
    <div class="row justify-content-center">
      <div class="card" style="width: 80%;">
        <form @submit.prevent="newArticle" ref="form" class="form">
          <div class="form-group">
            <label for="title" class="mb-1">Title</label>
            <input
              type="text"
              id="title"
              v-model="newtitle"
              :maxlength="40"
              required
              placeholder="Enter title"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="content" class="mb-1">Content</label>
            <textarea
              id="content"
              v-model="newcontent"
              rows="4"
              required
              placeholder="Enter content"
              class="form-control"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-save">SAVE</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  import { ref } from "vue";
  import { useArticleStore } from "@/stores/article.js";
  import swal from "sweetalert";
  import router from "@/router";
  
  const articleStore = useArticleStore();
  const newtitle = ref("");
  const newcontent = ref("");
  
  const newArticle = async function () {
  try {
    // 사용자가 게시글 생성을 확인하는 Swal
    const willCreate = await swal({
      title: "게시글을 생성할까요?",
      text: "목표를 공유해봐요!",
      icon: "info",
      buttons: [true, "생성하기!"],
    });

    // 사용자가 "생성하기!"를 클릭한 경우
    if (willCreate) {
      const databox = {
        title: newtitle.value,
        content: newcontent.value,
      };

      // 게시글 생성 요청
      await articleStore.CreateArticle('goal', databox);
      
      // 게시글 생성 후 데이터 갱신
      await articleStore.ReadArticles('goal'); // 카테고리 정보도 추가

      swal("성공적으로 생성되었어요!", {
        icon: "success",
      });

      // communityView.vue로 이동
      router.push({ name: "goal_community" });

    } else {
      // 사용자가 "취소"를 클릭한 경우
      swal("게시글 생성을 취소했어요.", {
        icon: "info",
      });
    }
  } catch (err) {
    // 에러 발생 시 처리
    console.error(err);
    swal("게시글 생성에 실패했어요!", {
      icon: "error",
    });
  }
};

// const gohome = function() {
//   router.push({name:'community'})
// }
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

.btn-save {
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

.btn-save:hover {
  background-color: #5a34a2; /* 버튼 hover 시 어두운 보라색 */
}

.btn-save:active {
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


