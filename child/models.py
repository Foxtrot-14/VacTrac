from django.db import models
from django.urls import reverse
from account.models import User
from vaccine.models import Vaccine
# Create your models here.
CHILD_GENDER = (
    (0,"Male"),
    (1,"Female"),
)

class Child(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.IntegerField(choices=CHILD_GENDER)
    adder = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='added_by') 
    vaccines_taken = models.ManyToManyField(Vaccine, through='Taken', related_name='done')
    vaccines_to_take = models.ManyToManyField(Vaccine, through='Due', related_name='upcoming') 
    
    def get_absolute_url(self):
        return reverse("child_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name

class Taken(models.Model):
    id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    taken_on = models.DateField(auto_now=False, auto_now_add=False)
    reactions = models.CharField(max_length=1000)
    
    def get_absolute_url(self):
        return reverse("taken_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.vaccine.name
    
class Due(models.Model):
    id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='due_on')
    due_on = models.DateField(auto_now=False, auto_now_add=False)
    
    def get_absolute_url(self):
        return reverse("due_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.vaccine.name