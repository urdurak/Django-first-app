from django import forms
from .models import Chtmsg

class MessageForm(forms.ModelForm):
    class Meta:
        model = Chtmsg
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget = forms.TextInput(attrs={'placeholder': 'Mesaj Yaz', 'class' : 'form-control'})