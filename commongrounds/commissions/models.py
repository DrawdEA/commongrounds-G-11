from django.db import models
from django.urls import reverse

# Create your models here.


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'commission type'
        verbose_name_plural = 'commission types'


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    updated_on = models.DateTimeField(null=False, auto_now=True)

    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commissions'
    )

    def __str__(self):
        if self.commission_type:
            return f"{self.title} ({self.commission_type.name})"
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']  # ascending
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'
