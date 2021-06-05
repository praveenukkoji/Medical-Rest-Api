from django.urls import path

from user.views import AddUserView, GetAllUserView, GetUserView, UpdateUserView, DeleteUserView, \
    AddRoleView, GetAllRoleView, GetRoleView, UpdateRoleView, DeleteRoleView, LoginView, LogoutView

urlpatterns = [
    path('addusers/', AddUserView.as_view()),
    path('getallusers/', GetAllUserView.as_view()),
    path('getusers/', GetUserView.as_view()),
    path('updateusers/', UpdateUserView.as_view()),
    path('deleteusers/', DeleteUserView.as_view()),

    path('addroles/', AddRoleView.as_view()),
    path('getallroles/', GetAllRoleView.as_view()),
    path('getroles/', GetRoleView.as_view()),
    path('updateroles/', UpdateRoleView.as_view()),
    path('deleteroles/', DeleteRoleView.as_view()),

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
