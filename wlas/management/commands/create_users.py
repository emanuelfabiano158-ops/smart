from django.core.management.base import BaseCommand
from wlas.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = [
            ("mhigidickson@gmail.com", "DICKSON Mhigi"),
            ("amosgos@gmail.com", "Amosi Godsoni"),
            ("fabina@gmail.com", "Emmanuel Fabiano"),
        ]

        for email, name in users:
            first_name = name.split()[0]
            last_name = " ".join(name.split()[1:])

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": "bsf_keeper",
                }
            )

            if created:
                user.set_password("default123")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {email}"))
            else:
                self.stdout.write(f"Already exists {email}")