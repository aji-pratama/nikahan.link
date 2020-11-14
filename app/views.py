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
        context['guest'] = Invitation.objects.get(wedding=self.get_object(), key=self.request.GET.get('invt'))
        return context

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get()
            if obj.private:
                return queryset.get(
                    publish_status=2,
                    slug=self.kwargs.get(self.slug_url_kwarg),
                    invitation__key=self.request.GET.get('invt')
                )
            return obj
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name})

    def get_template_names(self):
        obj = self.get_object()
        if obj.template:
            return ['wedding/{}'.format(obj.template)]
        else:
            return [self.template_name]
