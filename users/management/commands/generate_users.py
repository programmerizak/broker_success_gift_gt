from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate 20 users with a fixed password'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()

            # Generate phone number and trim to fit max length
            phone_number = fake.phone_number()[:13]

            # Create user with fixed password
            user = User.objects.create_user(
                username=email,
                email=email,
                password='12345isaac',
                first_name=first_name,
                last_name=last_name,
                profile_verified=fake.boolean(chance_of_getting_true=50),
                country=fake.country_code(),
                phone_number=phone_number,
                gender=random.choice(['Male', 'Female', 'Rather Not Specify']),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90)
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated users'))
