from django.core.management.base import BaseCommand, CommandError
from stats.models import Group, Video

class Command(BaseCommand):
    help = 'Updates pictures'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for g in Group.objects.all():
            if Video.objects.filter(group=g):
                vid = Video.objects.filter(group=g).order_by('upload_date').reverse()[0]
                vid.updatePic()
                g.pic_url = vid.thumbnail_url
                g.save()