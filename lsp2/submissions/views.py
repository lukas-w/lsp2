from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.models import User

from lsp2.submissions.models import Submission, ProjectSubmission, \
	SampleSubmission, ThemeSubmission


class UserDetail(DetailView):
	model = User
	template_name = 'user_detail.html'
	context_object_name = 's_user'


class SubmissionDetail(DetailView):
	model = Submission

	def get_context_data(self, **kwargs):
		context = super(SubmissionDetail, self).get_context_data(**kwargs)
		context['comment_list'] = context['submission'].comment_set.all()
		return context


class SubmissionList(ListView):
	model = Submission
	context_object_name = 'submission_list'

	paginate_by = 20

	def get_queryset(self):
		cat = self.kwargs['category']

		if cat is None:
			objects = Submission.objects
		if cat == 'projects':
			objects = ProjectSubmission.objects
		elif cat == 'samples':
			objects = SampleSubmission.objects
		elif cat == 'themes':
			objects = ThemeSubmission.objects

		return objects.all()

	def get_template_names(self):
		return 'submissions/submission_list.html'

	def get_context_data(self, **kwargs):
		print(dir(self))
		print(self.kwargs)
		context = super(SubmissionList, self).get_context_data(**kwargs)
		return context


class WelcomeView(TemplateView):
	template_name = "welcome.html"
