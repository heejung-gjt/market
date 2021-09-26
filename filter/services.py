from user.models import User
from product.models import Article
from django.shortcuts import get_object_or_404
from filter.models import Category,CategoryDetail
from django.db.models import Count
from product.dto import ProductFilterDto, ProductSubFilterDto
from django.db.models import Q
from utils import context_infor, paginator

class ProductFilterService():

    @staticmethod
    def find_by_product_list(category_pk):
        articles = get_object_or_404(Category, pk = category_pk).article
        articles = Category.objects.get(pk=category_pk).article.all()
        return articles

    @staticmethod
    def find_by_category_title(category_pk):
        category_title = get_object_or_404(Category, pk=category_pk)
        return category_title

    @staticmethod
    def find_by_all_category():
        category_list = Category.objects.all()
        return category_list

    @staticmethod
    def find_by_latest_article():
        article_list = Article.objects.filter(is_deleted = False).order_by('-created_at')
        return article_list

    @staticmethod
    def get_order_by_comment_count():
        article = Article.objects.filter(is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
        return article

    @staticmethod
    def get_order_by_like_count():
        article = Article.objects.filter(is_deleted=False).annotate(like_count=Count('like')).order_by('-like_count','-created_at')
        return article

    @staticmethod
    def get_order_by_user_article(request):
        user = request.user
        article = Article.objects.filter(writer__pk = user.pk, is_deleted=False).order_by('-created_at')
        return article

    @staticmethod
    def find_by_all_article():
        article_list = Article.objects.all()
        return article_list

    @staticmethod
    def find_by_not_deleted_article():
        article_list = Article.objects.filter(is_deleted = False).order_by('-created_at')
        return article_list

    @staticmethod
    def find_not_deleted_user_article_list(**kwargs):
        articles = Article.objects.filter(is_deleted=kwargs['is_deleted'], writer=kwargs['writer'])
        return articles

    @staticmethod
    def find_by_filter_article(user):
        articles = Article.objects.filter(writer__pk = user.pk)
        return articles

    @staticmethod
    def find_by_category_detail(pk):
        category_detail = CategoryDetail.objects.filter(category__pk = pk)
        return category_detail

    @staticmethod
    def find_by_category_pk_in_category_detail(category_detail_pk):
        category_pk = CategoryDetail.objects.filter(pk = category_detail_pk).first().category.pk
        return category_pk

    @staticmethod
    def find_article_infor(pk):
        article = get_object_or_404(Article, pk = pk)
        return article

    @staticmethod
    def get_filter_product_infor(request, dto:ProductFilterDto):
        print(dto)
        categorys = ProductFilterService.find_by_all_category()
        price_from = int(dto.price_from)
        price_to = int(dto.price_to)
        articles = None
        q = Q()
        if dto.category_pk:
            q &= Q(category = dto.category_pk)
            q &= Q(price__range =(price_from, price_to))
        if dto.product_sort:
            if dto.product_sort == '1':
                articles = Article.objects.filter(q).order_by('-created_at')
            elif dto.product_sort == '2':
                articles = Article.objects.filter(q).order_by('created_at')
            elif dto.product_sort == '3':
                articles = Article.objects.filter(q).order_by('price')
            elif dto.product_sort == '4':
                articles = Article.objects.filter(q).order_by('-price')
            elif dto.product_sort == '5':
                articles = Article.objects.filter(q, is_deleted=False).annotate(like_count=Count('like__users')).order_by('-like_count','-created_at')
            elif dto.product_sort == '6':
                articles = Article.objects.filter(q, is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
        else:
            articles = Article.objects.filter(q).order_by('-created_at')
        page = request.GET.get('page', '1')
        articles, page_range = paginator(articles, page, 9)
        context = context_infor(
            sort = dto.product_sort, 
            pk = dto.category_pk, 
            start = price_from, 
            end = price_to, 
            article_list = articles, 
            category_list = categorys, 
            is_page = False, 
            page_range = page_range
        )
        return context

    @staticmethod
    def get_filter_sub_product_infor(request, dto:ProductSubFilterDto):
        category_title = Category.objects.get(pk=dto.category)
        categorys = ProductFilterService.find_by_all_category()
        price_from = int(dto.price_from)
        price_to = int(dto.price_to)
        articles = None
        q = Q()
        q &= Q(category = dto.category)
        if dto.category_detail:
            q &= Q(category_detail = dto.category_detail)
        q &= Q(price__range =(price_from, price_to))

        if dto.product_sort:
            if dto.product_sort == '1':
                articles = Article.objects.filter(q).order_by('price')
            elif dto.product_sort == '2':
                articles = Article.objects.filter(q).order_by('-price')
            elif dto.product_sort == '3':
                articles = Article.objects.filter(q, is_deleted=False).annotate(like_count=Count('like__users')).order_by('-like_count','-created_at')
            elif dto.product_sort == '4':
                articles = Article.objects.filter(q, is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
        else:
            articles = Article.objects.filter(q).all()
        category_sub_list = CategoryDetail.objects.filter(category__pk = dto.category)
        category_name = Category.objects.filter(pk = dto.category).first().name
        page = request.GET.get('page', '1')
        articles, page_range = paginator(articles, page, 9)
        context = context_infor(
            category_list = categorys,
            category_sub_list = category_sub_list,
            articles = articles,
            page_range = page_range,
            sort = dto.product_sort,
            pk = dto.category,
            sub_pk = dto.category_detail,
            start = price_from,
            end = price_to,
            category_title = category_title,
            category_name = category_name
        )
        return context


    @staticmethod
    def find_by_user(pk):
        user = User.objects.filter(pk=pk).first()
        return user


class CategoryFilterService():

    @staticmethod
    def find_by_category_detail(pk):
        category =  CategoryDetail.objects.filter(pk= pk).first() 
        return category

    @staticmethod
    def find_by_filter_category(pk):
        category = get_object_or_404(Category, pk = pk)
        return category