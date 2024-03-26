from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
import re



class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=8 , required=True , label="Password" , widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password_confirm = forms.CharField(min_length=8 , label="Password Confirm", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(required=True , choices=UserProfile.SEX , label="Cinsiyet")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username' ,'sex', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields[field].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password' , 'Parolalar eşleşmedi.')
            self.add_error('password_confirm', 'Parolalar eşleşmedi.')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-postayla daha önceden kayıt olunmuş")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten mevcut!")
        return username

class LoginForm(forms.Form):
    username = forms.CharField(required=True , max_length=50 , label='Kullanıcı adı' , widget = forms.TextInput(attrs={'placeholder' : 'Kullanıcı adı veya e-posta giriniz','class' : 'form-control'}))
    password = forms.CharField(required=True , max_length=50 , label='Parola' , widget = forms.PasswordInput(attrs={'placeholder' : 'Şifre', 'class' : 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user =  authenticate(username = username , password = password)
        if not user:
            raise forms.ValidationError('Hatalı kullanıcı adı veya parola girdiniz.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+",username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1 :
                return users.first().username
        return username

class UserProfileUpdateForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea , required=False)
    dogum_tarihi = forms.DateField(input_formats=("%d.%m.%Y",),widget=forms.DateInput(format="%d.%m.%Y") , required=True , label='Doğum Tarihi')
    class Meta:
        model = User
        fields = ['profile_photo','username' , 'first_name' , 'last_name' ,'bio', 'dogum_tarihi' ,'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


    def clean_email(self):
        email = self.cleaned_data.get('email' , None)
        if not email:
            raise forms.ValidationError('Lütfen e-mail giriniz!')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('Bu e-mail adresi sistemde mevcut')

        return email


class UserPasswordChangeForm(forms.Form):
    user = None
    old_password= forms.CharField(min_length=8, required=True,label='Eski şifre' , widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    new_password = forms.CharField(min_length=8 , required=True,label='Yeni şifre',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_confirm = forms.CharField(min_length=8 , required=True,label='Yeni şifre tekrar',widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def __init__(self, user , *args, **kwargs):
        self.user = user
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            self.add_error('new_password' , "Yeni şifreler eşleşmedi")
            self.add_error('new_password_confirm' , 'Yeni şifreler eşleşmedi')

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Lütfen Şifrenizi doğru giriniz.')

        return old_password