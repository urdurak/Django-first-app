from django.shortcuts import render , HttpResponseRedirect,reverse , get_object_or_404
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm , LoginForm , UserProfileUpdateForm , UserPasswordChangeForm
from blogmy.decorators import anonymous_required
from .models import UserProfile
from following.models import Following

@anonymous_required
def register(request):
    # if not request.user.is_anonymous: # yetkili ise
    #     return HttpResponseRedirect(reverse('post-list'))
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        username =  form.cleaned_data.get('username')
        password =  form.cleaned_data.get('password')
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        user = authenticate(request=request, username= username, password = password)
        if user is not None:
            if user.is_active:
                login(request , user)
                messages.success(request, '<b>tebrikler kayıt olundu</b>', extra_tags='success')
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return render(request,'auths/register.html' , context={'form' : form})


@anonymous_required
def user_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                msg = "<b>Merhaba {}.Hoşgeldin</b>".format(username)
                messages.success(request, msg, extra_tags='success')
                return HttpResponseRedirect(reverse('post-list'))
    return render(request , 'auths/login.html' , context ={'form': form})

def user_logout(request):
    username = request.user.username
    logout(request)
    msg = "<b>başarıyla çıkış yapıldı.</b>"
    messages.success(request , msg , extra_tags="success" )
    return HttpResponseRedirect(reverse('user-login'))

def user_profile(request,username):
    is_following = False
    user = get_object_or_404(User,username=username)
    takipci_ve_takip_edilen = Following.user_followers_followeds(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    #eğer kendi profiline girmişse fonksiyon çalışmasın
    if user != request.user:
        is_following = Following.is_user_following(follower= request.user, followed=user)
    context = {'takipciler':takipciler,'takip_edilenler':takip_edilenler,'is_following': is_following, 'user': user, 'page': 'user-profile'}
    return render(request, 'auths/profile/user_profile.html', context=context)

def user_settings(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    dogum_tarihi = request.user.userprofile.dogum_tarihi
    initial = {'sex': sex, 'bio' :bio , 'profile_photo':profile_photo , 'dogum_tarihi' : dogum_tarihi}
    form = UserProfileUpdateForm(initial=initial ,instance=request.user , data=request.POST or None , files=request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=True)
            bio = form.cleaned_data.get('bio', None)
            sex = form.cleaned_data.get('sex', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)
            dogum_tarihi = form.cleaned_data.get('dogum_tarihi' , None)
            user.userprofile.sex = sex
            user.userprofile.profile_photo = profile_photo
            user.userprofile.bio = bio
            user.userprofile.dogum_tarihi = dogum_tarihi
            user.userprofile.save()
            messages.success(request, 'Kullanıcı bilgileriniz başarıyla değiştirildi.', extra_tags='success')
        else:
            messages.warning(request , 'Lütfen formları doğru doldurunuz.' ,  extra_tags='danger')

    return render(request , 'auths/profile/settings.html' , context={'form':form })

def user_password_change(request):
    form = UserPasswordChangeForm(user=request.user , data=request.POST or None)
    if form.is_valid():
        new_password = form.cleaned_data.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request,'Şifreniz başarıyla değiştirildi.' , extra_tags='success')
    return render(request, 'auths/profile/password_change.html' , context={'form' : form})

def my_favorites(request,username):
    is_following = False
    user = get_object_or_404(User,username=username)
    takipci_ve_takip_edilen = Following.user_followers_followeds(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    #eğer kendi profiline girmişse fonksiyon çalışmasın
    if user != request.user:
        is_following = Following.is_user_following(follower= request.user, followed=user)
    context = {'takipciler':takipciler,'takip_edilenler':takip_edilenler,'is_following': is_following, 'user': user, 'page': 'my-favorites'}
    return render(request, 'auths/profile/myfavorites.html' ,context=context)