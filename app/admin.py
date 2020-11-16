import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import Wedding, Invitation, Story, Gallery, InvitationText


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


class WeddingContentAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(WeddingContentAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(wedding=request.user.wedding)
        return qs


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = ['slug', 'bride', 'groom', 'date', 'template']
    form = WeddingModelForm

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
class InvitationAdmin(WeddingContentAdmin):
    list_display = ['name', 'code', 'wa_invite', 'attended']

    def wa_invite(self, obj):
        if obj.phone:
            return mark_safe(
                '<a class="btn btn-success" href="https://wa.me/{}?text={}" target="_blank"> Undang via Whatsapp </a>'.format(
                    obj.phone,
                    obj.wedding.invitation_text.text
                )
            )
        return None


@admin.register(InvitationText)
class InvitationTextAdmin(WeddingContentAdmin):
    list_display = ['text']


@admin.register(Gallery)
class GalleryAdmin(WeddingContentAdmin):
    list_display = ['title']


@admin.register(Story)
class StoryAdmin(WeddingContentAdmin):
    list_display = ['title']
