
from django.shortcuts import render
from social.services import SocialService
from django.http.response import JsonResponse
from django.views.generic import View
from .dto import CommentDeleteDto, CommentDto, CommentEditDto,ReCommentDto, CommentDeleteDto, SocialLikeDto
from django.contrib.auth.mixins import LoginRequiredMixin

import json
import time


class LikeView(View):

    def get(self, request, *args, **kwargs):
        return render(request,'detail.html')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_social_like_dto(request)
            context = SocialService.clicked_like(request, data)
            return JsonResponse(context)
  
    def _build_social_like_dto(self, request):
        data = json.loads(request.body)
        return SocialLikeDto(
            article_pk = data.get('article_pk')
        )


class CommentView(LoginRequiredMixin, View):
    login_url='/user/signin'
    direct_field_name = None

    def get(self, request, **kwargs):
        return render(request,'detail.html')

    def post(self, request,**kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
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

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_recomment_dto(request)      
            context = SocialService.create_recomment(data)
        return JsonResponse(context)

    @staticmethod
    def _build_recomment_dto(self, request):
        data = json.loads(request.body)
        return ReCommentDto(
            content = data.get('re_comment'),
            writer = request.user,
            created_at = time.time(),
            user_pk = data.get('user_pk'),
            comment_pk = data.get('comment_pk'),
            article_pk = data.get('article_pk')
            )


class EditView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_comment_edit_dto(request)
            context = SocialService.edit(data)
        return JsonResponse(context)

    @staticmethod
    def _build_comment_edit_dto(request):
        data = json.loads(request.body)
        return CommentEditDto(
            comment_pk = data.get('comment_pk'),
            comment = data.get('edit_comment')
        )


class DeleteView(View):

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = self._build_comment_delete_dto(request)
            context = SocialService.delete(data)
            if context['state'] == 'recomment':
                return JsonResponse(context)
            else:
                return JsonResponse(context)
    
    @staticmethod
    def _build_comment_delete_dto(request):
        data = json.loads(request.body)
        return CommentDeleteDto(
            recomment_pk = data.get('recomment_pk'),
            comment_pk = data.get('comment_pk'),
            message = data.get('msg')

        )
