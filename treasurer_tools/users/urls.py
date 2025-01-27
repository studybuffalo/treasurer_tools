from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('redirect/', views.UserRedirectView.as_view(), name='redirect'),
    path('<username>/', views.UserDetailView.as_view(), name='detail'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('', views.UserListView.as_view(), name='list'),
]
