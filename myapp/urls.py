from django.urls import path
from myapp import views



urlpatterns = [
    path('home/', views.index, name='home'),
    path('add-employee', views.add_employee, name='add_employee'),
    path('details/<int:pk>', views.details, name='details'),
    path('update/<int:pk>', views.update, name='update'),
    path('management/', views.management, name='management'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]   