from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('employee/', views.add_employee, name='add_employee'),
]
