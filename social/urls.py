from django.urls import path
from social.views import LikeView,CommentView, ReCommentView

app_name = 'social'
urlpatterns = [

    path('like',LikeView.as_view(), name='like'),
    path('comment/',CommentView.as_view(), name='comment'),
    path('re_comment/',ReCommentView.as_view(), name='re_comment'),
    
    #  path('user/', include('user.urls')),
]
    
