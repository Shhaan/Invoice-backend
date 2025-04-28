from django.urls import path
from .views import LoginView,LogoutView,CurrentUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user/', CurrentUserView.as_view(), name="logout"),



]