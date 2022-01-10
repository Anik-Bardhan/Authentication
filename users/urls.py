from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, DeleteView, UpdateView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete/<str:pk>/', DeleteView.as_view(), name='delete'),
    path('update/<str:pk>', UpdateView.as_view(), name = "update")
]
