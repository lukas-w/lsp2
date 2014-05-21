from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.models import User

from lsp2.backend.models import Submission


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


class WelcomeView(TemplateView):
	template_name = "welcome.html"
