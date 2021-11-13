from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f'{self.text}'



class Beer(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.id.__str__()}. {self.title}'