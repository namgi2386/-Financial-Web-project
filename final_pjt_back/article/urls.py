from django.urls import path
from . import views



urlpatterns = [
    path('free/<str:category_name>/', views.free_list), # 전체 게시글조회 , 글쓰기
    path('free/<str:category_name>/<int:free_pk>/', views.free_detail), # 특정 게시글 조회, 수정 , 삭제
    path('free/<str:category_name>/<int:free_pk>/recommends/' , views.free_recommend_create), # 특정게시글에 댓글들조회 작성
    path('free/<str:category_name>/<int:recommend_pk>/recommends/delete/', views.free_recommend_delete), # 특정댓글삭제

] # category_name >>> free , goal , qna
