from django.urls import path
from . import views

urlpatterns = [
    path('recommendByAge/' , views.recommendByAge),
    path('recommendByMBTI/' , views.recommendByMBTI),
    path('recommendByPrivateDeposit/' , views.recommendByPrivateDeposit),
    path('recommendByPrivateSaving/' , views.recommendByPrivateSaving),
]