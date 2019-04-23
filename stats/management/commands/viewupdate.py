from django.core.management.base import BaseCommand, CommandError
from stats.models import Group, Video

class Command(BaseCommand):
    help = 'Updates views'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for g in Group.objects.all():
            g.total_view_count = 0
            g.video_count = 0
            for v in Video.objects.filter(group=g):
                v.updateViews()
                g.total_view_count += v.view_count
                g.video_count += 1
                v.save()
            g.save()

