from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('add-blog/', add_blog, name='add_blog'),
    path('blog-detail/<slug:slug>', blog_detail, name='blog_detail'),
    path('see-blog/', see_blog, name='see_blog'),
    path('delete_blog/<slug>/', delete_blog, name='delete_blog'),
]
