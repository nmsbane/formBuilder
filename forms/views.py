import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.views import login
from .models import Form, FormValues, FormContents, FormResults, InputType
from django.views.decorators.csrf import csrf_exempt

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return login(request)

@login_required
def dashboard(request):
    all_forms = Form.objects.filter(user=request.user)
    return render(request, 'account/dashboard.html', {'all_forms': all_forms})

@login_required
def newform(request):
    fieldTypes = InputType.objects.all()
    return render(request, 'forms/create_form.html', {'fieldTypes': fieldTypes})
    
    
def fill_list(form_contents):
    input_list = []
    length = len(form_contents)
    start = 0
    while start < length:
        form = form_contents[start]
        if form.label is not None:
            new_field = {}
            new_field['name'] = form.label
            new_field['type'] = form.input_type
    	    if new_field['type'] == 'checkboxes' or new_field['type'] == 'radio' or new_field['type'] == 'select':
                # import ipdb
                # ipdb.set_trace()
                new_field['options'] = []
                for form_value in form.formvalues_set.all():
                    option_field = {}
                    option_field['name'] = form_value.name
                    option_field['value'] = form_value.value
                    new_field['options'].append(option_field)
            input_list.append(new_field)
            start = start + 1
    return input_list
                
            #     start = start + 1
            #     f1 = form_contents[start]
            #     while start < length and f1.label is None and f1.input_type == new_field['type']:
            #         fv = f1.values
            #         option_field = {}
            #         option_field['name'] = fv.name
            #         option_field['value'] = fv.value
            #         new_field['options'].append(option_field)
            #         start = start + 1
            #         if start < length:
    				    # f1 = form_contents[start]
            #         start = start - 1
    # 		input_list.append(new_field)
    # 	start = start + 1

#[{"type":"text","name":"First Field","value":"first field"},
# {"type":"textarea","name":"Text box1","value":"text box goes here"},
# {"type":"select","name":"Select box","options":[{"name":"Option 1","value":"1"},{"name":"Option 2","value":"2"}],"value":"Option 1"},
# {"type":"radio","name":"Radio button","options":[{"name":"option 1","value":"1"},{"name":"Option 2","value":"2"}],"value":"option 1"},
# {"type":"checkboxes","name":"Check box 1","options":[{"name":"Option 1","value":"1"},{"name":"Option 2","value":"2"}],"value":["","Option 2"]}]
@csrf_exempt
def share_form(request, form_id):
    if request.method == 'GET':
        form_object = get_object_or_404(Form, pk=form_id)
        form_contents = FormContents.objects.filter(form_id = form_object)
        output_list = fill_list(form_contents)
        return render(request, 'forms/share_form.html', {'fields': json.dumps(output_list), 'id': form_id})
        
    elif request.method == 'POST':
        form_object = get_object_or_404(Form, pk=form_id)
        data = json.loads(request.body)
        for field in data:
            if field:
                name = field['name']
                if field['type'] == 'checkboxes':
                    value = ''
                    for selected in field['value']:
                        if selected:
                            value = value + selected + ', '
                else:
                    value = field['value']
                fr = FormResults(form=form_object, name=name, value=value)
                fr.save()
        return render(request, 'forms/thanks.html')
    
    
def form_values(request, form_id):
    form_object = get_object_or_404(Form, pk=form_id)
    form_labels = FormContents.objects.filter(form_id=form_object)
    table_headers = []
    for fc in form_labels:
        table_headers.append(str(fc.label))
    form_results = FormResults.objects.filter(form_id=form_object)
    table_values = []
    # for label in table_headers:
    #     result_obj = {}
    #     result_obj['label'] = label
    #     result_obj['values'] = []
    #     for fr in form_results:
    #         if fr.name == label:
    #             result_obj['values'].append(fr.value)
    #     table_values.append(result_obj)
            
    for fr in form_results:
        result_object = {}
        result_object['name'] = fr.name
        result_object['value'] = fr.value
        table_values.append(result_object)
    return render(request, 'forms/results.html', {'table_headers': table_headers, 
                                                  'table_values': table_values})
    
    


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
                    fc = FormContents(form_id=form, input_type=field['type'], label=field['name'])
                    fc.save()
                elif field['type'] == 'checkboxes' or field['type'] == 'select' or field['type'] == 'radio':
                    # {"name":"Checkbox 1","type":"checkboxes","options":[{"name":"Option 1","value":"1"},
                    # {"name":"Option 2","value":"2"}],"value":{}}
                    fc = FormContents(form_id=form, input_type=field['type'], label=field['name'])
                    fc.save()
                    for key in field['options']:
                        fm = FormValues(form_id=form, name=key['name'], value=key['value'], )
                        fm.save()
                        # import ipdb
                        # ipdb.set_trace()
                        fc.formvalues_set.add(fm)
                        # fc = FormContents(form_id=form, input_type=field['type'], values=fm)
                        # fc.save()
        return HttpResponseRedirect(reverse('dashboard'))
    
        
    
    