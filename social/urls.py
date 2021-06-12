from django.urls import path
from social.views import LikeView

app_name = 'social'
urlpatterns = [

    path('like',LikeView.as_view(), name='like'),
    #  path('user/', include('user.urls')),
]
    
