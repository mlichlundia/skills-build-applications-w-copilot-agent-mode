from django.core.management.base import BaseCommand
from django.db import connection
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write('Creating users (super heroes)...')
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create(**hero) for hero in marvel_heroes]
        dc_users = [User.objects.create(**hero) for hero in dc_heroes]

        self.stdout.write('Creating teams...')
        marvel_team = Team.objects.create(name='Team Marvel')
        marvel_team.members.set(marvel_users)
        dc_team = Team.objects.create(name='Team DC')
        dc_team.members.set(dc_users)

        self.stdout.write('Creating activities...')
        for user in marvel_users + dc_users:
            Activity.objects.create(user=user, activity_type='Training', duration=60, calories=500, date=date(2024, 5, 1))

        self.stdout.write('Creating workouts...')
        workout1 = Workout.objects.create(name='Hero Cardio', description='Run 5km and 50 pushups')
        workout1.suggested_for.set(marvel_users + dc_users)

        self.stdout.write('Creating leaderboard...')
        for user in marvel_users + dc_users:
            Leaderboard.objects.create(user=user, score=1000, week=date(2024, 5, 5))

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('''
                db = connection.db_conn.client.get_database('octofit_db')
                db.users.create_index([('email', 1)], unique=True)
            ''')
        self.stdout.write(self.style.SUCCESS('Unique index on email field created for users collection.'))
