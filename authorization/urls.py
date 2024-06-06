from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path('register/', views.register, name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('verify_email/<int:id>', views.verify_email, name='verify_email'),
]