from django.db import models
from django.core.validators import MinValueValidator


class Guild(models.Model):
    guild_id = models.BigIntegerField(unique=True)
    dogeboard_id = models.BigIntegerField(blank=True, null=True)
    dogeboard_emoji = models.CharField(max_length=60, blank=True, null=True)
    dogeboard_reactions_required = models.PositiveIntegerField(
        default=5, validators=[MinValueValidator(1)]
    )

    max_dogeboard_reactions = 100

    def __str__(self):
        return f"Guild Id: {self.guild_id}"

    def reactions_is_valid(self):
        if isinstance(self.dogeboard_reactions_required, int):
            if self.dogeboard_reactions_required in range(
                1, self.max_dogeboard_reactions + 1
            ):
                return True
            else:
                raise ValueError(
                    f"Reactions required must be a positive integer 1 to {self.max_dogeboard_reactions}"
                )
        else:
            raise ValueError("Reactions required must be an integer")

    def save(self, *args, **kwargs):
        if self.reactions_is_valid():
            super(Guild, self).save(*args, **kwargs)
