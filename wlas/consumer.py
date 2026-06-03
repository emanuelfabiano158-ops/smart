import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import WaterLevel


class WaterConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        while True:
            data = await self.get_data()
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(2)

    async def get_data(self):
        records = await sync_to_async(list)(
            WaterLevel.objects.order_by('-recorded_at')[:20]
        )

        labels = []
        values = []

        for r in reversed(records):
            labels.append(r.recorded_at.strftime("%H:%M:%S"))
            values.append(r.depth)

        return {
            "labels": labels,
            "values": values
        }