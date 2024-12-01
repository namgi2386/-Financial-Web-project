from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render , get_object_or_404
from .models import ArticleFree , FreeRecommend
from .serializers import ArticleFreeSerializer , ArticleFreeListSerializer , FreeRecommendedSerializer


@api_view(['GET', 'POST']) # 전체 게시글조회 , 글쓰기
def free_list(request , category_name):
    if request.method == 'GET':
        articles = ArticleFree.objects.filter(category=category_name)
        print('ee')
        serializer = ArticleFreeListSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['category'] = category_name
        print(data)
        serializer = ArticleFreeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE','GET' , 'PUT']) # 특정 게시글 조회, 수정 , 삭제
def free_detail(request,category_name, free_pk):
    article = get_object_or_404(ArticleFree, pk=free_pk, category=category_name)
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = ArticleFreeSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ArticleFreeSerializer(article, data=request.data , partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(category=category_name )
            return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['DELETE','PUT']) # 특정댓글 수정 삭제
def free_recommend_delete(request,category_name, recommend_pk):
    recommend = get_object_or_404(FreeRecommend, pk=recommend_pk)
    if request.method == 'DELETE':
        if request.user != recommend.recommend_user:
            return Response({"error": "권한이 없습니다." }, status=status.HTTP_403_FORBIDDEN)
        recommend.delete()
        return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        print(recommend)
        print(request.data)
        serializer = FreeRecommendedSerializer(recommend, data=request.data , partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(recommend_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET','POST']) # 특정게시글에 댓글 조회 댓글작성
def free_recommend_create(request,category_name, free_pk):
    articlefree = get_object_or_404(ArticleFree, pk=free_pk, category=category_name)
    if request.method == 'GET':
        recommends = FreeRecommend.objects.filter(articlefree=free_pk)
        serializer = FreeRecommendedSerializer(recommends , many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = FreeRecommendedSerializer(data = request.data )
        if serializer.is_valid(raise_exception=True):
            serializer.save(articlefree=articlefree , recommend_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
