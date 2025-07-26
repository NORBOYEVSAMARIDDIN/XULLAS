from django.urls import path,include
from . import views
app_name='users'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot/', views.forgot_view, name='forgot'),
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('settings/', views.settings_view, name='settings'),
    path('restore/<str:email>/', views.restore_view, name='restore'),
    path('account/', views.account_view, name='account'),

    path('change-email/', views.change_email, name='change_email'),
    path('verify-change-email/<str:email>', views.verify_change_email, name='verify_change_email'),


    path('change-password/', views.change_password, name='change_password'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('read-profile/', views.read_profile, name='read_profile'),

    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('delete-photo/', views.delete_photo, name='delete_photo'),

    path('country/', views.country, name='country'),
    path('read-country/', views.read_country, name='read_country'),


    path('login/google/', views.google_loging, name='google_login'),
    path('google/login/callback/', views.google_callback, name='google_callback'),
]