from django.urls import path
from .views import SignupView, UsersView, UserMeView, UserDetailView, UserListView, UserCreateView

app_name = 'api_v1'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('users/', UsersView.as_view(), name='users'),
    path('users/me/', UserMeView.as_view(), name='user_me_view'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='users_list'),
]