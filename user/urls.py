from django.urls import path
# from user.views import signup
from user import views

urlpatterns = [
    path("signup/",views.signup , name="sign_up"),
    path("signin/",views.signin , name="signin"),
    path("signout/",views.signout , name="signout"),
    path("profile/",views.profile, name="profile"),
    path("change_password/",views.PasswordChangeView.as_view(), name="change-password"),
    # path("change_password/", views.change_password, name='change-password'),
    path("edit_profile/",views.EditUserProfile.as_view(), name="edit-profile"),

]