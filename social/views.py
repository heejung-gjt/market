from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from social.models import Like,Comment,ReComment
from product.models import Article
from django.views.generic import View
from django.shortcuts import get_object_or_404
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


class CommentView(View):

  def post(self, request, **kwargs):
    article = Article.objects.filter(pk=kwargs['pk']).first()
    
    Comment.objects.create(
      content = request.POST['comment'],
      article = article,
      writer = request.user,
      owner = article.writer
    )
    
    return redirect('product:detail',kwargs['pk'])


# class CommentView(View):
#   def get(self, request, **kwargs):
#     return render(request,'detail.html')
  
#   def post(self, request,**kwargs):
#     if request.is_ajax():
#       context = {}
#       data = json.loads(request.body)
#       article_pk = data.get('article_pk')
#       article = Article.objects.filter(pk=article_pk).first()
#       user_pk = data.get('user_pk')
#       owner_pk = data.get('owner_pk')
#       content = data.get('comment')
#       owner = User.objects.filter(pk = owner_pk).first()
#       user = User.objects.filter(pk = user_pk).first().username
#       comment = Comment.objects.filter(article__pk = article_pk).create(
#         article = article,
#         writer = request.user,
#         owner = owner,
#         content = content
#       )
#       context['comment_pk'] = comment.pk
#       context['comment']=data.get('comment')
#       context['user'] = user
#       return JsonResponse(context)


class ReCommentView(View):
  def post(self, request, **kwargs):
    article_pk = Comment.objects.filter(pk=kwargs['pk']).first().article.pk
    comment = Comment.objects.filter(pk=kwargs['pk']).first()
    recomment = ReComment.objects.filter(comment__pk = kwargs['pk']).first()
    recomment = ReComment.objects.filter(comment__pk=kwargs['pk']).create(
      content = request.POST['re_comment'],
      writer = request.user,
    )
    recomment.comment.add(comment)
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