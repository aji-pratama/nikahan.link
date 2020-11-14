import os

from django import forms
from django.conf import settings
from django.contrib import admin

from app.models import Wedding, Invitation, Story


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


class StoryAdminInline(admin.StackedInline):
    model = Story
    extra = 0


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = ['slug', 'bride', 'groom', 'date', 'template']
    form = WeddingModelForm
    inlines = [StoryAdminInline]

    def get_queryset(self, request):
        qs = super(WeddingAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.is_superuser:
            readonly_fields += ['user']

        return readonly_fields


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'attended']

    def get_queryset(self, request):
        qs = super(InvitationAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(wedding=request.user.wedding)
        return qs
