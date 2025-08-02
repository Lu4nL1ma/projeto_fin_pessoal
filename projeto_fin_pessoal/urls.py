from django.contrib import admin
from django.urls import path
from app_fin_pessoal import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('form_receita/', views.form_receita, name='form_rec'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('delete/', views.delete_receitas, name='delete_receitas'),
    path('admin/', admin.site.urls),
]
