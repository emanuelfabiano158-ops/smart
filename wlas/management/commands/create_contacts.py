from django.core.management.base import BaseCommand
from wlas.models import CustomUser, Contact


class Command(BaseCommand):
    help = "Create contacts for BSF users"

    def handle(self, *args, **kwargs):

        users = CustomUser.objects.filter(role="bsf_keeper")

        if not users.exists():
            self.stdout.write(self.style.ERROR("No BSF keeper users found"))
            return

        contacts_data = {
            "mhigidickson@gmail.com": [
                ("email", "mhigidickson@gmail.com"),
                ("phone", "+255700000001"),
                ("whatsapp", "+255700000001"),
            ],
            "amosgos@gmail.com": [
                ("email", "amosgos@gmail.com"),
                ("phone", "+255700000002"),
                ("whatsapp", "+255700000002"),
            ],
            "fabina@gmail.com": [
                ("email", "fabina@gmail.com"),
                ("phone", "+255700000003"),
                ("whatsapp", "+255700000003"),
            ],
        }

        created = 0

        for user in users:
            email = user.email   # ✅ IMPORTANT: real email from object

            if email not in contacts_data:
                continue

            for ctype, value in contacts_data[email]:

                Contact.objects.get_or_create(
                    user=user,   # ✅ REAL USER OBJECT (FIXED)
                    type=ctype,
                    value=value
                )

                created += 1
                self.stdout.write(f"Created {ctype} for {email}")

        self.stdout.write(self.style.SUCCESS(f"Total contacts created: {created}"))