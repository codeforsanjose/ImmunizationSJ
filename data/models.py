from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone


class Dataset(models.Model):
    GRADE_CHOICES = (
        ('CC', _('Child Care')),
        ('KG', _('Kindergarten')),
        ('7', _('7th Grade')),
    )

    year = models.IntegerField()
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    uid = models.CharField(max_length=20)
    queued_date = models.DateField(default=timezone.now)
    sourced = models.BooleanField(default=False)

    def __unicode__(self):
        return u'<Dataset for {grade} in {year}>'.format(
            grade=self.get_grade_display(),
            year=self.year
        )


class FieldsMap(models.Model):
    dataset = models.OneToOneField(Dataset, related_name='fields_map')

    # School/Facility Information
    code = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    public = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)

    # Immunization Record Information
    reported = models.CharField(max_length=255, blank=True)
    enrollment = models.CharField(max_length=255, blank=True)
    up_to_date = models.CharField(max_length=255, blank=True)
    conditional = models.CharField(max_length=255, blank=True)
    pme = models.CharField(max_length=255, blank=True)
    pbe = models.CharField(max_length=255, blank=True)
    dtp = models.CharField(max_length=255, blank=True)
    polio = models.CharField(max_length=255, blank=True)
    mmr = models.CharField(max_length=255, blank=True)
    hib = models.CharField(max_length=255, blank=True)
    hepb = models.CharField(max_length=255, blank=True)
    vari = models.CharField(max_length=255, blank=True)
