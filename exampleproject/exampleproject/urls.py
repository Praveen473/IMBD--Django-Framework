"""
URL configuration for exampleproject project.

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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from exam1.views import WatchListAV,WatchDetailAV,ReviewList,ReviewDetails,ReviewCreate,WatchListGv,UserReview,StreamPlatformVs,StreamDetailAV,StreamPlatformAV
# from exam1 import views
router=DefaultRouter()
router.register('str',StreamPlatformVs, basename='streamplatform')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('List/',WatchListAV.as_view(),name='movie-list'),
    path('List2/',WatchListGv.as_view(),name='movie-list2'),
    path('<int:pk>/',WatchDetailAV.as_view(),name='movie-details'),
    path('',include(router.urls)),
    path('account/',include('user_app.api.urls')),
    # path('api-auth/',include('rest_framework.urls')),
    # path('Stream/<int:pk>',StreamDetailAV.as_view(),name='streamplatform-detail'),
    # path('Stream/',StreamPlatformAV.as_view(),name='Stream-list'),
    path('<int:pk>/Review/',ReviewList.as_view(),name='Review-List'),
    path('<int:pk>/Review-Created/',ReviewCreate.as_view(),name='Review-List'),
    path('Review/<int:pk>/',ReviewDetails.as_view(),name='Review-Detail'),
    path('Review/',UserReview.as_view(),name='User-Review-Detail'),
    # path('Review',ReviewList.as_view(),name='Review-List'),
    # path('Review/<int:pk>',ReviewDetails.as_view(),name='Review-Detail'),
]
