<template>
  <div class="comment-section">
    <!-- 댓글 작성 폼 -->
    <form @submit.prevent="newComment" class="comment-form">
      <input
        v-model="comment"
        type="text"
        placeholder="댓글을 입력하세요"
        class="comment-input"
      />
      <button type="submit" class="submit-button">댓글 생성하기!</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useCommentStore } from "@/stores/comment";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores/userStore";


const route = useRoute();
const comment = ref("");
const commentStore = useCommentStore();
const userStore = useUserStore();


const emit = defineEmits();

const newComment = () => {
  const databox = {
    content: comment.value,
  };
  commentStore.CreateRecommend('qna', route.params.id,databox);
  comment.value = ""; // 댓글 입력 필드 초기화
  emit('commentAdded');
};



</script>

<style scoped>
.comment-section {
  max-width: 100%;
  margin: 0 auto;
}

.comment-container {
  margin: 10px 0;
}

.comment-item {
  margin-bottom: 15px;
  padding: 10px;
  border-bottom: 1px solid #dedede;
}

.comment-card {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-user-name {
  font-weight: bold;
  color: #4a4a4a;
}

.comment-actions {
  display: flex;
  gap: 5px;
}

.edit-button,
.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.edit-button {
  color: #007bff;
}

.delete-button {
  color: #ff4d4f;
}

.no-comments {
  text-align: center;
  color: #888;
  margin: 20px 0;
}

.comment-form {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.comment-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  padding: 10px 20px;
  border: none;
  background-color: #8e7dbe;
  color: white;
  cursor: pointer;
  border-radius: 20px;
}

.submit-button:hover {
  background-color: #7f3cc8;
}
</style>
