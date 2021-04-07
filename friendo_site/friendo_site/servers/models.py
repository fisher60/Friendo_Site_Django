from django.db import models


class Server(models.Model):
    server_id = models.CharField(max_length=60, unique=True)
    dogeboard_id = models.CharField(max_length=60, blank=True, null=True)
    dogeboard_emoji = models.CharField(max_length=60, blank=True, null=True)
    dogeboard_reactions_required = models.IntegerField(default=5)

    def __str__(self):
        return f"Server Id: {self.server_id}"
