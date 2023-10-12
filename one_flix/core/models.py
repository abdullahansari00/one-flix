from django.db import models


class RequestCount(models.Model):
    url = models.CharField(max_length=200, unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "request_count"
        verbose_name = "Request Count"
        verbose_name_plural = "Request Counts"

    def __str__(self):
        return f"{self.count} | {self.url}"
