from django.urls import path, include

from . import views

# Intended only for use in tests.py


urlpatterns = [
    path('', views.index, name='index'),
    path('nested/nested_redir/', views.nested_redir, name='nested_redir'),
    path('nested/nested_forbidden/', views.nested_forbidden, name='nested_forbidden'),
    path('accounts/', include('requirelogin.urls'))
]