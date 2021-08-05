from social.services import SocialService
from user.models import User
from django.shortcuts import render
from django.http.response import JsonResponse
from social.models import Like,Comment,ReComment
from product.models import Article
from django.views.generic import View
from .dto import CommentDto,ReCommentDto
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import get_time_passed

import json
import time
# Create your views here.


class LikeView(View):

  def get(self, request, **kwargs):
    return render(request,'detail.html')
  
  def post(self, request,**kwargs):
    if request.is_ajax():
      context = {}
      data = json.loads(request.body)
      print('헤헤헤헤소셜스')
      article_pk = data.get('article_pk')
      like = Like.objects.filter(article__pk=article_pk).first()

      # Like.objects.create(
      #   article = Article.objects.filter(pk=article_pk).first()
      # )
        
      if request.user in like.users.all(): 
        Like.objects.filter(article__pk = article_pk).update(
          is_liked = False
        )
        like.users.remove(request.user)
        context['is_liked'] = False  
      else:
        like.users.add(request.user)
        Like.objects.filter(article__pk = article_pk).update(
          is_liked = True
        )
        context['is_liked'] = True  
      context['article_pk'] = article_pk
      return JsonResponse(context)


# post에서 ajax일때 데이터를 받아 dto형식으로 데이터를 넣어 service에 보내준다
# 서비스에서는 해당 데이터를 가지고 comment를 create해주고 알맞은 데이터를 context에 넣어준다
#이때 service에서 filter되는 것들은 filter,user라는 services에서 import해서 사용하자

# view의 역할은 데이터를 받아 dto형식으로 데이터를 넣어주고 해당 데이터를 가지고 create해줄 Service에 
# 전달하고, 결과값을 받아 해당 template에 뿌려주는 역할을 담당한다

class CommentView(LoginRequiredMixin,generic.View):
  
  login_url='/user/signin'
  direct_field_name = None

  def get(self, request, **kwargs):
    return render(request,'detail.html')
  
  def post(self, request,**kwargs):
    if request.is_ajax():
      data = json.loads(request.body)
      print(request.body)
      print(type(data.get('article_pk')))
      comment_dto = self._build_comment_dto(data)
      context = SocialService.create_comment(comment_dto)
      return JsonResponse(context)
  
  @staticmethod
  def _build_comment_dto(data):
    return CommentDto(
      article_pk = data.get('article_pk'),
      content = data.get('content'),
      writer_pk = data.get('user_pk'),
      owner_pk = data.get('owner_pk')
    )
    

class ReCommentView(View):
  def post(self, request):
    if request.is_ajax():
      data = json.loads(request.body)
      recomment_dto = self._build_recomment_dto(request,data)      
      context = SocialService.create_recomment(recomment_dto)
    return JsonResponse(context)

  @staticmethod
  def _build_recomment_dto(request,data):
    return ReCommentDto(
      content = data.get('re_comment'),
      writer = request.user,
      created_at = time.time(),
      user_pk = data.get('user_pk'),
      comment_pk = data.get('comment_pk'),
      article_pk = data.get('article_pk')
      )


class EditView(View):
   def post(self, request, **kwargs):

    if request.is_ajax():
      data = json.loads(request.body)
      comment_pk = data.get('comment_pk')
      content = data.get('edit_comment')
      Comment.objects.filter(pk=comment_pk).update(
        content = content
      )
      return JsonResponse({'C':'C'})


class DeleteView(View):
   def post(self, request, **kwargs):

    if request.is_ajax():
      data = json.loads(request.body)
      if data.get('msg') == 'recomment_delete':
        recomment_pk = data.get('recomment_pk')
        ReComment.objects.filter(pk=recomment_pk).delete()
        return JsonResponse({'r':'r'})
      comment_pk = data.get('comment_pk')
      Comment.objects.filter(pk=comment_pk).delete()
      return JsonResponse({'C':'C'})



def kakako_login(reqeust):
  pass