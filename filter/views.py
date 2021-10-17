from filter.dto import CategoryProductDto
from product.views import View
from django.shortcuts import render
from filter.services import ProductFilterService

class CategoryView(View):

    def get(self, request, *args, **kwargs):
        data = self._build_category_list_dto()
        context = ProductFilterService.get_product(request, data)
        return render(request, 'category-list.html',context)

    def _build_category_list_dto(self):
        return CategoryProductDto(
            category_pk = self.kwargs['pk']
        )
