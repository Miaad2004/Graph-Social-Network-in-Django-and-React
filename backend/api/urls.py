from django.urls import path
from .views import *

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("register/", UserRegistrationView.as_view()),
    path("get_user/", GetUserInfoView.as_view()),
    path("delete_account/", UserDeleteView.as_view()),
    path("get_all_users/", GetAllUsersView.as_view()),
    path("get_connections/", GetAllConnectionsView.as_view()),
    path("add_connection/", AddConnectionView.as_view()),
    path("remove_connection/", RemoveConnectionView.as_view())
]
