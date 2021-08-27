"""vending_machinet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vending_machine.views.v1.product import create_product, get_product, update_product, delete_product, buy_product
from vending_machine.views.v1.user import create_user, update_user, delete_user, get_user, login, deposit_coins, \
    reset_deposit, logout

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("", include(router.urls)),
    path(r"user/create", create_user),
    path(r"user/<user_id>/update", update_user),
    path(r"user/<user_id>/delete", delete_user),
    path(r"user/<user_id>/get", get_user),
    path(r"user/login", login),
    path(r"user/logout", logout),
    path(r"user/deposit", deposit_coins),
    path(r"user/reset_deposit", reset_deposit),
    path(r"product/create", create_product),
    path(r"product/<id>/get", get_product),
    path(r"product/<id>/update", update_product),
    path(r"product/<id>/delete", delete_product),
    path(r"product/buy", buy_product),
]
