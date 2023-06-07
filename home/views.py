from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import BlogForm, UserUpdateForm, ProfileUpdateForm
from .models import BlogModel, Profile


@login_required
def user_profile_view(request):
    user = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user
    }
    return render(request, 'home/profile.html', context)


def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home/home.html', context)


def login_view(request):
    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)

    return render(request, 'home/blog_detail.html', context)


def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user).all()
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'home/see_blog.html', context)


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

            BlogModel.objects.create(
                title=title, content=content, image=image, user=user)

            return redirect('/add-blog/')
    except Exception as e:
        print(e)
    return render(request, 'home/add_blog.html', context)


def blog_update(request, slug):
    context = {}

    try:
        blog_post = BlogModel.objects.get(slug=slug)

        if blog_post.user != request.user:
            return redirect('/')

        initial_dict = {
            'content': blog_post.content, 'image': blog_post.image}
        form = BlogForm(initial=initial_dict)

        if request.method == 'POST':
            form = BlogForm(request.POST)

            if form.is_valid():
                blog_post.title = request.POST.get('title')
                blog_post.content = form.cleaned_data['content']
                blog_post.image = request.FILES.get('image')
                blog_post.save()

        context['blog_post'] = blog_post
        context['form'] = form

    except Exception as e:
        print(e)

    return render(request, 'home/blog_update.html', context)


def delete_blog(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)
    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'home/register.html')


def activate_email(request, token):
    try:
        user = Profile.objects.filter(token=token).first()
        if user:
            user.is_verified = True
            user.save()
            messages.success('Your account have been activated.')
        return redirect('/login/')

    except Exception as e:
        return redirect('/')
