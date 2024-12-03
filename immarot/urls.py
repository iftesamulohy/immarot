from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index2.as_view(),name="index"),
    path("login/", views.Login.as_view(),name="login"),
    # path('<str:menu_slug>/<str:action>/', views.MenuDetailView.as_view(), name='menu-detail'),
    # path('<str:menu_slug>/<str:action>/<str:app_name>/<str:model_name>/<str:fields>/', views.MenuDetailView.as_view(), name='menu-detail'),
    # In your urls.py
    path('<str:menu_slug>/<str:action>/<str:app_name>/<str:model_name>/<str:fields>/', views.MenuDetailView3.as_view(), name='menu-detail'),

]
