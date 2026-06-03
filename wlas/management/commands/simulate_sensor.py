import random
import time

from django.core.management.base import BaseCommand
from wlas.models import Container, WaterLevel

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Command(BaseCommand):
    help = "Simulate water sensor live data"

    def add_arguments(self, parser):
        parser.add_argument("--live", action="store_true")
        parser.add_argument("--delay", type=int, default=2)

    def handle(self, *args, **options):

        container = Container.objects.first()

        if not container:
            self.stdout.write("No container found")
            return

        delay = options["delay"]
        live = options["live"]

        def generate():
            depth = round(random.uniform(5, 60), 2)

            WaterLevel.objects.create(
                container=container,
                depth=depth
            )

            self.stdout.write(f"Depth: {depth}")

            # LIVE BROADCAST
            channel_layer = get_channel_layer()

            recent = WaterLevel.objects.filter(container=container).order_by("-id")[:10]
            labels = [str(i.id) for i in reversed(recent)]
            values = [i.depth for i in reversed(recent)]

            async_to_sync(channel_layer.group_send)(
                "water_group",
                {
                    "type": "send_water_data",
                    "labels": labels,
                    "values": values
                }
            )

        if live:
            while True:
                generate()
                time.sleep(delay)
        else:
            for _ in range(10):
                generate()
                time.sleep(delay)