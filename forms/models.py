from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class InputType(models.Model):
    type = models.CharField(max_length=255)
    
    def __str__(self):
        return "%s" % self.type


class Form(models.Model):
    name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(null=True)
    
    def save(self, *args, **kwargs):
        super(Form, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return "%s" % (self.name)


class FormResults(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    

class FormValues(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        super(FormValues, self).save(*args, **kwargs) # Call the "real" save() method
    
    def __str__(self):
        return "%s" % (self.value)
    
    
class FormContents(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    input_type = models.CharField(max_length=50)
    label = models.CharField(max_length=255, null=True)
    values = models.OneToOneField(FormValues, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        super(FormContents, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return "%s" % (self.input_type)

    