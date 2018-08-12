from datetime import datetime

from django import template
from django.db.models import Q

from guardian.shortcuts import get_objects_for_user

from core.models import Grow, PlantStage

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_user_grows(context):
    # TODO: For performance, consder checking if the User's grows are already in the context,
    # e.g, like on the dashboard overview
    user = context['request'].user
    if user.is_anonymous():
        return []
    grows = Grow.objects.filter(
        Q(owner=user),
        Q(end_date=None) | Q(end_date__gte=datetime.today().date())
    )
    return grows

@register.assignment_tag(takes_context=True)
def get_shared_grows(context):
    user = context['request'].user
    if user.is_anonymous():
        return []
    return get_objects_for_user(user, 'core.view_grow').exclude(owner=user).order_by('owner')

@register.inclusion_tag('core/_plant_change_stage.html')
def get_plant_stage_change_menu(plant):
    current_stage = plant.get_current_stage()
    other_stages = set(PlantStage.get_stages()) - set([current_stage.stage])
    print "cs",current_stage,", os:",other_stages
    return {'plant': plant, 'current_stage': current_stage, 'other_stages': other_stages}
