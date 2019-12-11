from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponse
from django.urls import resolve, reverse
from django.utils import timezone

from exammode.forms import ExamSessionForm
from userprofile.viewbase import UserProfileView
from course.viewbase import EnrollableViewMixin, CourseInstanceBaseView, CourseInstanceMixin
from authorization.permissions import ACCESS

from lib.viewbase import BaseRedirectView, BaseFormView, BaseView, BaseTemplateView

from .models import ExamSession, ExamAttempt

# Create your views here.


class ExamStartView(BaseTemplateView):
    access_mode = ACCESS.STUDENT
    template_name = "exammode/exam_start.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ExamStartView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['active_exams'] = ExamSession.active_exams.is_active()
        return context


class ExamDetailView(generic.DetailView):
    model = ExamSession

    def post(self, request, *args, **kwargs):
        session = self.get_object()
        redirect_url = session.start_exam(request.user)

        return redirect(redirect_url)


class ExamEndView(BaseTemplateView):
    template_name = "exammode/exam_end.html"
    access_mode = ACCESS.STUDENT

    def post(self, request, *args, **kwargs):
        session = request.user.userprofile.active_exam.exam_taken
        redirect_url = session.end_exam(request.user)

        return redirect(redirect_url)


class ExamFinalView(BaseTemplateView):
    template_name = "exammode/exam_final.html"
    access_mode = ACCESS.STUDENT


class ExamModuleNotDefined(BaseTemplateView):
    template_name = "exammode/exam_module_not_found.html"
    access_mode = ACCESS.STUDENT


class ExamReportView(BaseTemplateView):
    template_name = "exam_report.html"
    access_mode = ACCESS.TEACHER

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ExamReportView, self).get_context_data(**kwargs)
        print(self)
        # Create any data and add it to the context
        context['active_exams'] = ExamSession.active_exams.is_active()
        return context


class ExamSessionEdit(UpdateView):
    template_name = 'exammode/staff/edit_session_form.html'
    form_class = ExamSessionForm
    #fields = ['exam_module', 'can_start', 'duration', 'room']
    model = ExamSession

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_instance'] = self.get_object().course_instance
        return kwargs

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.get_object().course_instance

        self.fields['course_instance'].queryset = CourseInstance.objects.filter(
            id=instance.id)
        self.fields['exam_module'].queryset = CourseModule.objects.filter(
            course_instance=instance)

    '''

    def get_context_data(self, **kwargs):
        context = super(ExamSessionEdit, self).get_context_data(**kwargs)
        context['course_instance'] = self.get_object(
        ).course_instance
        return context

    def get_success_url(self):
        redirect_kwargs = {
            'course_slug': self.kwargs['course_slug'],
            'instance_slug': self.kwargs['instance_slug']
        }
        return reverse('exam-management', kwargs=redirect_kwargs)


class ExamSessionDelete(DeleteView):
    model = ExamSession

    def get_success_url(self):
        redirect_kwargs = {
            'course_slug': self.kwargs['course_slug'],
            'instance_slug': self.kwargs['instance_slug']
        }
        return reverse('exam-management', kwargs=redirect_kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return redirect(url)
        if "confirm" in request.POST:
            return super(ExamSessionDelete, self).post(request, *args, **kwargs)


class ExamManagementView(CourseInstanceMixin, BaseFormView):
    access_mode = ACCESS.TEACHER
    form_class = ExamSessionForm
    template_name = "exammode/staff/exam_management.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_instance'] = self.instance
        return kwargs

    def get_common_objects(self):
        super().get_common_objects()
        self.exam_sessions = list(self.exam_sessions)
        self.note('exam_sessions')

    def get_success_url(self):
        return self.request.path_info

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Changes were saved succesfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Failed to save changes."))
        return super().form_invalid(form)
    '''
    def post(self, request, *args, **kwargs):
        print("posting form now")
        form = ExamSessionForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect(self.request.path_info)
    '''
