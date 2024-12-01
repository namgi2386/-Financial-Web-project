<template>
  <div v-if="articleStore.Article && userStore.profileData">
    
    <!-- 카드 영역 -->
    <div class="article-card">
      <div class="article-title">
        <h3>{{ articleStore.Article.title }}</h3>
      </div>

      <!-- 작성자 정보 -->
      <div class="article-subtitle">
        <div class="user-info">
          <img :src="`http://localhost:8000${image}`" alt="User Profile" class="avatar-img" />
          <span class="user-nickname">{{ nickname }}</span>
        </div>
        <!-- 로그인한 사용자와 게시글 작성자가 같으면 수정, 삭제 버튼 표시 -->
        <!-- <p>{{ userStore.profileData.id }}</p>
        <p>{{ creatorId }}</p> -->
          <div v-if="userStore.profileData.id == creatorId" class="article-actions">
            <button class="update-btn" @click="articleUpdate">Update</button>
            <button class="delete-btn" @click="articleDelete">Delete</button>
          </div>
      </div>

      <hr />
      <div class="article-content">
        <p>{{ articleStore.Article.content }}</p>
      </div>

      <!-- 작성일, 수정일 표시 -->
      <div class="article-dates">
        <div class="created-date">
          <span>Created Date:</span>
          <span>{{ formatDate(articleStore.Article.created_at) }} {{ formatTime(articleStore.Article.created_at) }}</span>
        </div>
        <div class="updated-date">
          <span>Updated Date:</span>
          <span>{{ formatDate(articleStore.Article.updated_at) }} {{ formatTime(articleStore.Article.updated_at) }}</span>
        </div>
      </div>

      <hr />
      <!-- 댓글 컴포넌트 -->
      <goal_Comments v-if="articleStore.Article && userStore.profileData" :Username="userStore.profileData.nickname" :articleUser="articleStore.Article.user" @commentAdded="handleCommentAdded() "/>
      <ul >
          <div v-for="reco in articleStore.ArticlesComments" :key="reco.id">
            <li>
              <!-- 수정 모드인지 확인 -->
              <template v-if="editMode === reco.id">
                <input 
                  v-model="editedContent" 
                  class="edit-input" 
                  placeholder="댓글을 수정하세요" 
                />
                <div>
                  <button @click="saveComment(reco.id)">저장</button>
                  <button @click="cancelEdit" style="margin-left:10px">취소</button>
                </div>
              </template>
              <template v-else>
                <div class="comment-content">
                  <!-- <img :src="`http://localhost:8000${image}`" alt="User Profile" class="comment-img" /> -->
                  <img :src="`http://localhost:8000${
                  commentStore.recommends.find(comment => comment.recommend_user === reco.recommend_user)?.recommend_user_profile_img || 'Unknown img'
                  }`" alt="User Profile" class="comment-img" />
                  {{ commentStore.recommends.find(comment => comment.recommend_user === reco.recommend_user)?.recommend_user_nickname || 'Unknown User' }}
                  : {{ reco.content }}
                </div>
                <div class="comment-actions">
                  <div  v-if="reco.recommend_user === userStore.profileData.id">
                    <button @click="removeComment(reco.id)" class="delete-button">삭제</button>
                    <button @click="editComment(reco)">수정</button>
                  </div>
                  <div v-else>

                  </div>
                </div>
              </template>
            </li>
          </div>
        </ul>
      <div v-if="articleStore.Article.freerecommend_set.length === 0" class="no-comments">
        가장 먼저 댓글을 달아보세요!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useArticleStore } from "@/stores/article";
import { useRoute, useRouter } from "vue-router";
import goal_Comments from "@/components/goal_Comments.vue";
import { format, parseISO } from "date-fns";
import { useUserStore } from "@/stores/userStore";
import { useCommentStore } from "@/stores/comment";

const articleStore = useArticleStore();
const commentStore = useCommentStore()
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const nickname = route.query.nickname; // 닉네임 데이터 읽기
const image = route.query.img
const creatorId = route.query.creatorId

// 로컬 상태
const editMode = ref(null); // 현재 수정 중인 댓글 ID
  const editedContent = ref(""); // 수정된 내용


onMounted(() => {
    userStore.getProfile();
    console.log(userStore.profileData);
});

const profileImg = computed(() => {
  return `http://localhost:8000${articleStore.Article.user.profile_img}`;
});

const articleUpdate = () => {
  router.push({
    name: "goal_updatearticle",
    params: { id: articleStore.Article.pk },
    query : {
      nickname: route.query.nickname,
      img: route.query.img,
      creatorId: route.query.creatorId,
    },
  });
};

const returnArticleList = () => {
  router.push({
    name: "goal_community",
  });
};

const articleDelete = () => {
  swal({
    title: "정말 삭제하실건가요?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      articleStore.DeleteDetailArticle('goal',articleStore.Article.id);
      swal("성공적으로 삭제 되었습니다!", {
        icon: "success",
      });
      // communityView.vue로 이동
      router.push({ name: "goal_community" });
    } else {
      swal("취소되었습니다!");
    }
  });
};

// 댓글 수정 시작
const editComment = (reco) => {
    console.log('--here-');
    
    console.log(reco.id)
    editMode.value = reco.id; // 수정 모드로 전환
    editedContent.value = reco.content; // 기존 내용 불러오기
  };

    // 댓글 수정 저장
const saveComment = async (reco) => {
  console.log(reco);
  
  if (editedContent.value.trim()) {
    try {
      // 서버에 수정된 댓글 내용 전송
      await commentStore.UpdateRecommend('goal', reco, editedContent.value);

      // 서버에서 댓글 목록 다시 가져오기
      // await articleStore.ReadDetailArticle('free', route.params.id);
      console.log(articleStore.ArticlesComments);
      
      articleStore.ArticlesComments = articleStore.ArticlesComments.map((recos) => {
      if (recos.id === reco) {  // reco는 수정하려는 댓글 객체입니다.
        console.log('---------------');
        return { ...recos, content: editedContent.value };  // content를 editedContent.value로 변경
      }
      return recos;
      });
      console.log(articleStore.ArticlesComments);
      // 수정 모드 해제
      editMode.value = null;
      editedContent.value = "";
    } catch (error) {
      console.error("댓글 저장 중 오류 발생:", error);
    }
  } else {
    alert("댓글 내용을 입력하세요.");
  }
};

// 댓글 수정 취소
const cancelEdit = () => {
  editMode.value = null; // 수정 모드 해제
  editedContent.value = ""; // 입력 초기화
};

onMounted(async() => {
  await articleStore.ReadDetailArticle('goal', route.params.id);
});
const formatDate = (dateString) => {
  return format(parseISO(dateString), "yyyy-MM-dd");
};

const formatTime = (dateString) => {
  return format(parseISO(dateString), "HH:mm:ss");
};

const handleCommentAdded = async () => {
  console.log('emmited');
  await articleStore.ReadDetailArticle('goal', route.params.id);
}

const removeComment = async (recoId) => {
  await commentStore.DeleteRecommend('goal', recoId);
  articleStore.ArticlesComments = articleStore.ArticlesComments.filter((recos) => recos.id != recoId )
};

</script>

<style scoped>
/* 버튼 스타일 */
.update-btn, .delete-btn, .returnBtn {
  background: none;
  border: none;
  cursor: pointer;
  font-weight: bolder;
  font-size: 18px;
}

.update-btn {
  color: #9b4de2; /* 보라색 */
  text-shadow: 0.5px 0.5px 0.5px rgba(155, 77, 226, 0.8);
}

.delete-btn {
  color: #e13e8e; /* 보라색 계열의 붉은색 */
  text-shadow: 0.5px 0.5px 0.5px rgba(225, 62, 142, 0.8);
}

.returnBtn {
  color: #6a2d8b; /* 보라색 */
  text-shadow: 0.5px 0.5px 0.5px rgba(106, 45, 139, 0.8);
}

/* 버튼 hover 효과 */
.update-btn:hover, .delete-btn:hover, .returnBtn:hover {
  opacity: 0.8; /* hover 시 투명도 감소 */
}


/* 카드 스타일 */
.article-card {
  margin: 50px auto;
  padding: 30px;
  width: 80%;
  max-width: 700px;
  border: 1px solid #dedede;
  border-radius: 10px;
  background-color: #fafafa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-title h3 {
  font-size: 2em;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.article-subtitle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info .avatar-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
  border: 2px solid #dedede;
}

.user-nickname {
  font-size: 1.2em;
  font-weight: 600;
  color: #555;
}

.article-actions button {
  margin-left: 15px;
  padding: 8px 15px;
}

.article-content {
  font-size: 1.2em;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.article-dates {
  font-size: 0.9em;
  color: #777;
  margin-bottom: 20px;
  text-align: right;
}

.article-dates span {
  margin-right: 15px;
}

hr {
  border: 0;
  height: 1px;
  background-color: #dedede;
  margin: 25px 0;
}

.font-style {
  font-size: small;
  color: gray;
}

.no-comments {
  text-align: center;
  color: #888;
  margin: 20px 0;
  font-size: 1.1em;
}

.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #9b4de2; /* 보라색 계열 */
  transition: color 0.3s ease;
}

.delete-button:hover {
  color: #7f3cc8; /* 보라색 hover */
}

/* 댓글 스타일 */
.edit-input {
  margin-right: 10px;
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ddd;
  width: 300px;
  font-size: 14px;
}


button {
  padding: 8px 10px;
  background-color: #8e7dbe;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}


/* 댓글 목록 */
ul {
  list-style-type: none;
  padding-left: 0;
}

ul > div {
  margin-bottom: 15px;
  margin-top: 10px;
}

ul > div > li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

ul > div > li:hover {
  background-color: #f1f1f1;
}

span {
  font-size: 0.9em;
  color: #666;
}

.comment-img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #dedede; 
}

</style>
  
