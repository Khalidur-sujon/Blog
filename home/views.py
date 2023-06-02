from django.shortcuts import render, redirect
from .form import BlogForm
from .models import BlogModel


def home(request):
    return render(request, 'home/home.html')


def login_view(request):
    return render(request, 'home/login.html')


def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES('image')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid:
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                title=title, content=content, image=image, user=user)
            blog_obj.save()
            redirect('/add-blog/')
    except Exception as e:
        print(e)
    return render(request, 'home/add_blog.html', context)


def register_view(request):
    return render(request, 'home/register.html')
