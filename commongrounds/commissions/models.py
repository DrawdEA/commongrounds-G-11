from django.db import models
from django.urls import reverse
from accounts.models import Profile

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
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commissions'
    )

    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='created_commissions'
    )

    people_required = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    created_on = models.DateTimeField(null=False, auto_now_add=True)
    updated_on = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'


class Job(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    def __str__(self):
        return f"{self.role} - {self.commission.title}"

    class Meta:
        ordering = ['status', '-manpower_required', 'role']
        verbose_name = 'job'
        verbose_name_plural = 'jobs'


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} - {self.job}"

    class Meta:
        ordering = ['status', '-applied_on']
        verbose_name = 'job application'
        verbose_name_plural = 'job applications'