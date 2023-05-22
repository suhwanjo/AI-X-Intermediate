
# 현재 폴더의 views를 사용한다.
from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('post_update/<int:pk>', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/add_comment', views.add_comment),
    path('tag/<str:slug>/', views.tag_page),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
]