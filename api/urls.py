from django.urls import path
from api.views import *

urlpatterns = [
    path('login/', LoginView),
    path('register/', RegisterView)
]
