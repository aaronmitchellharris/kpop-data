from django import forms
from .models import Video

class VidForm(forms.ModelForm):
    #vid_group = forms.CharField(label='Video Group', max_length=100)
    #vid_title = forms.CharField(label='Video Title', max_length=100)
    #vid_publish_date = forms.DateField(label='Video Publish Date')
    #vid_yt_id = forms.CharField(label='Video YT ID', max_length=100)
    #vid_thumbnail_url = forms.CharField(label='Video Thumbnail Url', max_length=100)

    class Meta:
        model = Video
        fields = ('group','title','upload_date','yt_video_id','thumbnail_url')