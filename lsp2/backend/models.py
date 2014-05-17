import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class PlatformUser(User):
	loginFailureCount = models.PositiveSmallIntegerField(blank=True,null=True)

	def __str__(self):
		if self.first_name or self.last_name:
			return '%s %s' % (self.first_name, self.last_name )
		else:
			return self.username;

	class Meta:
		ordering = ('username', )
		verbose_name = "User"
		verbose_name_plural = "Users"


class Category(models.Model):
	name = models.CharField(max_length=32)
	name_plural = models.CharField(max_length=32)

	def __str__(self):
		return self.name;

	class Meta:
		verbose_name_plural = "Categories"


class Subcategory(models.Model):
	name = models.CharField(max_length=64)
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)

	class Meta:
		verbose_name_plural = "Subcategories"


class Comment(models.Model):
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	submission = models.ForeignKey('Submission', verbose_name=Category._meta.verbose_name)
	date = models.DateTimeField(default=datetime.datetime.now)
	text = models.TextField()


class Vote(models.Model):
	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	submission = models.ForeignKey('Submission')
	date = models.DateTimeField(default=datetime.datetime.now)
	upvote = models.BooleanField(default=True)

	def __str__(self):
		return '%s: %s1' % (self.submission.name, '+' if self.upvote else '-')


class AllowedMime(models.Model):
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)
	mime = models.CharField(max_length=31)


class License(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)


class File(models.Model):
	submission = models.ForeignKey('Submission')
	version = models.PositiveSmallIntegerField()
	size = models.PositiveSmallIntegerField()
	downloadCount = models.PositiveSmallIntegerField()
	sha1hash = models.CharField(max_length=40)
	
	date = models.DateTimeField(default=datetime.datetime.now)


class Submission(models.Model):
	name = models.CharField(max_length=128)
	filename = models.CharField(max_length=128)

	description = models.TextField(blank=True)

	updateDate = models.DateTimeField(default=datetime.datetime.now)

	soundcloudId = models.CharField(max_length=255, blank=True)

	user = models.ForeignKey('PlatformUser', verbose_name=PlatformUser._meta.verbose_name)
	license = models.ForeignKey('License', verbose_name=License._meta.verbose_name, blank=True, null=True)
	category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name)
	subcategory = models.ForeignKey('Subcategory', verbose_name=Subcategory._meta.verbose_name, blank=True, null=True)

	def __str__(self):
		return '%s "%s"' % (self.filename, self.name)

	def downloadCount(self):
		return self.file_set.aggregate(Sum('downloadCount'))['downloadCount__sum']

	def upVotes(self):
		return self.vote_set.filter(upvote = True).count()

	def downVotes(self):
		return self.vote_set.filter(upvote = False).count()

	def voteBalance(self):
		return upVotes - downVotes

