import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from model_utils.managers import InheritanceManager

from markupfield.fields import MarkupField


class Profile(models.Model):
	user = models.OneToOneField(User)
	text = MarkupField()


class Comment(models.Model):
	user = models.ForeignKey(User)
	submission = models.ForeignKey('Submission')
	date = models.DateTimeField(default=datetime.datetime.now)
	text = models.TextField()


class Vote(models.Model):
	user = models.ForeignKey(User)
	submission = models.ForeignKey('Submission')
	date = models.DateTimeField(default=datetime.datetime.now, null=True)
	upvote = models.BooleanField(default=True)

	def __str__(self):
		return '%s: %s1' % (self.submission.name, '+' if self.upvote else '-')


class Mime(models.Model):
	mime = models.CharField(max_length=16)


class License(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)


class File(models.Model):
	submission = models.ForeignKey('Submission')
	filename = models.CharField(max_length=128)
	version = models.PositiveSmallIntegerField()
	size = models.PositiveSmallIntegerField()
	downloadCount = models.PositiveSmallIntegerField()
	sha1hash = models.CharField(max_length=40)

	date = models.DateTimeField(default=datetime.datetime.now)


class Submission(models.Model):
	name = models.CharField(max_length=128)
	description = MarkupField(blank=True)

	submitDate = models.DateTimeField(default=datetime.datetime.now)
	updateDate = models.DateTimeField(default=datetime.datetime.now)

	uploader = models.ForeignKey(User)
	license = models.ForeignKey(
		License, verbose_name=License._meta.verbose_name, null=True)

	objects = InheritanceManager()

	class Meta:
		ordering = ["-submitDate"]

	def __str__(self):
		return self.name

	def downloadCount(self):
		return self.file_set.aggregate(Sum('downloadCount'))['downloadCount__sum']

	def upVotes(self):
		return self.vote_set.filter(upvote=True).count()

	def downVotes(self):
		return self.vote_set.filter(upvote=False).count()

	def voteBalance(self):
		return self.upVotes() - self.downVotes()

	def category(self):
		return Submission.objects.get_subclass(id=self.pk)._meta.verbose_name


class ProjectSubmission(Submission):
	seconds = models.PositiveSmallIntegerField(null=True)
	soundcloudId = models.CharField(max_length=255, blank=True)

	class Meta:
		verbose_name = "Project"
		verbose_name_plural = "Projects"


class SampleSubmission(Submission):
	milliseconds = models.PositiveSmallIntegerField(null=True)

	class Meta:
		verbose_name = "Sample"
		verbose_name_plural = "Samples"


class ThemeSubmission(Submission):
	class Meta:
		verbose_name = "Theme"
		verbose_name_plural = "Themes"
