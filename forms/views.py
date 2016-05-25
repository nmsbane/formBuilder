from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.views import login

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return login(request)

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required
def newform(request):
    return render(request, 'forms/create_form.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
            
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': user_form})

def create_form(request):
    if request.method == 'POST':
        print request.body
    return HttpResponseRedirect(reverse('dashboard'))
    
        
    
    