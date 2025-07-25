from django.urls import path,include
from . import views
app_name='users'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot/', views.forgot_view, name='forgot'),
    path('restore/<str:email>/', views.restore_view, name='restore'),
    path('', views.home_view, name='home')
]