from django.db import models

class GameType(models.Model):
    """GameType model

    fields:
        label (CharField): name of the game type
    """
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label
