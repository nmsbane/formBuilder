from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.views import login
from .models import Form, FormValues, FormContents

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


# input is of this form
# [
#    {"type":"text","name":"Name","placeholder":"Please enter your name"},
#    {"name":"Input field","type":"text"}
# ]
def create_form(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        form = None
        for field in data:
            if field:
                if field['name'] == 'Name':
                    form = Form(name=field.get('value', str(request.user.id) +'form' ), user=request.user)
                    form.save()
                elif field['type'] == 'text' or field['type'] == 'textarea' or field['type'] == 'email':
                    fm = FormValues(form_id=form, value=field['name'])
                    fm.save()
                    fc = FormContents(form_id=form, input_type=field['type'], values=fm)
                    fc.save()
                elif field['type'] == 'checkboxes' or field['type'] == 'select' or field['type'] == 'radio':
                    # {"name":"Checkbox 1","type":"checkboxes","options":[{"name":"Option 1","value":"1"},
                    # {"name":"Option 2","value":"2"}],"value":{}}
                    fm = FormValues(form_id=form, value=field['name'])
                    fm.save()
                    fc = FormContents(form_id=form, input_type=field['type'], values=fm)
                    fc.save()
                    for key in field['options']:
                        fm = FormValues(form_id=form, value=key['name'] + ' + ' + key['value'] )
                        fm.save()
                        fc = FormContents(form_id=form, input_type=field['type'], values=fm)
                        fc.save()
        return HttpResponseRedirect(reverse('dashboard'))
    
        
    
    