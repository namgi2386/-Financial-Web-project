from django.urls import path
from . import views

app_name = 'finlife'

urlpatterns = [
    path('api_test/',views.api_test , name="api_test"), # 테스트 GET
    path('save-deposit-products/', views.save_deposit_products, name="save_deposit_products"), # 정기예금 상품 목록 DB에 저장

    path('deposit/products/', views.deposit_products, name="deposit_products"),# 전체상품 GET PUSH
    path('deposit/options/', views.deposit_options, name='deposit_options'), # 옵션 전체 GET

    path('deposit/product/<str:fin_prdt_cd>/' , views.deposit_product , name="deposit_product"), # 특정 상품
    path('deposit/product/<str:fin_prdt_cd>/options/', views.deposit_product_options, name="deposit_product_options"), # 특정 상품의 옵션들

    path('deposit/products/bank/<str:kor_co_nm>/' , views.deposit_products_filter_bank , name='deposit_products_filter_bank' ), # 은행기준 필터링
    path('deposit/products/period/<str:save_trm>/', views.deposit_products_filter_period , name='deposit_products_filter_period'), # 기간기준 필터링


    path('api_test_saving/' , views.api_test_saving , name='api_test_saving'), # 테스트 적금전용
    path('save-saving-products/', views.save_saving_products, name="save_saving_products"), # 적금 상품 목록 DB에 저장

    path('saving/products/', views.saving_products, name="saving_products"),# 전체상품 GET PUSH
    path('saving/options/', views.saving_options, name='saving_options'), # 옵션 전체 GET

    path('saving/product/<str:fin_prdt_cd>/' , views.saving_product , name="saving_product"), # 특정 상품
    path('saving/product/<str:fin_prdt_cd>/options/', views.saving_product_options, name="saving_product_options"), # 특정 상품의 옵션들

    path('saving/products/bank/<str:kor_co_nm>/' , views.saving_products_filter_bank , name='saving_products_filter_bank' ), # 은행기준 필터링
    path('saving/products/period/<str:save_trm>/', views.saving_products_filter_period , name='saving_products_filter_period'), # 기간기준 필터링
    path('saving/products/type/<str:rsrv_type_nm>/', views.saving_products_filter_type , name='saving_products_filter_type'), # 적립유형기준 필터링

    path('deposit/total/', views.deposit_products_with_options, name='deposit_products_with_options'),
    path('saving/total/', views.saving_products_with_options, name='saving_products_with_options'),
    

]