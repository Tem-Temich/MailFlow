from django import forms

from clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'fio', 'comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
