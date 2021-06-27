from django.shortcuts import get_object_or_404
from social.dto import CommentDto, ReCommentDto
from social.models import Like, ReComment
from social.models import Comment
from user.models import Profile
from utils import context_infor,get_time_passed
from django.forms.models import model_to_dict
from filter.services import ProductFilterService
from user.services import UserFilterService
from product.models import Article
from django.contrib.auth.models import User

import time

class SocialService():

  @staticmethod
  def find_clicked_like_article_list(user):
    articles = Like.objects.filter(users__pk = user.pk).all()
    return articles

  @staticmethod
  def create_comment(dto:CommentDto):
    article = ProductFilterService.find_article_infor(dto.article_pk)
    owner = UserFilterService.find_user_infor(dto.owner_pk)
    user = UserFilterService.find_user_infor(dto.writer_pk).username
    writer = UserFilterService.find_user_infor(dto.writer_pk)

    comment = Comment.objects.filter(article__pk = dto.article_pk).create(
            article = article,
            writer = writer,
            owner = owner,
            content = dto.content,
            created_at = time.time()
          )
    profile_nickname = UserFilterService.find_profile_infor(dto.writer_pk).nickname
    comment_user_img = UserFilterService.get_profile_infor(dto.writer_pk)
    comment_writer_pk = SocialFilterService.find_by_comment_infor(comment.pk).writer.pk
    user_img = UserFilterService.find_profile_infor(dto.writer_pk).image.url
    
    # img dict로 변환하는 방법
    comment_user_img= comment_user_img.__dict__
    del comment_user_img['_state']

    # context_infor로 context 생성
    context = context_infor(
      comment_created = get_time_passed(comment),
      profile_nickname = profile_nickname,
      comment_user_img=comment_user_img,
      writer_pk=comment_writer_pk,
      comment_obj =model_to_dict(comment),
      comment = dto.content, 
      user=user, 
      new_comment = True,
      user_img = user_img
      )
    return context 

  @staticmethod
  def create_recomment(dto:ReCommentDto):
    comment = SocialFilterService.find_by_comment_infor(dto.comment_pk)
    user = UserFilterService.find_user_infor(dto.user_pk).username
    profile_nickname = UserFilterService.find_profile_infor(dto.user_pk).nickname
    recomment = ReComment.objects.create(
    content = dto.content,
    writer = dto.writer,
    created_at = dto.created_at
    )
    recomment.comment.add(comment)

    recomment_contents = {}
    for recomment in comment.re_comment.all():
      recomment_contents[recomment.id] = {
        'id':recomment.id,
        'created_at':get_time_passed(recomment),
        'updated_at':recomment.updated_at, 
        'content':recomment.content,
        'writer_pk':recomment.writer.pk,
        'writer':recomment.writer.username,
        'user_img': recomment.writer.profile.image.url,
        'profile_nickname':profile_nickname
        }
    
    context = context_infor(
      re_content = dto.content,
      user = user,
      comment_data = model_to_dict(comment),
      recomment_created = get_time_passed(recomment),
      comment_user_img = comment.writer.profile.image.url,
      recomment_obj = recomment_contents, 
      )
    return context


class SocialFilterService():

  @staticmethod
  def find_by_comment_infor(pk):
    result = get_object_or_404(Comment, pk = pk)
    return result

  @staticmethod
  def find_by_recomment_infor(pk):
    result = get_object_or_404(ReComment, comment__pk = pk)
    return result