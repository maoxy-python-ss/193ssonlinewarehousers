from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# 后台用户表
class Admin(models.Model):
    admin_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    salt = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_admin'

# 文章表
class Chapter(models.Model):
    buddhist = models.ForeignKey('Ghosa', models.DO_NOTHING, blank=True, null=True)
    chapter = models.CharField(max_length=50, blank=True, null=True)
    voice_url = models.CharField(max_length=50, blank=True, null=True)
    memory = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_chapter'


class Counter(models.Model):
    counter_name = models.CharField(max_length=50, blank=True, null=True)
    homework_data = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    homework = models.ForeignKey('Homework', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_counter'

# 修改表
class Ghosa(models.Model):
    album_name = models.CharField(max_length=20, blank=True, null=True)
    albumt_img = models.ImageField(upload_to='pic', default=None,max_length=50, blank=True, null=True)
    grade = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    broadcast = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    issue_data = models.DateTimeField(blank=True, null=True)
    intro = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_ghosa'

# 工作表
class Homework(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    homework_name = models.CharField(max_length=50, blank=True, null=True)
    sort = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_homework'

# 图片路径表
class Image(models.Model):
    img_url = models.ImageField(upload_to='pic', default=None,blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    upload_time = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_image'

# 用户表
class User(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    religious_name = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    head_img = models.ImageField(upload_to='pic', default=None,max_length=50, blank=True, null=True)
    salt = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    register_data = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_user'
