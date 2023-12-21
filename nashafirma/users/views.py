from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views import generic as view
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import RegistrationForm, LoginForm, EditProfileForm, FeedbackCreateForm
from .models import SiteUser, Feedback
from utils.utils import get_client_ip
from utils.email import send_contact_email_message

UserModel = get_user_model()


def get_profile(pk):
    try:
        return UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist as ex:
        return None


class UserRegistrationView(view.CreateView):
    title = "Реєстрація"
    model = UserModel
    template_name = "users/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(auth_views.LoginView):
    title = "Вхід"
    form_class = LoginForm
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_success_url(self):
        return reverse_lazy("home")


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, view.DetailView):
    title = "Профіль"
    model = SiteUser
    template_name = "users/profile_details.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.request.user == self.object
        context["title"] = self.title
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        profile = get_object_or_404(SiteUser, pk=pk)
        return profile

    def test_func(self):
        return self.request.user.pk == self.kwargs.get("pk")


class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, view.UpdateView):
    title = "Редагувати профіль"
    model = SiteUser
    form_class = EditProfileForm
    template_name = "users/profile_edit.html"

    def get_success_url(self):
        return reverse_lazy("profile_details", kwargs={"pk": self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context["user"] = self.object
        return context

    def test_func(self):
        return self.request.user.pk == self.kwargs.get("pk")


class DeleteProfileView(LoginRequiredMixin, UserPassesTestMixin, view.DeleteView):
    title = "Видалити профіль"
    model = SiteUser
    template_name = "users/profile_delete.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def test_func(self):
        return self.request.user.pk == self.kwargs.get("pk")


class UserLogOutView(auth_views.LogoutView):
    next_page = reverse_lazy("login")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    title = "Відновлення паролю"
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    success_message = "На Ваш %(email)s було відправлено листа для зміни пароля."
    subject_template_name = "users/password_reset_subject.txt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class TermsView(TemplateView):
    title = "Умови використання"
    template_name = 'users/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    title = "Контакти"
    model = Feedback
    form_class = FeedbackCreateForm
    template_name = "users/feedback.html"
    extra_context = {'title': 'Контактна форма'}
    success_url = reverse_lazy('feedback_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(
                feedback.subject, feedback.email, feedback.content, feedback.ip_address, feedback.user_id)
        return super().form_valid(form)


class FeedbackSuccessView(TemplateView):
    title = "Лист надіслано вдало"
    template_name = 'users/feedback_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
