from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

#Password Change##
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import PasswordChangingForm, EditUserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
#Password Change#

#Edit/Delete Profile#
from django.views import generic
#Edit/Delete Profile#


def signup(request):
    if request.user.is_authenticated:
        return redirect("all_news")

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = False

        if User.objects.filter(username = username).exists():
            messages.error(request, "Username is already taken. Try with a new username")
            user_exists = True

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email is already taken. Try with a new email")
            user_exists = True

        if user_exists:
            return render(request, 'user/signup.html')
        
        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password= password
        )
        user.save()
        messages.success(request, "Account Created Successfully. Login to Continue")

    return render(request, 'user/signup.html')

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return render(request, 'user/signin.html')
        else:
            login(request,user)
            return redirect("index")
        
    return render(request, 'user/signin.html')

def signout(request):
    logout(request)
    return render(request, 'user/signin.html')

@login_required(login_url="/user/signin")
def profile(request):
    return render(request, 'user/profile.html')

@method_decorator(never_cache, name="dispatch")
class PasswordChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    login_url = "/user/signin/"
    form_class = PasswordChangingForm
    template_name = "user/change_user_password.html"
    success_url = reverse_lazy('profile')
    # success_url = "/user/profile"
    success_message = "Password changed successfully !"

    # def form_invalid(self, form):
    #     messages.add_message(self.request, messages.ERROR, "Please submit the form carefully!")
    #     return redirect('change-password')

    # def get_queryset(self):
    #     if PasswordChangingForm.old_password != self.request.user.password:
    #         messages.error(self.request, "Old password is incorrect")
    #         return render('user/password_change.html',)

                  
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
# @login_required(login_url="/user/signin")
# def change_password(request):
#     if request.method == 'POST':
#         fm= PasswordChangingForm(user = request.user, data = request.POST)
#         if fm.is_valid():
#             fm.save()
#             update_session_auth_hash(request, fm.user)  # Important!
#             messages.success(request, 'Password Changed Successfully!')
#             return redirect('profile')
#         else:
#             # messages.error(request, 'Please correct the error below.')
#             return render(request, 'user/password_change.html', {'form': fm})
#     else:
#         fm = PasswordChangingForm(request.user)
#     return render(request, 'user/password_change.html', {'form': fm})
    

# def password_success(request):
#     return render(request, 'user/password_change_success.html')

@method_decorator(never_cache, name="dispatch")
class EditUserProfile(SuccessMessageMixin,LoginRequiredMixin,generic.UpdateView):
    login_url = "/user/signin/"
    form_class = EditUserProfileForm
    template_name = "user/edit_user_profile.html"
    success_url = reverse_lazy('profile')
    success_message = "Profile Updated Successfully !"

    #Prefill details in form
    def get_object(self):
        return self.request.user
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully!")
        return redirect('profile')

@method_decorator(never_cache, name="dispatch")
class DeleteUserProfile(SuccessMessageMixin,LoginRequiredMixin, generic.DeleteView):
    login_url = "/user/signin/"
    model = User
    template_name = "user/delete_user_profile.html"
    success_url = reverse_lazy('sign_up')
    success_message = "Account has been deleted successfully !"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully!")
        return redirect('profile')