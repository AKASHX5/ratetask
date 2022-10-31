from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Ports(models.Model):
    code = models.CharField(primary_key=True,max_length=100,blank=True)
    name = models.TextField(blank=True)
    parent_slug = models.ForeignKey('Regions', models.DO_NOTHING, db_column='parent_slug',blank=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'ports'


class Prices(models.Model):
    orig_code = models.ForeignKey(Ports, models.DO_NOTHING, db_column='orig_code', related_name='orig_code', blank=True)
    dest_code = models.ForeignKey(Ports, models.DO_NOTHING, db_column='dest_code', related_name='dest_code', blank=True)
    day = models.DateField(primary_key=True,blank=True)
    price = models.IntegerField(blank=True)


    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'prices'


class Regions(models.Model):
    slug = models.CharField(max_length=100,blank=True)
    name = models.TextField(primary_key=True,blank=True)
    parent_slug = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_slug', blank=True)

    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'regions'


