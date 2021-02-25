from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from creator.forms import ColumnFormSet
from creator.models import DataSet, Schema


class SchemaListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'schema/list.html'
    model = Schema
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        return Schema.objects.filter(user=user)


class SchemaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    fields = ['name']
    template_name = 'schema/create.html'
    model = Schema

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['column'] = ColumnFormSet(self.request.POST)
        else:
            data['column'] = ColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        data_set = context['column']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            if data_set.is_valid():
                data_set.instance = self.object
                data_set.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('datasets', kwargs={'id': self.object.id})


class SchemaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    template_name = 'schema/datasets.html'
    model = Schema
    context_object_name = 'schema'
    pk_url_kwarg = 'id'
    queryset = Schema.objects.prefetch_related('dataset_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datasets'] = self.object.dataset_set.all()
        return context

    def post(self, request, *args, **kwargs):
        ds = DataSet.objects.create(schema_id=kwargs.get('id'),
                                    rows=self.request.POST.get('rows'))
        print(ds)
        return HttpResponseRedirect(reverse('datasets', kwargs=kwargs))

