from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.conf import settings
from pymongo import MongoClient
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        # Clear all data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Team Marvel', universe='Marvel')
        dc = Team.objects.create(name='Team DC', universe='DC')

        # Users (super heroes)
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Workouts
        workouts = [
            Workout.objects.create(name='Strength Training', description='Full body strength workout', suggested_for='strength'),
            Workout.objects.create(name='Cardio Blast', description='High intensity cardio', suggested_for='cardio'),
        ]

        # Activities
        Activity.objects.create(user=users[0], activity_type='Running', duration_minutes=30, date=date.today())
        Activity.objects.create(user=users[1], activity_type='Cycling', duration_minutes=45, date=date.today())
        Activity.objects.create(user=users[2], activity_type='Swimming', duration_minutes=60, date=date.today())
        Activity.objects.create(user=users[3], activity_type='Yoga', duration_minutes=40, date=date.today())

        # Leaderboard
        Leaderboard.objects.create(user=users[0], score=100, rank=1)
        Leaderboard.objects.create(user=users[1], score=90, rank=2)
        Leaderboard.objects.create(user=users[2], score=80, rank=3)
        Leaderboard.objects.create(user=users[3], score=70, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
