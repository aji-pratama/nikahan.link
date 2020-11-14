import os

from django import forms
from django.conf import settings
from django.contrib import admin

from app.models import Wedding


class WeddingModelForm(forms.ModelForm):
    template = forms.ChoiceField(widget=forms.Select())

    class Meta:
        model = Wedding
        exclude = []

    def __init__(self, *args, **kwargs):
        super(WeddingModelForm, self).__init__(*args, **kwargs)
        template_html = os.listdir(os.path.join(settings.BASE_DIR, 'templates/wedding'))
        self.fields['template'].choices = zip(template_html, template_html)
        self.initial['template'] = 'default.html'


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug', 'template']
    form = WeddingModelForm
