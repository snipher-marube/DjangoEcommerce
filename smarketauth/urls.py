from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate')
]
