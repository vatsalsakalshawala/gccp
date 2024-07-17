from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('myapp/home/', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/rate/', views.add_rating, name='add_rating'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('photo/upload/', views.upload_photo, name='upload_photo'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
