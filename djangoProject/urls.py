"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from food.urls import LandingPageView
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', LandingPageView.as_view(), name='landing'),
    path("food/", include("food.urls")),
    path('orders/', include('orders.urls', namespace='orders')),
    path("register/", users_views.register, name="Register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("profile/", users_views.profile, name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
                   # ... the rest of your URLconf goes here ...
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


