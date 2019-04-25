from django.db import models
from django.utils import timezone
from . import yt
import datetime


class Group(models.Model):
    name = models.CharField(max_length=200)
    debut_date = models.DateField('debut date')
    video_count = models.IntegerField(default=0)
    total_view_count = models.IntegerField(default=0)
    company = models.CharField(max_length=200)
    current_member_count = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='gallery')
    yt_channel_id = models.CharField(max_length=200)
    pic_url = models.CharField(max_length=200, null=True)

    GIRL = 'G'
    BOY = 'B'
    MIX = 'M'
    GENDER_CHOICES = (
        (GIRL, 'Female'),
        (BOY, 'Male'),
        (MIX, 'Mixed')
    )
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default=GIRL)

    def __str__(self):
        return self.name

    def is_solo(self):
        return (self.current_member_count == 1)

class Video(models.Model):
    group = models.ForeignKey(Group, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    upload_date = models.DateField('upload date')
    view_count = models.IntegerField(default=0)
    yt_video_id = models.CharField(max_length=200)
    thumbnail_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title

    def updateViews(self):
        self.view_count = yt.YTapi.getViewCount(yt_id=self.yt_video_id)[0]
        self.save()

    def updatePic(self):
        self.thumbnail_url = yt.YTapi.getViewCount(yt_id=self.yt_video_id)[1]
        self.save()