from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from .services import handle_user
from .forms import ChangeForm, LoginUserForm, RegisterUserForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
class RegisterUser(SuccessMessageMixin, CreateView):
    """Show register form"""

    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    error_message = "Registration error"

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(RegisterUser, self).dispatch

        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        return dispatch_method(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Registration"
        return context


class LoginUser(SuccessMessageMixin, LoginView):

    """Autorization class"""

    form_class = LoginUserForm
    template_name = "accounts/login.html"
    error_message = "Something went wrong"
    success_url = reverse_lazy("home")

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(LoginUser, self).dispatch

        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        return dispatch_method(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        try:

            username = kwargs.get("data").get("username")
            user_active = handle_user.get_user_by_email(username).is_active
            if not user_active:
                messages.error(self.request, "Unfortunatelly this user is unactive")
        except Exception:
            pass
        return kwargs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Sign in"
        return context


class LogoutUser(LogoutView, SuccessMessageMixin):

    next_page = "home"
    success_message = "Logout successfully"


@login_required(login_url="login")
def get_profile(request, user_id):

    user = handle_user.get_user_by_id(user_id)

    context = {
        "user": user,
    }

    return render(request, "base/profile.html", context=context)


@login_required(login_url="login")
def get_profile_edit(request, user_id):

    user = handle_user.get_user_by_id(user_id)
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=user)
        if form.is_valid():
            try:

                form.save()
                return HttpResponseRedirect(
                    reverse("profile", kwargs={"user_id": user_id})
                )
            except Exception as er:
                print(er)
                messages.error(request, er)
        else:
            return "invalid"

    form = ChangeForm(instance=user)

    context = {"user": user, "form": form}

    return render(request, "base/profile_edit.html", context=context)


@login_required(login_url="/accounts/login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Ups, noe gikk galt. Prøv på nytt")

    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})
