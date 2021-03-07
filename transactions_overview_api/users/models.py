from django.db import models


class CustomerUser(models.Model):
    name = models.CharField("full name", max_length=150)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"Client: {self.name} / Email: {self.email} / Age: {self.age}"
