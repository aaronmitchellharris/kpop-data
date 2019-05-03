from django import forms
from .models import Video

class VidForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('group','title','upload_date','yt_video_id','thumbnail_url')