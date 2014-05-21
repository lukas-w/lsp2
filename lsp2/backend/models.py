import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


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
	description = models.TextField(blank=True)

	submitDate = models.DateTimeField(default=datetime.datetime.now)
	updateDate = models.DateTimeField(default=datetime.datetime.now)

	uploader = models.ForeignKey(User)
	license = models.ForeignKey(
		License, verbose_name=License._meta.verbose_name, null=True)

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


class ProjectSubmission(Submission):
	seconds = models.PositiveSmallIntegerField()
	soundcloudId = models.CharField(max_length=255, blank=True)


class SampleSubmission(Submission):
	milliseconds = models.PositiveSmallIntegerField()


class ThemeSubmission(Submission):
	pass
