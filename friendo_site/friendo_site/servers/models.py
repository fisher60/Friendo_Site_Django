from django.db import models


class Server(models.Model):
    server_id = models.CharField(max_length=60)
    dogeboard_id = models.CharField(max_length=60, blank=True, null=True)
