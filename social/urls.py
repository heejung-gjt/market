from django.urls import path
from social.views import LikeView,CommentView, ReCommentView,DeleteView,EditView

app_name = 'social'
urlpatterns = [

    path('like',LikeView.as_view(), name='like'),
    path('comment/',CommentView.as_view(), name='comment'),
    path('re_comment/',ReCommentView.as_view(), name='re_comment'),
    path('edit/',EditView.as_view(),name='edit'),
    path('delete/',DeleteView.as_view(),name='delete'),
    
]
    
