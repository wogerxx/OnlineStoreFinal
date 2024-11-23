from django.shortcuts import render,redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm, UpdateAccountForm

User = get_user_model()


class SignUpView(CreateView):
    model = User
    template_name = 'app_users/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

class UpdateAccount(UpdateView):
    template_name = 'app_users/account.html'
    model = User
    form_class = UpdateAccountForm
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        user = form.save(commit=False)
        new_password = form.cleaned_data.get('new_password')

        if new_password:
            user.set_password(new_password)

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('account', kwargs={'user_id': self.request.user.id})
        else:
            return reverse('login')



def logout_view(request):
    logout(request)
    return redirect('products')