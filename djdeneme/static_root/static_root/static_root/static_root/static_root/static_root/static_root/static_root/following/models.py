from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Following(models.Model):
    follower = models.ForeignKey(User ,related_name="follower", null=True , verbose_name="Takip eden Kullanıcı" , on_delete=models.CASCADE)
    followed = models.ForeignKey(User ,related_name="followed", null=True , verbose_name="Takip edilen kullanıcı" , on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Takipleşme sistemi"

    def __str__(self):
        return "{} kullanıcısı {} adlı kullanıcıyı takip etti.".format(self.follower.username,self.followed.username)

    @classmethod
    def follow(cls,follower,followed):
        cls.objects.create(follower=follower,followed=followed)

    @classmethod
    def unfollow(cls,follower,followed):
        cls.objects.filter(follower=follower,followed=followed).delete()

    @classmethod
    def is_user_following(cls,follower,followed):
        return cls.objects.filter(follower=follower , followed=followed).exists()

    @classmethod
    def user_followers_followeds(cls,user):
        data = {'takip_edilenler':0 , 'takipciler':0}
        takip_edilenler = cls.objects.filter(follower=user).count()
        takipciler = cls.objects.filter(followed=user).count()

        data.update({'takip_edilenler':takip_edilenler , 'takipciler':takipciler})
        return data

    @classmethod
    def get_followers(cls,user):
        #Kullanıcının takipçilerini listeler.
        return cls.objects.filter(followed=user)

    @classmethod
    def get_followings(cls, user):
        # Kullanıcının takip ettiği kullanıcıları listeler.
        return cls.objects.filter(follower=user)

    @classmethod
    def get_followed_username(cls,user):
        follewedes = cls.get_followings(user)
        return follewedes.values_list('followed__username' , flat=True)

