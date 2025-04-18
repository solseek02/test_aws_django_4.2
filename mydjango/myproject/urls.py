from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # myapp의 모든 URL 패턴 포함
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
]

