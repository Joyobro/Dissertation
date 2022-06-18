# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from uuid import uuid4

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    orgid = models.ForeignKey('Organisation', models.DO_NOTHING, db_column='orgid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    type = models.CharField(max_length=45, blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    manufacturer = models.CharField(max_length=45, blank=True, null=True)
    note1 = models.CharField(max_length=45, blank=True, null=True)
    note2 = models.CharField(max_length=45, blank=True, null=True)
    orgid = models.ForeignKey('Organisation', models.DO_NOTHING, db_column='orgid', blank=True, null=True)
    assignedname = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Organisation(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    account = models.CharField(max_length=45, blank=True, null=True)
    taxcode = models.CharField(max_length=45, blank=True, null=True)
    note1 = models.CharField(max_length=100, blank=True, null=True)
    note2 = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organisation'


class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    firstname = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    contactno = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    orgid = models.ForeignKey(Organisation, models.DO_NOTHING, db_column='orgid', blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    famcontact = models.CharField(max_length=45, blank=True, null=True)
    registime = models.DateTimeField(blank=True, null=True)
    devicesetup = models.CharField(max_length=200, blank=True, null=True)
    deviceid = models.ForeignKey(Device, models.DO_NOTHING, db_column='deviceid', blank=True, null=True)
    postcode = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class Sensordata(models.Model):
    id = models.CharField(primary_key=True, max_length=45,default=uuid4)
    deviceid = models.CharField(max_length=45, blank=True, null=True)
    profileid = models.CharField(max_length=45, blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    step = models.IntegerField(blank=True, null=True)
    battery = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lg = models.FloatField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    batterystatus = models.IntegerField(blank=True, null=True)
    accelerometer = models.TextField(blank=True,null=True)
    light = models.TextField(blank=True,null=True)
    stress = models.FloatField(blank=True,null=True)
    bloodpressure = models.TextField(blank=True,null=True)
    ppg = models.TextField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'sensordata'
