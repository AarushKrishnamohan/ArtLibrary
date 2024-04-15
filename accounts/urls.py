from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_user, name = 'login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),



    #password reset views
    path('reset-password/reset-password', views.reset_password, name='reset-password'),
    path('reset-password/new-password', views.reset_change_password, name='reset-change-password'),
    path('reset-password/confirmation/', views.reset_password_confirmation, name='reset-password-confirmation'),
    path('change-password/', views.change_password, name='change-password')


]