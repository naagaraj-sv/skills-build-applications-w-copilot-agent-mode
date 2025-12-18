from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        for model in [Leaderboard, Activity, Workout, User, Team]:
            for obj in model.objects.all():
                if getattr(obj, 'id', None) is not None:
                    obj.delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        workout1 = Workout.objects.create(name='Super Strength', description='Strength training for heroes')
        workout2 = Workout.objects.create(name='Agility Training', description='Agility and reflexes')
        workout1.suggested_for.set(users)
        workout2.suggested_for.set(users)

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Web Swinging', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Suit Up', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Gadget Training', duration=50, date=timezone.now().date())

        self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
        Leaderboard.objects.create(user=users[0], score=100, rank=1)
        Leaderboard.objects.create(user=users[1], score=90, rank=2)
        Leaderboard.objects.create(user=users[2], score=80, rank=3)
        Leaderboard.objects.create(user=users[3], score=70, rank=4)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
