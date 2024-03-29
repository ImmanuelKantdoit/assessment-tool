"""
Url mappings for the user API
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('edit/', views.ManageUserView.as_view(), name='edit'),
    path('user/', views.RetrieveUserView.as_view(), name='user'),
    path(
        'users/',
        views.RetrieveAllUsersView.as_view(),
        name='all-users'
    ),
    path(
        'edit/<int:pk>/',
        views.EditUserDetailsView.as_view(),
        name='edit-user-details'
    ),
]
