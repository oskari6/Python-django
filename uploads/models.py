from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    image = models.ImageField(upload_to='uploads/files/covers')

    def __str__(self):
        return f'{self.title} from {self.year}'
    
class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' ' + self.description