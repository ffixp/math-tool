from django.db import models

class LatexRenderCache(models.Model):
    id = models.AutoField(primary_key=True)
    expression = models.TextField()
    svg = models.TextField()

    def __str__(self):
        return self.expression