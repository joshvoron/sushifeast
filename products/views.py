from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from users.models import BasketItem, BasketModel

from .models import CategoryModel, ProductModel


class GeneralView(ListView):
    template_name = 'general.html'
    context_object_name = 'dish'

    def get_queryset(self):
        return ProductModel.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        try:
            basket = BasketModel.objects.get(user=self.request.user, is_payed=False)
            counter = basket.total_quantity()
        except BasketModel.DoesNotExist:
            counter = ''

        context = super().get_context_data(**kwargs)
        context['alldishes'] = ProductModel.objects.filter(is_available=True)
        context['hitdishes'] = ProductModel.objects.filter(hit=True)
        context['newdishes'] = ProductModel.objects.filter(new=True)
        context['category'] = CategoryModel.objects.all()
        context['user'] = self.request.user
        context['counter'] = counter
        return context


class CategoryView(ListView):
    template_name = 'category.html'
    context_object_name = 'dish'

    def get_queryset(self):
        category_id = self.kwargs['pk']
        queryset = ProductModel.objects.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        try:
            basket = BasketModel.objects.get(user=self.request.user, is_payed=False)
            counter = basket.total_quantity()
        except BasketModel.DoesNotExist:
            counter = ''

        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['alldishes'] = ProductModel.objects.filter(category_id=self.kwargs['pk'])
        context['category'] = CategoryModel.objects.get(id=category_id)
        context['user'] = self.request.user
        context['counter'] = counter
        return context


@require_POST
def add_to_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        product = ProductModel.objects.get(id=product_id)
        user = request.user

        try:
            basket = BasketModel.objects.get(
                user=user, is_payed=False, is_delivered=False, is_collected=False, is_completed=False)
        except BasketModel.DoesNotExist:
            basket = BasketModel(user=user)
            basket.save()

        basket_item = BasketItem(product=product, quantity=quantity, user=user, basket=basket)
        basket_item.save()

        return JsonResponse({'success': True})
