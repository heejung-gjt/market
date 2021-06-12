from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from social.models import Like
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

def kakako_login(reqeust):
  pass