from django.forms import ModelForm

from app.models import Invitation


class InvitationForm(ModelForm):

    class Meta:
        model = Invitation
        fields = [
            'wedding',
            'code',
            'name',
            'phone',
            'greeting',
            'attended',
        ]
