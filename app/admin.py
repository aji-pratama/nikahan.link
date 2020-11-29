import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import Wedding, Bride, Groom, Invitation, Story, Gallery, ImageGallery, InvitationText


class WeddingModelForm(forms.ModelForm):
    template = forms.ChoiceField(widget=forms.Select(), help_text='Template yang akan ditampilkan pada wesbsite undangan.')

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


class BrideAdminInline(admin.StackedInline):
    model = Bride
    extra = 1


class GroomAdminInline(admin.StackedInline):
    model = Groom
    extra = 1


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = ['slug', 'date', 'template']
    form = WeddingModelForm
    inlines = [BrideAdminInline, GroomAdminInline]

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('admin/css/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'admin/js/location_picker.js',
            )

    def get_queryset(self, request):
        qs = super(WeddingAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.is_superuser:
            readonly_fields += ['user', 'publish_status']

        return readonly_fields


@admin.register(Invitation)
class InvitationAdmin(WeddingContentAdmin):
    list_display = ['name', 'code', 'wa_invite', 'attended']

    def wa_invite(self, obj):
        invitation_test = obj.wedding.invitation_text.text if hasattr(obj.wedding, 'invitation_text') else ''
        if obj.phone:
            html = mark_safe(
                '<a class="btn btn-success" href="https://wa.me/{}?text={}" target="_blank"> Undang via Whatsapp </a>'.format(
                    obj.phone,
                    invitation_test
                )
            )
            return html
        return None


@admin.register(InvitationText)
class InvitationTextAdmin(WeddingContentAdmin):
    list_display = ['text']


class ImageGalleryAdminInline(admin.StackedInline):
    model = ImageGallery
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(WeddingContentAdmin):
    list_display = ['title']
    inlines = [ImageGalleryAdminInline]


@admin.register(Story)
class StoryAdmin(WeddingContentAdmin):
    list_display = ['title', 'date']
