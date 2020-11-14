from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from app.models import Wedding


class WeddingView(DetailView):
    context_object_name = 'wedding'
    template = 'wedding/default.html'
    model = Wedding

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            queryset = queryset.filter(publish_status=2, slug=slug)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name})

        return obj

    def get_template_names(self):
        obj = self.get_object()
        if obj.template:
            return ['wedding/{}'.format(obj.template)]
        else:
            return [self.template_name]
