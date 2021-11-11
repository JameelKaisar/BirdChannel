"""BirdChannel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.aboutpage, name="aboutpage"),
    path("contact/", views.contactpage, name="contactpage"),
    path("help/", views.helppage, name="helppage"),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login_request"),
    path("change-password/", views.change_password, name="change_password"),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("admin/", views.admin_section, name="admin_section"),
    path("birds/", views.birds_section, name="birds_section"),
    path("conservation/", views.conservation_categories, name="conservation_categories"),
    path("conservation/<slug:category_slug>", views.conservation_content, name="conservation_content"),
    path("birding/", views.birding_categories, name="birding_categories"),
    path("birding/<slug:category_slug>", views.birding_content, name="birding_content"),
    path("delete-data", views.delete_data, name="delete_data"),
    path("edit-data", views.edit_data, name="edit_data"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
