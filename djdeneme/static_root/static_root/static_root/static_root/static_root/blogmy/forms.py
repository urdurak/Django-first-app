from django import forms
from .models import myblogger, Comment
banned_email_list = ['ahmet@gmail.com' , 'deneme@hotmail.com']
class IletisimForm(forms.Form):
    isim = forms.CharField( max_length=50 , label='İsim' , required=False )
    soyisim = forms.CharField(max_length=50 , label='Soyisim' , required=False)
    email = forms.EmailField(max_length=50 , label='Email' , required=True)
    email2 = forms.EmailField(max_length=50 , label='Email Doğrula', required=True)
    icerik = forms.CharField( max_length=1000 , label='İçerik' )

    def __init__(self , *args , **kwargs):
        super(IletisimForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class' : 'form-control'}
        self.fields['icerik'].widget = forms.Textarea(attrs={'class' : 'form-control'})

    def clean_isim(self):
        isim = self.cleaned_data.get('isim')
        if isim == "ahmet":
            raise forms.ValidationError("Lütfen ahmet dışında kullanıcı girin.")
        return isim

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in banned_email_list:
            raise forms.ValidationError("Bu email banlanmıştır.Lütfen başka bir hesapla giriniz.")
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            self.add_error('email' , 'Emailler eşleşmedi')
            raise forms.ValidationError("Girdiğiniz emailler birbiri ile eşleşmedi.")


class BlogForm(forms.ModelForm):
    class Meta:
        model = myblogger
        fields = ['title' , 'icerik', 'yayin_taslak' ,'image']

    def __init__(self , *args , **kwargs):
        super(BlogForm, self).__init__(*args , **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget.attrs['rows'] = 10


class PostSorguForm(forms.Form):
    Yayin_Taslak = (('all' , "HEPSİ") ,("yayin" , "YAYIN") , ("taslak" , "TASLAK"))

    search = forms.CharField(required=False , max_length=500 , widget=forms.TextInput(attrs={'placeholder' :'Bir şey ara' ,'class' : 'form-control'}))
    taslak_yayin = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Yayin_Taslak, required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget = forms.TextInput(attrs={'placeholder': 'Yorum Yap', 'class' : 'form-control'})
