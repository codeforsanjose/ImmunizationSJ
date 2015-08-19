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


class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class City(Sector):
    # Add additional information
    pass


class County(Sector):
    # Add additional information
    pass


class District(Sector):
    # Add additional information
    pass


class School(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=255)
    public = models.BooleanField()

    # Sectors
    city = models.ForeignKey(City, related_name='schools')
    county = models.ForeignKey(County, related_name='schools')
    district = models.ForeignKey(District, blank=True, null=True,
                                 related_name='schools')

    # Add school geolocation information


# Temporary model to hold sourced data
class Record(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='records')
    school = models.ForeignKey(School, related_name='records')
    reported = models.BooleanField()
    enrollment = models.IntegerField(blank=True, null=True)
    up_to_date = models.IntegerField(blank=True, null=True)
    conditional = models.IntegerField(blank=True, null=True)
    pme = models.IntegerField(blank=True, null=True)
    pbe = models.IntegerField(blank=True, null=True)
    dtp = models.IntegerField(blank=True, null=True)
    polio = models.IntegerField(blank=True, null=True)
    mmr = models.IntegerField(blank=True, null=True)
    hib = models.IntegerField(blank=True, null=True)
    hepb = models.IntegerField(blank=True, null=True)
    vari = models.IntegerField(blank=True, null=True)


class Summary(models.Model):
    SUMMARY_TYPES = (
        ('ALL', _('All')),
        ('PRI', _('Private')),
        ('PUB', _('Public')),
    )

    dataset = models.ForeignKey(Dataset)
    sector = models.ForeignKey(Sector, related_name='summaries')
    summary_type = models.CharField(max_length=3, choices=SUMMARY_TYPES)
    summary = models.TextField(blank=True)
