from django.views import generic
from django.contrib.auth import get_user_model

def LoginView(request):
    return 'Hello'

from .forms import UserRegisterForm
from django.urls import reverse_lazy

User = get_user_model()

class UserRegisterView(generic.CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegisterForm
    success_message = "Registration successful"
