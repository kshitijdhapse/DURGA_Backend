from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'products', FoodItemViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('branches/', BranchSelectAPI.as_view(), name = 'Branches'),
    path('menu/', FoodDetail.as_view(), name = 'Menu'),
    path('menu/<str:branch>/',BranchMenuAPI.as_view(),name='branch-menu'),
    path('othermenu/<str:branch>/',OtherBranchMenuAPI.as_view(),name='other-branch-menu'),
    path('api/', include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('addbranchitem/',AddToBranchMenu.as_view(),name='add'),
    path('updateprice/',UpdateBranchMenuPriceAPI.as_view(),name='update'),
]