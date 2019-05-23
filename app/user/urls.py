from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import SignupView, LoginView, LogoutView, UserView


app_name = 'user'

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', login_required(UserView.as_view()), name='user'),
]
