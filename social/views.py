from user.models import Profile
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from social.models import Like,Comment,ReComment
from product.models import Article
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

import json

# Create your views here.


class LikeView(View):

  def get(self, request, **kwargs):
    return render(request,'detail.html')
  
  def post(self, request,**kwargs):
    if request.is_ajax():
      context = {}
      data = json.loads(request.body)
      article_pk = data.get('article_pk')
      article = get_object_or_404(Article,pk=article_pk)
      like = Like.objects.filter(article__pk=article_pk).first()
      # if like is None:
      #   like = Like.objects.create(
      #     article = article
      #   )
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



class CommentView(LoginRequiredMixin,generic.View):
  login_url='/user/signin'
  direct_field_name = None
  def get(self, request, **kwargs):
    return render(request,'detail.html')
  
  def post(self, request,**kwargs):
    if request.is_ajax():
      context = {}
      data = json.loads(request.body)
      article_pk = data.get('article_pk')
      content = data.get('content')
      article = Article.objects.filter(pk=article_pk).first()
      user_pk = data.get('user_pk')
      owner_pk = data.get('owner_pk')
      owner = User.objects.filter(pk = owner_pk).first()
      user = User.objects.filter(pk = user_pk).first().username
      comment = Comment.objects.filter(article__pk = article_pk).create(
        article = article,
        writer = request.user,
        owner = owner,
        content = content,

      )

      profile_nickname = Profile.objects.filter(user__pk=user_pk).first().nickname
      context['profile_nickname'] = profile_nickname
      user_img = Profile.objects.filter(user__pk = user_pk).first().image.url
      context['user_img'] = user_img
      
      comment_user_img = Profile.objects.get(user__pk = user_pk)
      comment_user_img= comment_user_img.__dict__
      del comment_user_img['_state']

      context['comment_user_img'] = comment_user_img
      comment_writer_pk = Comment.objects.filter(pk = comment.pk).first().writer.pk
      context['writer_pk'] = comment_writer_pk
      context['comment_obj'] = model_to_dict(comment)
      context['comment']= content
      context['user'] = user
      context['new_comment'] = True
      return JsonResponse(context)


class ReCommentView(View):
  def post(self, request, **kwargs):
    if request.is_ajax():
      context = {}
      data = json.loads(request.body)
      user_pk = data.get('user_pk')
      comment_pk = data.get('comment_pk')
      re_content = data.get('re_comment')
      article = Article.objects.filter(pk=comment_pk).first()
      comment = Comment.objects.filter(pk = comment_pk).first()
      user = User.objects.filter(pk = user_pk).first().username
      recomment = ReComment.objects.filter(comment__pk=comment_pk).first()
      context['article'] = article 
      context['re_content']=re_content
      context['user'] = user
      context['comment_data'] = model_to_dict(comment)
      profile_nickname = Profile.objects.filter(user__pk=user_pk).first().nickname
      
      recomment=ReComment.objects.filter(comment__pk=comment_pk).create(
      content = re_content,
      writer = request.user,
      )
      recomment.comment.add(comment)
      recomment_contents = {}
      for recomment in comment.re_comment.all():
        recomment_contents[recomment.id] = {'id':recomment.id,'created_at':recomment.created_at,'updated_at':recomment.updated_at, 'content':recomment.content,'writer_pk':recomment.writer.pk,'writer':recomment.writer.username,'user_img': recomment.writer.profile.image.url,'profile_nickname':profile_nickname}
      
      context['comment_user_img'] = comment.writer.profile.image.url
      context['recomment_obj'] = recomment_contents
      return JsonResponse(context)


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