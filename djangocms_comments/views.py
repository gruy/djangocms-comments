from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from djangocms_comments import settings
from djangocms_comments.forms import UnregisteredCommentForm, CommentForm


def get_form_class(request):
    if request.user.is_anonymous:
        return UnregisteredCommentForm
    else:
        return CommentForm


def get_is_user(request):
    return not request.user.is_anonymous


class SaveComment(FormView):
    comment = None
    template_name = 'djangocms_comments/comment_box.html'

    def get_form_class(self):
        return get_form_class(self.request)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(self.request.POST, request=self.request)
        return form

    def form_valid(self, form):
        self.comment = form.save()
        if settings.EMAIL_NEW_COMMENTS and not self.comment.parent:
            self.email_new_comment()
        return form

    def form_invalid(self, form):
        return form

    def create_new_form(self, old_form):
        initial = {
            'config_id': old_form.cleaned_data['config_id'],
            'page_type': old_form.cleaned_data['page_type'],
            'page_id': old_form.cleaned_data['page_id'],
        }
        return self.get_form_class()(initial=initial, request=self.request)

    def post(self, request, *args, **kwargs):
        form = super(SaveComment, self).post(request, *args, **kwargs)
        if request.GET.get('ajax'):
            return self.render_to_response({
                'form': self.create_new_form(form) if form.is_valid() else form,
                'comment': self.comment,
                'is_user': get_is_user(request),
                'comments_settings': settings,
            })
        referrer = request.META.get('HTTP_REFERER', '')
        return redirect(referrer)

    def email_new_comment(self):
        to = settings.EMAIL_NEW_COMMENTS_ADDRESSES
        subject = settings.EMAIL_NEW_COMMENTS_SUBJECT
        rev = reverse('admin:djangocms_comments_comment_change', kwargs={'object_id': self.comment.id})
        url = f'{self.request.scheme}://{self.request.get_host()}{rev}'

        context = {
            'request': self.request,
            'subject': subject,
            'body': settings.EMAIL_NEW_COMMENTS_BODY,
            'author': self.comment.author,
            'comment': self.comment.body,
            'url': url,
        }

        message = render_to_string('djangocms_comments/email_new_comment.txt', context)
        message_html = render_to_string('djangocms_comments/email_new_comment.html', context)

        email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, to)
        email.attach_alternative(message_html, 'text/html')
        email.send(fail_silently=True)
