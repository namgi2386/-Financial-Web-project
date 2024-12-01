import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import { useCommentStore } from './comment';

// import { useRouter } from 'vue-router';

export const useArticleStore = defineStore('article', () => {

  // 특정 카테고리 전체글 조회
  const commentStore = useCommentStore()

  const Articles = ref([]);

  const ReadArticles = function (category_name) {
  const token = localStorage.getItem('token');
  return axios({
    method: 'GET',
    url: `http://localhost:8000/article/free/${category_name}/`,
    headers: { Authorization: `Token ${token}` }
  })
    .then((res) => {
      console.log('ee');
      
      console.log(res.data);
      Articles.value = res.data;
    })
    .catch((err) => {
      console.log("get err");
      
      console.error(err);
      throw err; // 에러를 다시 던져 호출한 쪽에서 처리 가능하도록
    });
};

  // 특정 카테고리 글쓰기
  const CreateArticle = function(category_name , databox){
    const { title , content } = databox
    const token = localStorage.getItem('token');
    console.log(category_name);
    console.log(databox);
    axios({
      method : 'POST',
      url : `http://localhost:8000/article/free/${category_name}/`,
      data : { title , content},
      headers: {Authorization: `Token ${token}`}
    }).then((res)=>{
      console.log(res.data);
    }).catch(err => console.log(err)
  )}

  // 특정 카테고리 특정글 조회
  const Article = ref(null)
  const ArticlesComments = ref([])
  const ReadDetailArticle = function(category_name,article_pk){
    // const router = useRouter();
    const token = localStorage.getItem('token');
    axios({
      method : 'GET',
      url : `http://localhost:8000/article/free/${category_name}/${article_pk}/`,
      headers: {Authorization: `Token ${token}`}
    }).then((res)=>{
      console.log(res.data);
      Article.value = res.data
      ArticlesComments.value = res.data.freerecommend_set
      console.log(ArticlesComments.value);
      commentStore.GETRecommend(category_name, article_pk)
      
      // router.push({name:'detailarticle'})
    }).catch(err => console.log(err)
  )}

    // 특정 카테고리 특정글 수정

    const UpdateDetailArticle = function(category_name, article_pk , databox){
      const { title , content } = databox
      console.log('inner');
      console.log(category_name);
      console.log(article_pk);
      console.log(databox);
      
      const token = localStorage.getItem('token');
      axios({
        method : 'PUT',
        url : `http://localhost:8000/article/free/${category_name}/${article_pk}/`,
        data : {
          title,
          content
        },
        headers: {Authorization: `Token ${token}`}
      }).then((res)=>{
        console.log(res.data);
      }).catch(err => console.log(err)
    )}
    
    // 특정 카테고리 특정글 삭제
    const DeleteDetailArticle = function(category_name,article_pk){
      const token = localStorage.getItem('token');
      axios({
        method : 'DELETE',
        url : `http://localhost:8000/article/free/${category_name}/${article_pk}/`,
        headers: {Authorization: `Token ${token}`}
      }).then((res)=>{
        console.log(res.data);
      }).catch(err => console.log(err)
    )}

  return { ReadArticles,CreateArticle,
    ReadDetailArticle,UpdateDetailArticle,
    DeleteDetailArticle,Articles,Article , ArticlesComments 
  }
})