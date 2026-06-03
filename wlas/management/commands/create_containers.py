from django.core.management.base import BaseCommand
from wlas.models import Container


class Command(BaseCommand):
    help = "Create BSF containers for sensor system"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=3,
            help="Number of containers to create (default: 3)"
        )

    def handle(self, *args, **options):
        count = options["count"]

        containers_data = [
            {
                "label": "BSF-01",
                "location": "DUCE Site A",
                "max_depth": 50,
                "alert_min": 10,
                "alert_max": 45,
            },
            {
                "label": "BSF-02",
                "location": "DUCE Site B",
                "max_depth": 60,
                "alert_min": 15,
                "alert_max": 50,
            },
            {
                "label": "BSF-03",
                "location": "DUCE Site C",
                "max_depth": 55,
                "alert_min": 12,
                "alert_max": 48,
            },
        ]

        created = 0

        for i in range(min(count, len(containers_data))):
            data = containers_data[i]

            obj, created_flag = Container.objects.get_or_create(
                label=data["label"],
                defaults=data
            )

            if created_flag:
                self.stdout.write(self.style.SUCCESS(f"Created {obj.label}"))
                created += 1
            else:
                self.stdout.write(f"Already exists: {obj.label}")

        self.stdout.write(self.style.SUCCESS(f"\nTotal new containers: {created}"))