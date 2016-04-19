from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime
import requests

class Command(BaseCommand):
    help = 'Generating fake users'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        include_fields = ','.join([
            'name',
            'email',
            'registered',
            'login'
        ])

        r = requests.get('http://api.randomuser.me', params={
            'results': options['number'],
            'inc': include_fields
        })

        # TODO: we can use bulk_update or DB transaction here
        user_precount = User.objects.count()
        for result in r.json()['results']:
            User.objects.create_user(
                result['login']['username'],
                result['email'],
                result['login']['password'],
                first_name=result['name']['first'],
                last_name=result['name']['last'],
                date_joined=datetime.fromtimestamp(result['registered'])
            )

        user_diffcount = User.objects.count() - user_precount

        self.stdout.write(self.style.SUCCESS(
            'Successfully created {} users'.format(user_diffcount))
        )