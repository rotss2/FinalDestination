from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

# OPTIONAL: only if you used the LogoutGetView approach
class LogoutGetView(auth_views.LogoutView):
    http_method_names = ["get", "post", "options"]

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutGetView.as_view(), name="logout"),  # or auth_views.LogoutView.as_view()
]
