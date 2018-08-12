from datetime import datetime
from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import CharField, Q, Value
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView,  ListView, TemplateView, UpdateView

from allauth.account.forms import SignupForm
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user

from shared.mixins import PermissionRequiredMixinWithAnonymous

from .forms import MeasurementForm
from .models import Grow, Measurement, Photo, Plant


class HomePageView(TemplateView):
    template_name = 'core/homepage.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard_view')
        return super(HomePageView, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        signup_form = SignupForm()
        context['signup_form'] = signup_form
        return context


class GrowGuideView(TemplateView):
    template_name = 'core/grow_guide.html'


class LearnMoreView(TemplateView):
    template_name = 'core/topics/learn_more.html'


class DashboardView(LoginRequiredMixin, ListView):
    model = Grow
    template_name = 'core/grow_list.html'
    filter_sizes = {'active': 0, 'archived': 0, 'shared': 0}

    def get_queryset(self):
        queryset = super(DashboardView, self).get_queryset()
        user = self.request.user
        active = queryset.filter(Q(owner=user),
                                 Q(end_date=None) | Q(end_date__gt=datetime.today().date())
                                 ).annotate(type=Value('active', output_field=CharField()))
        self.filter_sizes['active'] = len(active)

        archived = queryset.filter(owner=user,
                                   end_date__lte=datetime.today().date()
                                   ).annotate(type=Value('archived', output_field=CharField()))
        self.filter_sizes['archived'] = len(archived)

        shared = get_objects_for_user(user, 'core.view_grow').exclude(owner=user).annotate(type=Value('shared', output_field=CharField()))
        self.filter_sizes['shared'] = len(shared)

        return list(chain(active, archived, shared))

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'active')

        for filter, size in self.filter_sizes.items():
            context[filter+'_size'] = size

        return context


class GrowDetailsView(PermissionRequiredMixinWithAnonymous, DetailView):
    model = Grow
    permission_required = 'view_grow'


class GrowCreateView(CreateView):
    model = Grow
    template_name = "core/generic_form.html"
    fields = ('start_date', 'name', 'description')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        # TODO: These two lines should be in a transaction
        self.object.save()
        assign_perm('view_grow', self.object.owner, self.object)
        assign_perm('change_grow', self.object.owner, self.object)
        assign_perm('delete_grow', self.object.owner, self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        form_class = super(GrowCreateView, self).get_form_class()
        form_class.header = "Create New Grow"
        form_class.required_css_class = 'field-required'
        return form_class

    def get_success_url(self):
        return reverse('growdetails_view', kwargs={'pk': self.object.pk})


class GrowUpdateView(PermissionRequiredMixinWithAnonymous, UpdateView):
    model = Grow
    fields = ('start_date', 'end_date', 'name', 'description')
    permission_required = 'change_grow'

    def get_form_class(self):
        form_class = super(GrowUpdateView, self).get_form_class()
        form_class.header = "Update Grow: %s" % self.object.name
        form_class.required_css_class = 'field-required'
        return form_class

    def get_success_url(self):
        return reverse('growdetails_view', kwargs={'pk': self.object.pk})


class GrowDeleteView(PermissionRequiredMixin, DeleteView):
    model = Grow
    permission_required = 'delete_grow'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '%s was successfully deleted!' % self.object.name)
        return super(GrowDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard_view')


class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'core/generic_form.html'

    def get_form_kwargs(self):
        kwargs = super(MeasurementCreateView, self).get_form_kwargs()

        # Remember this check if based on  self.kwargs, not the form kwargs (which is what we're modifying)
        if 'group' in self.kwargs and 'grow_id' in self.kwargs:
            # This is potentially unsafe as we're filtering right on grow ID and not checking if that grow object exists
            plants = Plant.objects.filter(grow_id=self.kwargs['grow_id'], group=self.kwargs['group'])

        elif 'plant_id' in self.kwargs:
            plants = Plant.objects.filter(id=self.kwargs['plant_id'])

        kwargs.update({'plants': plants})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print self.object.air_temperature
        print form.plants
        for p in form.plants:
            self.object.plant = p
            self.object.save()
            self.object.id = None
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('growdetails_view', kwargs={'pk': self.object.plant.grow_id, })


class MeasurementUpdateView(UpdateView):
    # TODO: Lock this down with permissions
    model = Measurement
    form_class = MeasurementForm
    template_name = 'core/generic_form.html'

    def get_success_url(self):
        return reverse('measurementlistforplant_view', kwargs={'plant_id': self.object.plant_id})


class MeasurementListForPlantView(ListView):
    # TODO: Lock this down with permissions
    model = Measurement

    def get_queryset(self):
        return Measurement.objects.filter(plant_id=self.kwargs['plant_id'])

    def get_context_data(self, **kwargs):
        print self.kwargs
        context = super(MeasurementListForPlantView, self).get_context_data(**kwargs)
        context['plant'] = Plant.objects.get(id=self.kwargs['plant_id'])

        return context


class MeasurementDeleteView(DeleteView):
    model = Measurement

    def delete(self, request, *args, **kwargs):
        return super(MeasurementDeleteView, self).delete(request, *args, **kwargs)


class PhotoCreateView(CreateView):
    model = Photo
    fields = ['img', 'taken_timestamp', 'description']
    template_name = 'core/generic_form.html'

    # TODO: Lock this down with permissions
    def dispatch(self, request, *args, **kwargs):
        self.plant = None
        self.grow = None
        if 'plant_id' in self.kwargs:
            self.plant = Plant.objects.get(id=self.kwargs['plant_id'])
            self.grow = self.plant.grow
        if 'grow_id' in self.kwargs:
            self.grow = Grow.objects.get(id=self.kwargs['grow_id'])
        return super(PhotoCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        form_class = super(PhotoCreateView, self).get_form_class()
        form_class.header = "Upload Photo"
        form_class.required_css_class = 'field-required'
        form_class.info_msg = self.get_form_info_msg()
        return form_class

    def get_form_info_msg(self):
        if self.plant:
            return "The uploaded photo will be attached to plant: <strong>%s</strong>" % self.plant
        if self.grow:
            return "The uploaded photo will be attached to grow: <strong>%s</strong>" % self.grow

    def get_initial(self):
        initial = super(PhotoCreateView, self).get_initial()
        if self.plant and self.grow:
            initial['description'] = "Photo of plant %s from grow %s" % (self.plant, self.grow)
        return initial

    def get_success_url(self):
        if self.object.plant:
            url = reverse('photolistview_plant', kwargs={'plant_id': self.object.plant_id})
        elif self.object.grow:
            url = reverse('photolistview_grow', kwargs={'grow_id': self.object.grow_id})
        return url
    
    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.plant:
            self.object.plant = self.plant
        if self.grow:
            self.object.grow = self.grow

        self.object.save()

        assign_perm('view_photo', self.request.user, self.object)
        assign_perm('change_photo', self.request.user, self.object)
        assign_perm('delete_photo', self.request.user, self.object)
        return super(PhotoCreateView, self).form_valid(form)


class PhotoListView(ListView):
    model = Photo

    # TODO: Check permissions- does the user have view_grow access to the Grow for this photo list?

    def dispatch(self, request, *args, **kwargs):
        self.plant = None
        self.grow = None
        if 'plant_id' in self.kwargs:
            self.plant = Plant.objects.get(id=self.kwargs['plant_id'])
            self.grow = self.plant.grow
        if 'grow_id' in self.kwargs:
            self.grow = Grow.objects.get(id=self.kwargs['grow_id'])
        return super(PhotoListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data()
        if self.plant:
            context['plant_obj'] = self.plant
        if self.grow:
            context['grow_obj'] = self.grow
        return context

    def get_queryset(self):
        if self.plant:
            return Photo.objects.filter(plant=self.plant).order_by('-taken_timestamp')
        if self.grow:
            return Photo.objects.filter(grow=self.grow).order_by('-taken_timestamp')


class PhotoDetailView(DetailView):
    model = Photo
    # TODO: Check permissions- does the user have view_grow access to the Grow for this photo?


class PhotoUpdateView(UpdateView):
    model = Photo
    template_name = 'core/generic_form.html'
    fields = ['taken_timestamp', 'description']

    def get_form_class(self):
        form_class = super(PhotoUpdateView, self).get_form_class()
        form_class.header = "Edit Photo"
        form_class.required_css_class = 'field-required'
        form_class.info_msg = 'Editing photo:<br/><img src="%s" style="width:200px; height:auto;">' % (settings.MEDIA_URL+str(self.object.img))
        return form_class

    def get_success_url(self):
        return reverse('photodetail_view', kwargs={'pk': self.object.id})


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    permission_required = 'delete_photo'

    def delete(self, request, *args, **kwargs):
        response = super(PhotoDeleteView, self).delete(request, *args, **kwargs)
        messages.success(request, 'Photo was successfully deleted!')
        return response

    def get_success_url(self):
        if self.object.plant:
            url = reverse('photolistview_plant', kwargs={'plant_id': self.object.plant_id})
        elif self.object.grow:
            url = reverse('photolistview_grow', kwargs={'grow_id': self.object.grow_id})
        return url