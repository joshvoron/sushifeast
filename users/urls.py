from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (AllBasketsView, BasketView, ChangePasswordView,
                    CustomLoginView, CustomRegistrationView,
                    EmailVerificationView, ProfileView, UpdateProfileView,
                    basket_pay, basket_remove)

app_name = 'users'

urlpatterns = [
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('changepassword/', login_required(ChangePasswordView.as_view()), name='changepassword'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('registration/', CustomRegistrationView.as_view(), name='registration'),
    path('profile-edit/', login_required(UpdateProfileView.as_view()), name='profile-edit'),
    path('card/', login_required(BasketView.as_view()), name='basket'),
    path('basket/remove/<int:basket_id>/', login_required(basket_remove), name='basket_remove'),
    path('all-baskets/', login_required(AllBasketsView.as_view()), name='all-baskets'),
    path('pay/', login_required(basket_pay), name='basket-pay'),
    path('verification/<str:email>/<uuid:code>/', login_required(EmailVerificationView.as_view()), name='verification'),
]
