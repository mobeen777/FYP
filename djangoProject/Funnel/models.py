from django.db import models


# Create your models here.

class Funnel(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.CharField(max_length=255, blank=True, null=True)
    properties = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funnel'
