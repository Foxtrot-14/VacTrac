from audioop import reverse
from django.db import models

class Vaccine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    due = models.IntegerField()
    dose = models.CharField(max_length=15)
    route = models.CharField(max_length=50)
    site = models.CharField(max_length=25)
    
    def get_absolute_url(self):
        return reverse("vaccine_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name