from django.db import models
from reader.models import Reader


# Create your models here.

class Subscription(models.Model):
    start_subscription = models.DateField()
    end_subscription = models.DateField()
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, )
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return '{} {} {} '.format(
            self.start_subscription,
            self.end_subscription,
            self.reader.first_name
        )
