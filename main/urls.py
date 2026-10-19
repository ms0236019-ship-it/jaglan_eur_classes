from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/submit/", views.submit_inquiry, name="submit_inquiry"),
    path("login/", auth_views.LoginView.as_view(template_name="auth.html", extra_context={"title": "Sign in"}), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
]