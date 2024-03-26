from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from uuid import uuid4
import os

def upload_to(instance, filename):
    uzanti = filename.split(".")[-1]
    new_name = "{}.{}".format(str(uuid4()),uzanti)
    unique_id = instance.unique_id
    return os.path.join("blog", unique_id , new_name)


# Create your models here.
class myblogger(models.Model):
    user = models.ForeignKey(User,default=1 , null=True , verbose_name='user' , on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=True, verbose_name="Başlık giriniz",
                             help_text="Buraya başlık girilir.")

    icerik = models.TextField(max_length=1000, blank=False, null=True, verbose_name="içerik giriniz.")

    Yayin_Taslak = ((None , "Lütfen birini seçin") ,("yayin" , "YAYIN") , ("taslak" , "TASLAK"))

    yayin_taslak = models.CharField(choices=Yayin_Taslak, max_length=6 , null=True , blank=False)

    image = models.ImageField(default = "deadpool_7.jpg", upload_to = upload_to  , blank=True, verbose_name="Resim" , null=True)

    unique_id = models.CharField(max_length=100 , null=True ,editable=True)

    slug = models.SlugField(null=True, unique=True, editable=False)

    created_date = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "Gönderiler"
        ordering = ['-id']

    def __str__(self):
        return "{} , {}".format(self.title , self.user)

    def get_added_favorite_user(self):
        return self.favorite_blog.values_list('user__username' , flat=True)

    def get_yayin_taslak_html(self):
        if self.yayin_taslak == "taslak":
            return '<span class="label label-danger">{}</span>'.format(self.get_yayin_taslak_display())
        return '<span class="label label-success">{}</span>'.format(self.get_yayin_taslak_display())

    def comment_count(self):
        yorum_sayisi = self.comment.count()
        if yorum_sayisi > 0:
            return yorum_sayisi
        else:
            return "Henüz yorum yok"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "/media/deadpool_7.jpg" # eski postlara default resim döndürür

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(self.title)
        new_slug = slug
        while myblogger.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "{}-{}".format(slug, sayi)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            new_unique_key = str(uuid4())
            self.unique_id = new_unique_key
            self.slug = self.get_unique_slug()
        else:
            blog = myblogger.objects.get(slug=self.slug)
            if blog.title != self.title:
                self.slug = self.get_unique_slug()
        super(myblogger, self).save(*args, **kwargs)

    def get_comment(self):
        return self.comment.all()



class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True , related_name='comment')
    blog = models.ForeignKey(myblogger , on_delete=models.CASCADE , null=True , related_name="comment")
    icerik = models.TextField(max_length=300 , verbose_name='Yorum' , blank=False , null=True ,)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Yorumlar"
    def __str__(self):
        return "%s %s"%(self.user, self.blog)

    def get_screen_name(self):
        if self.user.first_name:
            return "{}".format(self.user.get_full_name())
        return self.user.username


class FavoriteBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='favorite_blog')
    blog = models.ForeignKey(myblogger, on_delete=models.CASCADE, null=True, related_name="favorite_blog")

    class Meta:
        verbose_name_plural = "Favorilerim"

    def __str__(self):
        return "%s %s" % (self.user, self.blog)
