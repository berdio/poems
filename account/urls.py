from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.log_user_in, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<int:uid>/<str:token>', views.activate, name='activate'),
]
