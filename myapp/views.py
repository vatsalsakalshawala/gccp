# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import BlogModel, Comment, Profile
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .form import BlogForm
from django.http import HttpResponseForbidden


def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    posts_per_page = 6
    page_number = request.GET.get('page', 1)
    all_blogs = BlogModel.objects.all().order_by('-created_at')
    paginator = Paginator(all_blogs, posts_per_page)

    try:
        blogs = paginator.page(page_number)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'blogs': blogs})


def login_view(request):
    return render(request, 'login.html')


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        comments = Comment.objects.filter(blog=blog_obj).order_by('-created_at')
        context['blog_obj'] = blog_obj
        context['comments'] = comments

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('login_view')

            profile = Profile.objects.get(user=request.user)
            if not profile.is_verified:
                return HttpResponseForbidden('You need to verify your account to comment.')

            content = request.POST.get('content')
            Comment.objects.create(blog=blog_obj, user=request.user, content=content)
            return redirect('blog_detail', slug=slug)
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)


@login_required
def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    return render(request, 'see_blog.html', context)


@login_required
def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            return redirect('/add-blog/')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)


@login_required
def blog_update(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


@login_required
def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')


def header(request):
    return render(request, 'header.html')


def search_view(request):
    query = request.GET.get('query', '')
    if query:
        blogs = BlogModel.objects.filter(
            Q(title__icontains=query) | Q(user__username__icontains=query)
        )
    else:
        blogs = BlogModel.objects.all()

    context = {
        'blogs': blogs,
        'query': query
    }
    return render(request, 'search_results.html', context)
