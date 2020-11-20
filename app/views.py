from django.http import Http404
from django.views.generic import DetailView, TemplateView

from app.models import Wedding, Invitation


class HomeView(TemplateView):
    template_name = 'web/index.html'


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
            raise Http404("Tidak ditemukan undangan pernikahan ini.")

    def get_template_names(self):
        obj = self.get_object()
        queryset = self.get_queryset()
        if obj.template:
            if obj.private:
                try:
                    obj = queryset.get(invitation__code=self.request.GET.get('invite', ''))
                except queryset.model.DoesNotExist:
                    return ['web/invitation_code.html']
            return ['wedding/{}'.format(obj.template)]
        return [self.template_name]

    def get_guest(self):
        try:
            return Invitation.objects.get(wedding=self.get_object(), code=self.request.GET.get('invite'))
        except Exception:
            return None
