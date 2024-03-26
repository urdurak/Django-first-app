from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from uuid import uuid4

# Create your models here.

class Chtmsg(models.Model):
    sender = models.ForeignKey(User ,related_name="sender", null=True , verbose_name="Mesaj Gönderen Kullanıcı" , on_delete=models.CASCADE)
    receiver = models.ForeignKey(User ,related_name="receiver", null=True , verbose_name="Mesaj Alan kullanıcı" , on_delete=models.CASCADE)
    icerik = models.TextField(max_length=1000 , verbose_name='message' , blank=False , null=True)
    message_date = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name_plural= "Mesajlaşma Sistemi"

    def __str__(self):
        return "{} kullanıcısı {} adlı kullanıcıya şu mesajı gönderdi : {}".format(self.sender.username,self.receiver.username,self.icerik)


class Chtroom(models.Model):
    owner1 = models.ForeignKey(User, related_name="owner1", null=True, verbose_name="kurucu1", on_delete=models.CASCADE)
    owner2 = models.ForeignKey(User, related_name="owner2", null=True, verbose_name="kurucu2", on_delete=models.CASCADE)
    room_id = models.SlugField(null=True, unique=True, editable=False , verbose_name='unique_room')

    class Meta:
        verbose_name_plural = "Chat Odaları"

    def __str__(self):
        return "{}-{} Chat Odası".format(self.owner1,self.owner2)

    def clean_owner2(self):
        if self.owner1 != self.owner2:
            return True
        return False

    def get_room_url(self):
        return reverse('personal-inbox' , kwargs={'room_id': self.room_id})

    def save(self, *args, **kwargs):
        if self.id is None:
            new_unique_id = str(uuid4())
            self.room_id = slugify(new_unique_id)
        super(Chtroom, self).save(*args, **kwargs)
