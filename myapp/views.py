from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Rating, Photo, Recipe
from .forms import PostForm, CommentForm, RatingForm, PhotoForm, RecipeForm

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'myapp/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    ratings = Rating.objects.filter(post=post)
    average_rating = ratings.aggregate(Avg('score'))['score__avg']
    return render(request, 'myapp/post_detail.html', {'post': post, 'comments': comments, 'average_rating': average_rating})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'myapp/create_post.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'myapp/add_comment.html', {'form': form})

@login_required
def add_rating(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.post = post
            rating.user = request.user
            rating.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = RatingForm()
    return render(request, 'myapp/add_rating.html', {'form': form})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = PhotoForm()
    return render(request, 'myapp/upload_photo.html', {'form': form})

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'myapp/create_recipe.html', {'form': form})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'myapp/recipe_detail.html', {'recipe': recipe})

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    photos = Photo.objects.filter(user=user).order_by('-uploaded_at')
    return render(request, 'myapp/profile.html', {'user': user, 'posts': posts, 'photos': photos})

@login_required
def update_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'myapp/update_profile.html', {'form': form})
