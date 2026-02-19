from django import forms
from mail_messages.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
