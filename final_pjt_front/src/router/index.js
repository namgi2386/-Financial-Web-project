import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignUpView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import DepositProductView from '@/views/DepositProductView.vue'
import DetailArticleView from '@/views/ArticleView/DetailArticleView.vue'
import MainView from '@/views/MainView.vue'
import UserProfileView from '@/views/UserProfileView.vue'
import SavingsProductView from '@/views/SavingsProductView.vue'
import Map from '@/components/Map/Map.vue'
import Bank from '@/components/Map/Bank.vue'
import AtmBody from '@/components/Map/AtmBody.vue'

import CommunityView from '@/views/ArticleView/CommunityView.vue'
import CreateArticleView from '@/views/ArticleView/CreateArticleView.vue'
import UpdateArticleView from '@/views/ArticleView/UpdateArticleView.vue'


import AgeRecommendView from '@/components/Recommend/AgeRecommend.vue'
import MbtiRecommendView from '@/components/Recommend/MbtiRecommend.vue'
import PrivateRecommendView from '@/components/Recommend/PrivateRecommend.vue'


import Qna_CreateArticleView from '@/views/ArticleView/Qna_CreateArticleView.vue'
import Qna_CommunityView from '@/views/ArticleView/Qna_CommunityView.vue'
import Qna_DetailArticleView from '@/views/ArticleView/Qna_DetailArticleView.vue'
import Qna_UpdateArticleView from '@/views/ArticleView/Qna_UpdateArticleView.vue'
import Goal_CreateArticleView from '@/views/ArticleView/Goal_CreateArticleView.vue'
import Goal_CommunityView from '@/views/ArticleView/Goal_CommunityView.vue'
import Goal_DetailArticleView from '@/views/ArticleView/Goal_DetailArticleView.vue'
import Goal_UpdateArticleView from '@/views/ArticleView/Goal_UpdateArticleView.vue'
import UpdateSignup from '@/components/UpdateSignup.vue'
import SignDeposit from '@/components/SignDeposit.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/login',
      name: 'login',
      component: LoginView
    },
    {
      path:'/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path:'/profile',
      name: 'profile',
      component: UserProfileView
    },
    {
      path:'/exchangerate',
      name: 'exchangerate',
      component: ExchangeRateView
    },
    {
      path:'/deposit',
      name:'deposit',
      component: DepositProductView
    },
    
    {
      path:'',
      name:'main',
      component: MainView
    },
    {
      path: '/saving',
      name: 'saving',
      component: SavingsProductView
    },
    {
      path: '/map',
      name: 'map',
      component: Map,
    },
    {
      path: '/atm',
      name: 'atm',
      component: AtmBody,
    },
    {
      path: '/bank',
      name: 'bank',
      component: Bank,
    },

    // free게시판
    {
      path:'/ArticleView/createarticle',
      name: 'createarticle',
      component: CreateArticleView
    },
    {
      path:'/ArticleView/community',
      name:'community',
      component: CommunityView
    },
    {
      path: '/ArticleView/detailarticle/:id',
      name: 'detailarticle',
      component: DetailArticleView
    },
    {
      path: '/ArticleView/updatearticle/:id',
      name: 'updatearticle',
      component: UpdateArticleView
    },
    // 질문게시판
    {
      path:'/ArticleView/qna_createarticle',
      name: 'qna_createarticle',
      component: Qna_CreateArticleView
    },
    {
      path:'/ArticleView/qna_community',
      name:'qna_community',
      component: Qna_CommunityView
    },
    {
      path: '/ArticleView/qna_detailarticle/:id',
      name: 'qna_detailarticle',
      component: Qna_DetailArticleView
    },
    {
      path: '/ArticleView/qna_updatearticle/:id',
      name: 'qna_updatearticle',
      component: Qna_UpdateArticleView
    },

    //목표게시판
    {
      path:'/ArticleView/goal_createarticle',
      name: 'goal_createarticle',
      component: Goal_CreateArticleView
    },
    {
      path:'/ArticleView/goal_community',
      name:'goal_community',
      component: Goal_CommunityView
    },
    {
      path: '/ArticleView/goal_detailarticle/:id',
      name: 'goal_detailarticle',
      component: Goal_DetailArticleView
    },
    {
      path: '/ArticleView/goal_updatearticle/:id',
      name: 'goal_updatearticle',
      component: Goal_UpdateArticleView
    },

    {
      path: '/updatesignup',
      name: 'updatesignup',
      component: UpdateSignup
    },

    // 추천게시판 3개 링크
    {
      path: '/recommendByAge',
      name: 'recommendByAge',
      component: AgeRecommendView
    },
    {
      path: '/recommendByMBTI',
      name: 'recommendByMBTI',
      component: MbtiRecommendView
    },
    {
      path: '/recommendByPrivate',
      name: 'recommendByPrivate',
      component: PrivateRecommendView
    },
    {
      path: '/signdeposit',
      name: 'signdeposit',
      component: SignDeposit
    }


  ],
})

export default router
