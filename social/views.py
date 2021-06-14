from user.models import Profile
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from social.models import Like,Comment,ReComment
from product.models import Article
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

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


# class CommentView(View):

#   def post(self, request, **kwargs):
#     article = Article.objects.filter(pk=kwargs['pk']).first()
    
#     Comment.objects.create(
#       content = request.POST['comment'],
#       article = article,
#       writer = request.user,
#       owner = article.writer
#     )
    
#     return redirect('product:detail',kwargs['pk'])


class CommentView(View):
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
      # image = Comment.objects.filter(article__pk = article_pk).first().writer.profile.image
      # json.dumps(str(image)) 
      comment = Comment.objects.filter(article__pk = article_pk).create(
        article = article,
        writer = request.user,
        owner = owner,
        content = content
      )
      user_img = Profile.objects.filter(user__pk = user_pk).first().image.url
      context['user_img'] = user_img
      print(context)
      
      comment_user_img = Profile.objects.get(user__pk = user_pk)
      comment_user_img= comment_user_img.__dict__
      del comment_user_img['_state']

      # comment_user_img = comment_user_img
      print(comment_user_img)
      # del comment_user_img['_state']
      # del comment_user['_state']
      # comment_user = de/l comment_user['state']
      context['comment_user_img'] = comment_user_img
      comment_writer_pk = Comment.objects.filter(pk = comment.pk).first().writer.pk
      context['writer_pk'] = comment_writer_pk
      context['comment_obj'] = model_to_dict(comment)
      context['comment']= content
      context['user'] = user
      # context['image'] = json.dumps(str(image))
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
      context['article'] =article 
      context['re_content']=re_content
      context['user'] = user
      context['comment_data'] = model_to_dict(comment)
      
      recomment=ReComment.objects.filter(comment__pk=comment_pk).create(
      content = re_content,
      writer = request.user,
      )
      recomment.comment.add(comment)
      recomment_contents = {}
      for recomment in comment.re_comment.all():
        recomment_contents[recomment.id] = {'id':recomment.id,'created_at':recomment.created_at,'updated_at':recomment.updated_at, 'content':recomment.content,'writer_pk':recomment.writer.pk,'writer':recomment.writer.username,'user_img': recomment.writer.profile.image.url}
      
      context['user_img'] = recomment.writer.profile.image.url
      context['comment_user_img'] = comment.writer.profile.image.url
      context['recomment_obj'] = recomment_contents
      return JsonResponse(context)

    article_pk = Comment.objects.filter(pk=kwargs['pk']).first().article.pk
    comment = Comment.objects.filter(pk=kwargs['pk']).first()
    recomment = ReComment.objects.filter(comment__pk = kwargs['pk']).first()
    # recomment = ReComment.objects.filter(comment__pk=kwargs['pk']).create(
    #   content = request.POST['re_comment'],
    #   writer = request.user,
    # )
    # recomment.comment.add(comment)
    return redirect('product:detail',article_pk)


# class ReCommentView(View):
#   def get(self, request, **kwargs):
#     return render(request,'detail.html')
  
#   def post(self, request,**kwargs):
#     if request.is_ajax():
#       context = {}
#       data = json.loads(request.body)
#       # article_pk = data.get('article_pk')
#       user_pk = data.get('user_pk')
#       writer_pk = data.get('writer_pk')
#       article = Article.objects.filter(pk=writer_pk).first()
#       context['article'] =article
#       user = User.objects.filter(pk = user_pk).first().username
#       context['re_comment']=data.get('re_comment')
#       context['user'] = user
#       comment_data = json.loads(serialize('json',Comment.objects.filter(pk=data.get('comment_pk'))))
#       print(comment_data)
#       context['comment_data'] = comment_data
#       return JsonResponse(context)


def kakako_login(reqeust):
  pass