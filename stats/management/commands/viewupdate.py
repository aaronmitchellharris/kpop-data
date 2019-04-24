from django.core.management.base import BaseCommand, CommandError
from stats.models import Group, Video

class Command(BaseCommand):
    help = 'Updates views'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for g in Group.objects.all():
            print(g)
            g.total_view_count = 0
            print('total views now 0')
            g.video_count = 0
            print('total videos now 0')
            for v in Video.objects.filter(group=g):
                print(v)
                v.updateViews()
                print('views now ' + str(v.view_count))
                g.total_view_count += v.view_count
                print('group views now ' + str(g.total_view_count))
                g.video_count += 1
                print('video count now ' + str(g.video_count))
                v.save()
            g.save()

        for vid in Video.objects.all():
            print(vid.title + ': ' + str(vid.view_count))