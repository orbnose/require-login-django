from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from . import views

app_name = 'requirelogin'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/',
        auth_views.PasswordChangeView.as_view( success_url=reverse_lazy('requirelogin:password_change_done') ),
        name="change_password"),
    path('change_password/done/',
        auth_views.PasswordChangeDoneView.as_view( extra_context = {'return_url': settings.LOGIN_REDIRECT_URL} ), 
        name="password_change_done"),
]