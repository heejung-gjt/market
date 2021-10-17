from django.http import request
from .dto import ProductDto, EditDto, ProductCategoryDto, ProductPkDto, ProductSearchDto
from .models import Article,Price
from social.models import Like, Comment
from user.models import User
from filter.services import CategoryFilterService, ProductFilterService
from .models import Photo
from utils import calculate_price, context_infor, paginator
from django.utils.datastructures import MultiValueDictKeyError
from market.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME,AWS_S3_REGION_NAME
from boto3.session import Session
from user.utils import context
from django.db.models import Q
from datetime import datetime

import time


# product crud 
class ProductService():

    @staticmethod
    def create(dto:ProductDto):
        try:
            category_detail_pk = dto.category_detail_pk
        except MultiValueDictKeyError:
            categorys = ProductFilterService.find_by_all_category()
            result = context_infor(state = True, msg = '카테고리를 선택해주세요 !', category_list = categorys)
            return result

        category_pk = ProductFilterService.find_by_category_pk_in_category_detail(category_detail_pk)
        category_detail_name = CategoryFilterService.find_by_category_detail(dto.category_detail_pk)
        category_pk = CategoryFilterService.find_by_category_detail(dto.category_pk).category.pk
        category = CategoryFilterService.find_by_filter_category(category_pk)
        discount_rate = calculate_price(dto.origin_price, dto.price)

        if not dto.content or not dto.image or not dto.price or not dto.origin_price or not dto.name:
            result = context_infor(state = True, msg = '모든 내용을 작성해주세요 !')
            return result
            
        if discount_rate == -1:
            result = context_infor(state = True, msg = '정상적인 금액을 입력해주세요 !')
            return result
        
        article = Article.objects.create(
            name = dto.name,
            category = category,
            content = dto.content,
            origin_price = dto.origin_price,
            price = dto.price,
            writer = dto.writer,
            address = dto.writer.address,
            created_at = time.time()
        )
        article.category_detail.add(category_detail_name)

        Price.objects.create(
            article = article,
            discount_rate = discount_rate 
        )

        Like.objects.create(
            article = article
            )

        # 여러개의 이미지 s3에 넣기
        session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
        )
        s3 = session.resource('s3')
        s3_url = "https://django-s3-practices.s3.ap-northeast-2.amazonaws.com/"

        for file in dto.image:
            now = datetime.now().strftime('%Y%H%M%S')
            s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
            Key = now+file.name,
            Body = file
            )
            Photo.objects.create(
            article = article,
            image = s3_url+now+file.name
            )  

        result = context_infor(state = False, msg = 'completed', category_pk = category_pk)
        return result

    @staticmethod
    def edit(dto:EditDto):
        category = CategoryFilterService.find_by_filter_category(dto.category_pk)
        article = ProductFilterService.find_article_infor(dto.article_pk)
        discount_rate = calculate_price(dto.origin_price, dto.price)

        Article.objects.filter(pk=dto.article_pk).update(
            category = category,
            name = dto.name,
            content = dto.content,
            origin_price = dto.origin_price,
            price = dto.price,
            writer = dto.writer,   
        )
        discount_rate = calculate_price(dto.origin_price, dto.price)
        if discount_rate == -1:
            return discount_rate

        Price.objects.filter(article__pk = dto.article_pk).update(
            article = article,
            discount_rate = discount_rate 
        )
         # 여러개의 이미지 s3에 넣기
        session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
        )
        s3 = session.resource('s3')
        s3_url = "https://django-s3-practices.s3.ap-northeast-2.amazonaws.com/"

        if dto.image:
            Photo.objects.filter(article__pk = dto.article_pk).delete() 
            for file in dto.image:
                now = datetime.now().strftime('%Y%H%M%S')
                s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
                Key = now+file.name,
                Body = file
                )
                Photo.objects.filter(article__pk = dto.article_pk).create(
                    article = article,
                    image = s3_url+now+file.name
                ) 

        return False

    @staticmethod
    def delete(dto:ProductPkDto):
        Article.objects.filter(pk = dto.article_pk).update(
            is_deleted = True
        )
        result = context_infor(state = 'success')
        return result
    
    @staticmethod
    def get_product_infor(request, articles):
        article_list = ProductFilterService.find_by_not_deleted_article()
        page = request.GET.get('page', '1')
        articles, page_range = paginator(article_list, page, 9)
        context = context_infor(
            articles = articles,
            product_title = '모든',
            page_range = page_range,
            category_list =  ProductFilterService.find_by_all_category(),
            is_page = True
            )
        return context

    @staticmethod
    def get_detail_infor(request, dto:ProductPkDto):
        article = ProductFilterService.find_article_infor(dto.article_pk)
        like = Like.objects.filter(article__pk = dto.article_pk).first()
        category_list = ProductFilterService.find_by_all_category()
        comment_list = [
        {
            'writer':comment.writer,
            'pk':comment.pk,
            'username':User.objects.get(pk=comment.writer.pk).nickname,
            'content':comment.content,
            'image_url':comment.writer.image,
            'writer_nickname':comment.writer.nickname,
            're_comment':comment.re_comment.all(),
            'comment_obj':comment
        } for comment in Comment.objects.filter(article__pk = dto.article_pk)
        ]
        context = context_infor(
            article = article, 
            category_list = category_list, 
            comment_list = comment_list
            )
        if like is not None:
            if request.user in like.users.all(): 
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        return context

    @staticmethod
    def get_category_detail(dto:ProductCategoryDto):
        categorys = ProductFilterService.find_by_all_category()
        category_detail = ProductFilterService.find_by_category_detail(dto.category_detail_pk)
        category = ProductFilterService.find_by_category_title(dto.category_detail_pk)
        context = context_infor(
            category_list = categorys, 
            category = category, 
            state = True, 
            category_detail = category_detail
            )
        return context

    @staticmethod
    def get_search_product_infor(request, dto:ProductSearchDto):
        categorys = ProductFilterService.find_by_all_category()
        articles = Article.objects.filter(Q(name__icontains=dto.search_keyword) | Q(content__icontains=dto.search_keyword) | Q(category__name__icontains=dto.search_keyword), is_deleted = False).distinct().order_by('-created_at')
        article_sum = articles.count()
        page = request.GET.get('page', '1')
        articles, page_range = paginator(articles, page, 12)

        context = context_infor(
            article_sum = article_sum,
            articles = articles,
            category_list = categorys,
            keyword = dto.search_keyword,
            page_range = page_range
        )
        return context