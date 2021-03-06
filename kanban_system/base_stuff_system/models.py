from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class ExtendedUser(models.Model):
    date_of_birth = models.DateField(help_text="Please use the following format: <em>%d/%m/%Y</em>.")
    image = models.ImageField(default='default.jpg', upload_to='profiles', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Company(models.Model):
    title = models.CharField(max_length=20, blank=False)
    employee = models.ManyToManyField(User, related_name='employee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=20, blank=False, unique_for_date='date')
    description = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    in_progress = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    form_error = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Notes(models.Model):
    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=300, blank=False)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
