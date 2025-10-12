from django.db import models
from django.urls import reverse


class Task(models.Model):
    """
    This is a model for tasks
    """

    user = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"

    def get_absolute_api_url(self):
        return reverse("task:api-v1:task-detail", kwargs={"pk": self.id})
