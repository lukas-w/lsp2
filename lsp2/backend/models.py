import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PlatformUser(User):

	loginFailureCount = models.SmallIntegerField(blank=True,null=True)

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name )

	class Meta:
		ordering = ('username', )
		verbose_name = "User"
		verbose_name = "Users"


class Category(models.Model):

	name = models.CharField(max_length=64)
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)


class Subcategory(models.Model):

	name = models.CharField(max_length=64)
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)


class Comment(models.Model):
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	file = models.ForeignKey('File', verbose_name=Category._meta.verbose_name)
	date = models.DateTimeField(default=datetime.datetime.now)
	text = models.TextField()


class Rating(models.Model):
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	file = models.ForeignKey('File', verbose_name=Category._meta.verbose_name)
	date = models.DateTimeField(default=datetime.datetime.now)
	stars = models.SmallIntegerField()


class FileType(models.Model):
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)
	extension = models.CharField(max_length=255)


class License(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)


class File(models.Model):
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	filename = models.CharField(max_length=255)
	size = models.SmallIntegerField()
	description = models.TextField()
	license = models.ForeignKey('License', verbose_name=License._meta.verbose_name)
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)
	subcategory = models.ForeignKey('Subcategory', verbose_name=Subcategory._meta.verbose_name)
	insertDate = models.DateTimeField(default=datetime.datetime.now)
	updateDate = models.DateTimeField(default=datetime.datetime.now)
	downloadCount = models.SmallIntegerField()
	sha1hash = models.CharField(max_length=40)
	soundcloudId = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
