import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import { useArticleStore } from './article';

export const useCommentStore = defineStore('comment', () => {
  // 댓글 리스트 (로컬에서 상태 관리)
  const recommends = ref([]);
  const articleStore = useArticleStore()

  // 특정 카테고리 특정글 댓글 가져오기
  const GETRecommend = function(category_name, article_pk) {
    const token = localStorage.getItem('token');
    // recommends.value = null
    axios({
      method: 'GET',
      url: `http://localhost:8000/article/free/${category_name}/${article_pk}/recommends/`,
      headers: { Authorization: `Token ${token}` }
    })
    .then((response) => {
      recommends.value = response.data
    })
    .catch((err) => {
      console.error("댓글 로딩 중 오류 발생:", err);
    });
  };




  const CreateRecommend = function(category_name, article_pk, contentbox) {
    const token = localStorage.getItem('token');
    const content = contentbox.content;
    axios({
      method: 'POST',
      url: `http://localhost:8000/article/free/${category_name}/${article_pk}/recommends/`,
      data: { content },
      headers: { Authorization: `Token ${token}` }
    })
    .then((response) => {
      console.log("댓글추가");
      
      console.log(response.data);
      // 새 댓글 추가
      recommends.value.push(response.data);
      console.log('no1');
      
      console.log(recommends.value);
      console.log('no2');
      console.log(response.data);
      console.log(articleStore.ArticlesComments);
      articleStore.ArticlesComments.push(response.data)
      console.log(articleStore.ArticlesComments);
    })
    .catch((err) => {
      console.error("댓글 작성 중 오류 발생:", err);
    });
  };

  // 특정 카테고리 특정글 댓글 삭제
  const DeleteRecommend = function(category_name, recommend_pk) {
    const token = localStorage.getItem('token');
    
    axios({
      method: 'DELETE',
      url: `http://localhost:8000/article/free/${category_name}/${recommend_pk}/recommends/delete/`,
      headers: { Authorization: `Token ${token}` }
    })
    .then((res) => {
      console.log("삭제");
      
      console.log(res.data);
      console.log(recommends.value);
      
      // 로컬 상태에서 댓글 제거
      recommends.value = recommends.value.filter(
        (recommend) => recommend.id !== recommend_pk
      );
    })
    .catch((err) => {
      console.error("댓글 삭제 중 오류 발생:", err);
    });
  };

  // 댓글 수정
  const UpdateRecommend = function(category_name, recommend_pk, newContent) {
    const token = localStorage.getItem('token');
    axios({
      method: 'PUT',
      url: `http://localhost:8000/article/free/${category_name}/${recommend_pk}/recommends/delete/`,
      data: { content: newContent },
      headers: { Authorization: `Token ${token}` }
    })
    .then((response) => {
      // 로컬 상태 갱신
      // const recommendIndex = recommends.value.findIndex(
      //   (recommend) => recommend.id === recommend_pk
      // );
      // if (recommendIndex !== -1) {
      //   recommends.value[recommendIndex].content = newContent;
      //   console.log(`댓글이 수정되었습니다: ${newContent}`);
      // }
      recommends.value = recommends.value.filter(
        (recommend) => recommend.id !== recommend_pk
      );
    })
    .catch((error) => {
      console.error("댓글 수정 중 오류 발생:", error);
    });
  };

  return {
    recommends,
    CreateRecommend,
    DeleteRecommend,
    UpdateRecommend,
    GETRecommend,
  };
});
