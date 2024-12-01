"""
URL configuration for mypjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import custom_signup
from accounts.views import user_delete
from accounts.views import getmyprofile
from accounts.views import getmyfininfo
from accounts.views import getDetailprofile

from django.conf.urls.static import static
from django.conf import settings

from accounts.views import like_product_deposit
from accounts.views import unlike_product_deposit
from accounts.views import get_liked_products_deposit
from accounts.views import toggle_love
from accounts.views import get_my_love_products
from accounts.views import get_product_loves

from accounts.views import like_product_saving
from accounts.views import unlike_product_saving
from accounts.views import get_liked_products_saving
from accounts.views import toggle_love_saving
from accounts.views import get_my_love_products_saving
from accounts.views import get_product_loves_saving

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finlife/', include('finlife.urls')),
    path('exchange_rate/', include('exchange_rate.urls')),
    path('article/', include('article.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('hot/' , include('hot.urls')),
    # path('accounts/signup/', include('dj_rest_auth.registration.urls')), 절대 주석 풀지마
    path('accounts/signup/', custom_signup),  
    path('accounts/delete/<str:username>/', user_delete),
    path('accounts/profile/', getmyprofile),
    path('accounts/fininfo/' , getmyfininfo),
    path('accounts/profile/<int:user_id>/' , getDetailprofile),


    path('like_product/deposit/<str:fin_prdt_cd>/', like_product_deposit), # 찜하기
    path('unlike_product/deposit/<str:fin_prdt_cd>/' , unlike_product_deposit), # 찜삭제하기
    path('get_liked_products/deposit/',get_liked_products_deposit), # 찜조회하기
    path('like-product/deposit/<str:fin_prdt_cd>/', toggle_love, name='toggle_love'), # 좋아요 추가 제거하기
    path('liked-products/deposit/', get_my_love_products, name='get_my_love_products'), # 좋아요한 상품 목록
    path('product-likes/deposit/<str:fin_prdt_cd>/', get_product_loves, name='get_product_loves'), # 해당 상품 좋아요 수 조회

    path('like_product/saving/<str:fin_prdt_cd>/', like_product_saving),
    path('unlike_product/saving/<str:fin_prdt_cd>/' , unlike_product_saving),
    path('get_liked_products/saving/',get_liked_products_saving),
    path('like-product/saving/<str:fin_prdt_cd>/', toggle_love_saving, name='toggle_love_saving'),
    path('liked-products/saving/', get_my_love_products_saving, name='get_my_love_products_saving'),
    path('product-likes/saving/<str:fin_prdt_cd>/', get_product_loves_saving, name='get_product_loves_saving'),




    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
