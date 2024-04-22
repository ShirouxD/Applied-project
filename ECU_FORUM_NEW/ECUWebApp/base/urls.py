from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('thread/<str:pk>/', views.thread, name="thread"),
    path('profile/<str:pk>/', views.userProfile, name="user_profile"),
    path('create_thread/', views.createThread, name="create_thread"),
    path('update_thread/<str:pk>/', views.updateThread, name="update_thread"),
    path('delete_thread/<str:pk>/', views.deleteThread, name="delete_thread"),
    path('delete_comment/<str:pk>/', views.deleteComment, name="delete_comment"),
    path('update_user/', views.updateUser, name="update_user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('social_page/', views.socialPage, name="social_page"),
    path('social/create/', views.createSocialPost, name='create_social_post'),
    path('delete_social_post/<int:pk>/', views.deleteSocialPost, name="delete_social_post"),
    path('uni_map/', views.uniMap, name="uni_map"),
    path('reserve_room/', views.reserveRoom, name="reserve_room"),
]
