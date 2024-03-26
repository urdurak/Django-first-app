from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponseBadRequest , HttpResponseForbidden , JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string
from djdeneme.settings import MEDIA_ROOT
from django.template.defaultfilters import slugify
import os

from .models import myblogger , Comment , FavoriteBlog
from .forms import IletisimForm, BlogForm, PostSorguForm, CommentForm
from blogmy.decorators import is_post





@login_required(login_url=reverse_lazy('user-login'))
def post_list(request):
    posts = myblogger.objects.all()
    # blog = get_object_or_404(myblogger, slug=slug)
    form = PostSorguForm(data=request.GET or None)
    form2 = CommentForm()
    page = request.GET.get('page' , 1)
    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin')
        search = form.cleaned_data.get('search',None)
        if search:
            posts = posts.filter(Q(icerik__icontains=search) | Q(title__icontains=search )).distinct()
        if taslak_yayin and taslak_yayin != 'all':
            posts = posts.filter(yayin_taslak=taslak_yayin)

    paginator = Paginator(posts,3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {"posts": posts , 'form' : form , 'form2':form2 }
    return render(request, 'blog/blog-list.html', context=context)

@login_required(login_url=reverse_lazy('user-login'))
def post_update(request, slug):
    blog = get_object_or_404(myblogger, slug=slug)
    if request.user != blog.user:
        return HttpResponseForbidden()
    form = BlogForm(instance=blog, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        saved_form = form.save(commit=True)
        msg = "Tebrikler <strong>{}</strong> isimli postunuz başarıyla düzenlendi".format(saved_form.title)
        messages.success(request, msg)
        return HttpResponseRedirect(saved_form.get_absolute_url())
    return render(request, 'blog/post-update.html', context={'blog': blog, 'form': form})

@login_required(login_url=reverse_lazy('user-login'))
def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))
    form = BlogForm()
    context = {"form": form}
    if request.method == 'POST':
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            created_blog = form.save(commit=False)
            created_blog.user = request.user
            created_blog.save()
            msg = "Tebrikler <strong>{}</strong> isimli postunuz başarıyla oluşturuldu".format(created_blog.title)
            messages.success(request, msg)
            return HttpResponseRedirect(created_blog.get_absolute_url())
            # return HttpResponseRedirect(reverse('post-detail', kwargs={'slug':created_blog.slug} ))  # This command can open detail page
    return render(request, 'blog/post-create.html', context)

@login_required(login_url=reverse_lazy('user-login'))
def post_detail(request, slug):
    blog = get_object_or_404(myblogger, slug=slug)  # objeyi çek yada 404 hatası
    form = CommentForm()
    return render(request, 'blog/post-detail.html', context={'blog': blog , 'form' : form})

@login_required(login_url=reverse_lazy('user-login'))
@is_post
def add_comment(request, slug):
    blog = get_object_or_404(myblogger,slug=slug)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        new_comment.user = request.user
        new_comment.save()
        messages.success(request , 'yorumunuz basarılı bir şekilde oluşturuldu')
        return HttpResponseRedirect((blog.get_absolute_url()))


@login_required(login_url=reverse_lazy('user-login'))
def add_or_remove_favorite(request,slug):
    # url = request.GET.get('next' , None)
    if not request.is_ajax():  # Ajax isteği değilse bad response hatası
        return HttpResponseBadRequest()
    blog = get_object_or_404(myblogger , slug = slug)
    print(blog , "finduk")
    favori_blog = FavoriteBlog.objects.filter(blog=blog , user = request.user)
    print(favori_blog , 'fistuk')
    if favori_blog.exists():
        favori_blog.delete()
    else:
        FavoriteBlog.objects.create(blog = blog , user= request.user)
    # if not url:
    #     reverse('post-list')
    data = {'is_valid':True}
    return JsonResponse(data=data)


@login_required(login_url=reverse_lazy('user-login'))
def post_delete(request, slug):
    blog = get_object_or_404(myblogger, slug=slug)  # objeyi çek yada 404 hatası
    if request.user != blog.user:
        return HttpResponseForbidden()
    if os.path.isfile(blog.image.path):
        os.remove(blog.image.path)
    blog.delete()
    msg = "<strong>{}</strong> isimli postunuz başarıyla silindi".format(blog.title)
    messages.warning(request, msg)
    return HttpResponseRedirect(reverse('post-list'))


mesajlar = []


def iletisim(request):
    form = IletisimForm(data=request.GET or None)
    if form.is_valid():
        isim = form.cleaned_data.get("isim")
        soyisim = form.cleaned_data.get("soyisim")
        email = form.cleaned_data.get("email")
        icerik = form.cleaned_data.get("icerik")
        data = {'isim': isim, 'soyisim': soyisim, 'email': email, 'icerik': icerik}
        mesajlar.append(data)
        return render(request, 'iletisim.html', context={'mesajlar': mesajlar, 'form': form})
    return render(request, 'gecici/profile2.html', context={'form': form})


def deneme(request):
    if request.is_ajax():
        context = {'msg' : 'merhaba ajax'}
        return JsonResponse(data=context)
    return render(request , 'deneme.html')

def deneme_ajax(request):

    if not request.is_ajax():
        return HttpResponseBadRequest()
    isim = request.POST.get('isim')
    return JsonResponse(data={'isim':isim, 'he':'hasdsad'})

def deneme_ajax2(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    context = {'ogrenci':{'isim_soyisim':'ahmet durmaz' , 'ogretmen_isim_soyisim' :'Temel korkmaz'}}
    html = render_to_string('ogrenci_velisine_mesaj.html' , context=context , request=request)
    data = {'html': html}
    return JsonResponse(data=data)

def mylist(request):
    return render(request , 'gecici/mypost.html')

def chtdeneme(request):
    return render(request , 'gecici/chattemp.html')