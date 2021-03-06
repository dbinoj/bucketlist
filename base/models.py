from __future__ import unicode_literals
from django.db.models import Sum, Value

from flufl.enum import IntEnum
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BudgetType(models.Model):
    """Here user can add type of expense example food, travel,
    accomdation etc"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Dream(models.Model):
    """Create your Own Dream and Go ahead"""
    PUBLIC = 'PUB'
    PRIVATE = 'PRI'
    SHARED = 'SHD'
    CREATED = 'CRD'
    PLANNED = 'PLD'
    PROCESSING = 'PROG'
    POSTPONED = 'POST'
    ACHIEVED = 'ACD'
    DROPPED = 'DRD'
    VISIBILITY_CHOICES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
        (SHARED, 'shared')
    )
    STATUS_CHOICES = (
        (CREATED, 'created'),
        (PLANNED, 'planned'),
        (PROCESSING, 'processing'),
        (POSTPONED, 'postponed'),
        (ACHIEVED, 'achieved'),
        (DROPPED, 'dropped')
    )
    name = models.CharField(max_length=200)
    description = models.CharField(null=True, blank=True, max_length=255)
    visibility = models.CharField(
        max_length=3,
        default='PUB',
        choices=VISIBILITY_CHOICES
    )
    status = models.CharField(
        max_length=4,
        default='CRD',
        choices=STATUS_CHOICES
    )
    created_by = models.ForeignKey(
        User, blank=True, null=True,
        related_name="dreamer", on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def _calculate_total_budget(self):
        """calculates the total budget for a trip from all kind
        of expenses"""
        return Budget.objects.filter(
            dream=self.pk
        ).aggregate(sum=(Sum('amount')))['sum']
    total_budget = property(_calculate_total_budget)

    def __str__(self):
        return self.name


class Budget(models.Model):
    """Expenses for trip"""
    budget_type = models.ForeignKey(BudgetType, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    dream = models.ForeignKey(Dream)

    def __str__(self):
        return '%s %s' % (self.amount, self.dream)
