# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import BlogModel, Comment, Profile
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .form import BlogForm, ContactForm
from django.http import HttpResponseForbidden
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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

    return render(request, 'home.html', {'blogs': all_blogs})


# def login_view(request):
#     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['loginUsername']
        password = request.POST['loginPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            login_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session['login_time'] = login_time
            response = redirect('home')
            response.set_cookie('login_time', login_time, max_age=3600)  # Cookie expires in 1 hour
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

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


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
        else:
            print(form.errors)  # Print errors to the console for debugging
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

@login_required
def profile_view(request):
    login_sessions = request.COOKIES.get('login_sessions', '[]')
    login_sessions = json.loads(login_sessions)
    
    return render(request, 'profile.html', {'login_sessions': login_sessions})
