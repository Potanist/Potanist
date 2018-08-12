from django.conf.urls import patterns, url
from .views import DashboardView, GrowGuideView, GrowCreateView, \
    GrowDeleteView, GrowDetailsView, GrowUpdateView, HomePageView, MeasurementCreateView, MeasurementListForPlantView, \
    MeasurementUpdateView, PhotoCreateView, PhotoDeleteView, PhotoDetailView, PhotoListView, PhotoUpdateView, LearnMoreView

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='homepage_view'),
    url(r'^guide$', GrowGuideView.as_view(), name="growguide_view"),
    url(r'^learn_more$', LearnMoreView.as_view(), name="learnmore_view"),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard_view'),
    url(r'^dashboard/grow/create/$', GrowCreateView.as_view(), name='creategrow_view'),
    url(r'^dashboard/grow/(?P<pk>[^/]+)/$', GrowDetailsView.as_view(), name='growdetails_view'),
    url(r'^dashboard/grow/update/(?P<pk>[^/]+)/$', GrowUpdateView.as_view(), name='growupdate_view'),
    url(r'^dashboard/grow/delete/(?P<pk>[^/]+)/$', GrowDeleteView.as_view(), name='growdelete_view'),

    # Measurements
    url(r'^dashboard/measurement/create/(?P<grow_id>[^/]+)/(?P<group>[^/]+)$', MeasurementCreateView.as_view(), name='measurementcreateview_group'),
    url(r'^dashboard/measurement/create/(?P<plant_id>[^/]+)$', MeasurementCreateView.as_view(), name='measurementcreateview_plant'),
    url(r'^dashboard/measurement/update/(?P<pk>[^/]+)/$', MeasurementUpdateView.as_view(), name='measurementupdate_view'),
    url(r'^dashboard/measurement/list/plant/(?P<plant_id>[^/]+)/$', MeasurementListForPlantView.as_view(), name='measurementlistforplant_view'),

    # Photos
    url(r'^dashboard/photos/create/plant/(?P<plant_id>[^/]+)$', PhotoCreateView.as_view(), name="photocreateview_plant"),
    url(r'^dashboard/photos/create/grow/(?P<grow_id>[^/]+)$', PhotoCreateView.as_view(), name="photocreateview_grow"),

    url(r'^dashboard/photos/plant/(?P<plant_id>[^/]+)$', PhotoListView.as_view(), name="photolistview_plant"),
    url(r'^dashboard/photos/grow/(?P<grow_id>[^/]+)$', PhotoListView.as_view(), name="photolistview_grow"),

    url(r'^dashboard/photos/delete/(?P<pk>[^/]+)', PhotoDeleteView.as_view(), name="photodelete_view"),
    url(r'^dashboard/photos/update/(?P<pk>[^/]+)', PhotoUpdateView.as_view(), name="photoupdate_view"),
    url(r'^dashboard/photos/(?P<pk>[^/]+)', PhotoDetailView.as_view(), name="photodetail_view"),
)
