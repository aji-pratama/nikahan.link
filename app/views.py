from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from app.models import Wedding, Invitation


class WeddingView(DetailView):
    model = Wedding
    context_object_name = 'wedding'
    template = 'wedding/default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guest'] = self.get_guest()
        return context

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get(publish_status=2, slug=self.kwargs.get(self.slug_url_kwarg))
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name})

    def get_template_names(self):
        obj = self.get_object()
        queryset = self.get_queryset()
        if obj.template:
            if obj.private:
                try:
                    obj = queryset.get(invitation__code=self.request.GET.get('invite'))
                except queryset.model.DoesNotExist:
                    return ['web/invitation_code.html']
            return ['wedding/{}'.format(obj.template)]
        return [self.template_name]

    def get_guest(self):
        try:
            return Invitation.objects.get(wedding=self.get_object(), code=self.request.GET.get('invite'))
        except Exception:
            return None
