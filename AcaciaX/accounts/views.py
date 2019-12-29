from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class ProfileSummaryView(ListView):
    model = User
    template_name = 'profile-summary.html'

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class ProfileNotificationView(ListView):
    model = User
    template_name = 'profile-notifications.html'

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class ProfileActivityView(ListView):
    model = User
    template_name = 'profile-activity.html'

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class ProfileMessageView(ListView):
    model = User
    template_name = 'profile-messages.html'

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class ProfileBadgeView(ListView):
    model = User
    template_name = 'profile-badges.html'

    def get_object(self):
        return self.request.user
