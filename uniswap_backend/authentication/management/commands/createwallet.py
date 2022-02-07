from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from authentication.models import Wallet


class Command(BaseCommand):
    help = 'Add new wallet'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, required=True)
        parser.add_argument('-p', '--password', type=str, required=True)

    def handle(self, *args, **options):
        print(options)
        username = options.get('username')
        query = get_user_model().objects.filter(username=username)
        if not query.exists():
            raise CommandError(f'Invalid username: {username}. User not found!')
        user = query.first()
        password = options.get('password')
        if not user.check_password(password):
            raise CommandError(f'Forbidden! 403')
        while 1:
            address = input("Address: ")
            private_key = input("Private key: ")
            if not address or not private_key:
                self.stdout.write("All fields required")
            else:
                if len(address) < 10 or len(private_key) < 10:
                    self.stdout.write("Min length 10!")
                else:
                    if Wallet.objects.filter(user=user, address=address).exists():
                        self.stdout.write("Wallet already exists!")
                    else:
                        wallet = Wallet.objects.create(user=user, address=address, private_key=private_key)
                        self.stdout.write(self.style.SUCCESS('Successfully added wallet "%s"' % wallet.address))
                        break
