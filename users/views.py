from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.views.generic.detail import DetailView
from rest_framework import permissions, status, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from .forms import UserCreationForm, UserUpdateForm
from .models import BasketItem, BasketModel, CustomUserModel, EmailVerification
from .serializers import BasketSerializer, BasketUpdateSerializer


class ProfileView(DetailView):
    model = CustomUserModel
    template_name = 'profile.html'

    def get_object(self):
        return CustomUserModel.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUserModel.objects.get(username=self.request.user.username)
        return context


class ChangePasswordView(PasswordChangeView):
    template_name = 'password-change.html'

    def get_success_url(self):
        return reverse('users:logout')

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        return get_object_or_404(CustomUserModel, pk=user_id)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', None)
        if redirect_to:
            return redirect_to
        else:
            return reverse('products:main')


class CustomRegistrationView(CreateView, SuccessMessageMixin):
    model = CustomUserModel
    template_name = 'register.html'
    success_message = 'Your registration was successful!'
    form_class = UserCreationForm
    success_url = '/users/login'


class UpdateProfileView(UpdateView):
    template_name = 'profile-edit.html'
    form_class = UserUpdateForm
    model = CustomUserModel

    def get_success_url(self):
        return reverse('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUserModel.objects.get(username=self.request.user.username)
        return context

    def get_object(self):
        return CustomUserModel.objects.get(username=self.request.user.username)


class BasketView(DetailView):
    model = BasketModel
    template_name = 'basket.html'

    def get_object(self):
        try:
            basket = BasketModel.objects.get(
                user=self.request.user, is_payed=False, is_delivered=False, is_collected=False
            )
        except BasketModel.DoesNotExist:
            basket = BasketModel(user=self.request.user)
            basket.save()

        return basket

    def get_context_data(self, **kwargs):
        user = CustomUserModel.objects.get(username=self.request.user.username)

        basket_items = BasketItem.objects.filter(
            user=user, basket__is_payed=False, basket__is_delivered=False, basket__is_collected=False)
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['items'] = basket_items

        return context


def basket_remove(request, basket_id):
    try:
        basket = BasketModel.objects.get(id=basket_id, user=request.user, is_collected=False)
        basket.delete()
    except BasketModel.DoesNotExist:
        pass

    return redirect('users:basket')


def basket_pay(request):
    try:
        basket = BasketModel.objects.get(
            user=request.user, is_collected=False, is_payed=False, is_completed=False, is_delivered=False
        )
        basket.is_payed = True
        basket.is_collected = True
        basket.save()
    except BasketModel.DoesNotExist:
        pass

    return redirect('users:basket')


class AllBasketsView(ListView):
    template_name = 'orders.html'
    model = BasketModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        baskets = BasketModel.objects.filter(user=self.request.user, is_payed=True)

        total_per_basket = {}
        for basket in baskets:
            total_per_basket[basket.id] = sum(item.quantity * item.product.price for item in basket.items.all())

        context['baskets'] = baskets
        context['user'] = self.request.user

        return context


class EmailVerificationView(TemplateView):
    template_name = 'verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = CustomUserModel.objects.get(email=kwargs['email'])
        verifications = EmailVerification.objects.filter(user=user, code=code)
        if verifications.exists() and not verifications.first().is_expired():
            user.email_verification = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('products:main'))


# REST API VIEWS
class BasketViewSet(viewsets.ModelViewSet):
    queryset = BasketModel.objects.filter(
        is_collected=True, is_payed=True, is_completed=False, is_delivered=False
    ).order_by('-id')
    serializer_class = BasketSerializer
    permissions_classes = [permissions.IsAdminUser]


class UpdateBasket(UpdateAPIView):
    def get_queryset(self):
        order_pk = self.kwargs['pk']
        print(order_pk)
        queryset = BasketModel.objects.get(id=order_pk)
        return queryset

    serializer_class = BasketUpdateSerializer
    permission_classes = [permissions.BasePermission]

    def post(self, request, **kwargs):
        order_pk = self.kwargs['pk']
        basket = BasketModel.objects.get(id=order_pk)
        basket.is_completed = True
        basket.save()

        serializer = BasketUpdateSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)
