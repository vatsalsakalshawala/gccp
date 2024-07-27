import os
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name="login_view"),
    #path('post/', post, name="post"),
    path('register/', register_view, name="register_view"),
    path('add-blog/', add_blog, name="add_blog"),
    path('blog-detail/<slug>', blog_detail, name="blog_detail"),
    path('see-blog/', see_blog, name="see_blog"),
    path('blog-delete/<id>', blog_delete, name="blog_delete"),
    path('blog-update/<slug>/', blog_update, name="blog_update"),
    path('logout-view/', logout_view, name="logout_view"),
    path('verify/<token>/', verify, name="verify"),
    path('header/', header, name="header"),
    # path('base1/', base1, name="base1"),

    # path('profile/', profile_view, name='profile'),
    path('search/', search_view, name='search'),
    path('contact/', contact_view, name='contact_view'),
    path('contact_success/', contact_success, name='contact_success'),   
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name='reset_password'),
    path('reset_password_Sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name='password_reset_confirm'),
    path('reset_password_compelete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name='password_reset_complete'),

    path('profile/', profile_view, name='profile_view'),

]
