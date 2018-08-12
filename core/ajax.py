import json
import uuid

from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from .models import Breeder, Grow, Measurement, Plant, PlantStage, Strain


@dajaxice_register
def ajax_get_breeders(request):
    breeder_list = []
    breeder_queryset = Breeder.objects.all().values('id', 'name')
    try:
        default = Breeder.objects.get(name="Generic")
        breeder_list.append((str(default.pk), default.name))
        breeder_queryset = breeder_queryset.exclude(id=default.id)
    except Breeder.DoesNotExist:
        pass

    breeder_list.extend([(str(b['id']), b['name']) for b in breeder_queryset])
    return json.dumps(breeder_list)

@dajaxice_register
def ajax_get_strains_of_breeder(request, breeder_id):
    strain_list = [(str(s['id']), s['name']) for s in Strain.objects.filter(breeder_id=breeder_id).values('id', 'name')]
    return json.dumps(strain_list)

@dajaxice_register
def ajax_create_plant(request, form):
    plant_form = deserialize_form(form)
    plant = Plant()

    strain_uuid = uuid.UUID(plant_form['strain_id'])
    try:
        strain = Strain.objects.get(id=strain_uuid)
    except Strain.DoesNotExist:
        # Raise error 500
        raise
    plant.strain = strain

    grow_uuid = uuid.UUID(plant_form['grow_id'])
    try:
        grow = Grow.objects.get(id=grow_uuid)
    except Grow.DoesNotExist:
        # Raise error 500
        raise

    if request.user.has_perm('change_grow', grow):
        plant.grow = grow

        qty = int(plant_form['quantity'])

        # TODO: Name handling, indexing
        name = plant_form['name']
        if not name:
            name = "(None)"
        plant.name = name
        plant.methodology = plant_form['methodology']
        plant.group = plant_form['group'] if plant_form['group'] else Plant.UNGROUPED

        results = []
        for i in xrange(0, qty):
            plant.save()
            # serializes requires an iterator that yields Django model instances, so wrap plant in a list
            results.append(plant)

            plantstage = PlantStage()
            plantstage.plant = plant
            plantstage.stage = plant_form['stage']
            plantstage.save()

            plant.id = None

        return serializers.serialize('json', results, fields=('id', 'grow', 'group', 'name', 'strain', 'get_current_stage'))

@dajaxice_register
def ajax_change_plant_group(request, new_group, **kwargs):
    if not new_group:
        new_group = Plant.UNGROUPED
    new_group = new_group.strip()
    plants = Plant.objects.filter(**kwargs)
    plants.update(group=new_group)
    kwargs.update({'new_group': new_group})
    return json.dumps(kwargs)


@dajaxice_register
def ajax_change_plant_name(request, plant_id, new_name):
    response = {}
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        response['error'] = 'That plant doesn\'t exist.'
    else:
        old_name = plant.name
        plant.name = new_name
        plant.save()
        response['msg'] = 'Plant \'%s\' has been renamed to \'%s\'' % (old_name, plant.name)
    return json.dumps(response)

@dajaxice_register
def ajax_change_plant_stage(request, plant_id, new_stage, **kwargs):
    response = {}
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
       response['error'] = 'That plant doesn\'t exist.'
    else:
        # TODO: Check for permissions
        stages = PlantStage.get_stages()
        if new_stage not in stages:
            response['error'] = 'Invalid stage name.'
        else:
            response['old_stage'] = plant.get_current_stage().stage
            stage = PlantStage(plant=plant, stage=new_stage)
            stage.save()
            response['msg'] = 'Plant %s set to stage %s at %s' % (plant, stage, stage.date)
            response['new_stage'] = stage.stage
            response['plant_pk'] = str(plant.pk)
    return json.dumps(response)

@dajaxice_register
def ajax_set_grow_privacy_level(request, grow_id, privacy_level):
    # TODO: Figure out what to do if the Grow does not exist
    retval = {}
    print privacy_level
    try:
        grow = Grow.objects.get(id=grow_id)
    except Grow.DoesNotExist:
        retval = {'error': 'This grow does not exist (id=%s)' % grow_id}
    else:
        if grow.owner == request.user:
            if grow.set_privacy(privacy_level):
                retval = {'msg': 'Successfully set %s to %s.' % (grow, privacy_level)}
            else:
                retval = {'error': 'There was an error setting the privacy to %s' % privacy_level}
        else:
            retval = {'error': 'You must be the owner of a grow to change it\'s visibility.'}

    return json.dumps(retval)

@dajaxice_register
def ajax_set_user_share_level(request, grow_id, target_user, share_level):
    retval = {'alerts': []}
    try:
        grow = Grow.objects.get(id=grow_id)
    except Grow.DoesNotExist:
        retval['alerts'].append({'type': 'danger', 'msg': 'This grow does not exist (id=%s)' % grow_id})
    else:
        user = User.objects.filter(Q(username=target_user) | Q(email=target_user))
        if not user:
            retval['alerts'].append({'type': 'warning', 'msg': 'No user with username or email %s' % target_user})
        elif len(user) > 1:
            retval['alerts'].append({'type': 'warning', 'msg': 'Multiple users found, please enter a unique username.'})
        else:
            user = user[0]
            if grow.share_with_user(user, share_level):
                if share_level == 'remove':
                    msg = 'Removed share access to %s' % user.username
                else:
                    msg = 'Sucessfully granted %s permissions to %s' % (share_level, user.username)
                retval['alerts'].append({'type': 'success', 'msg': msg})
                retval['data'] = {'user': user.username, 'share_level': share_level}
            else:
                retval['alerts'].append({'type': 'danger', 'msg': 'Could not grant %s permissions to %s' % (share_level, user.username)})

    return json.dumps(retval)


@dajaxice_register
def get_shared_users_for_grow(request, grow_id):
    retval = {'alerts': []}
    try:
        grow = Grow.objects.select_related('owner').get(id=grow_id)
    except Grow.DoesNotExist:
        retval['alerts'].append({'type': 'danger', 'msg': 'This grow does not exist (id=%s)' % grow_id})
    else:
        users_perms = grow.get_shared_users()
        retval['data'] = render_to_string('sharing/includes/_user_share_row.html', context={'user_perms': users_perms})

    return json.dumps(retval)

@dajaxice_register
def ajax_delete_measurement(request, measurement_id, modal_id):
    retval = {'alerts': [], 'modal_id': modal_id, 'measurement_id': measurement_id}
    try:
        measurement = Measurement.objects.select_related('plant').get(id=measurement_id)
    except Measurement.DoesNotExist:
        retval['alerts'].append({'type': 'danger', 'msg': 'This measurement does not exist (id=%s)' % measurement_id})
    else:
        if request.user.has_perm('change_grow', measurement.plant.grow):
            measurement.delete()
            retval['alerts'].append({'type': 'success', 'msg': 'This measurement was successfully deleted!'})
            retval['success'] = True
        else:
            retval['alerts'].append({'type': 'warning', 'msg': 'You do not have permissions to modify this grow.'})

    return json.dumps(retval)

@dajaxice_register
def ajax_delete_plant(request, plant_id, modal_id):
    retval = {'alerts': [], 'modal_id': modal_id, 'plant_id': plant_id}
    try:
        plant = Plant.objects.select_related('grow').get(id=plant_id)
    except Plant.DoesNotExist:
        retval['alerts'].append({'type': 'danger', 'msg': 'This plant does not exist (id=%s)' % plant_id})
    else:
        if request.user.has_perm('change_grow', plant.grow):
            plant.delete()
            retval['alerts'].append({'type': 'success', 'msg': '%s was successfully deleted.' % plant})
            retval['success'] = True
        else:
            retval['alerts'].append({'type': 'warning', 'msg': 'You do not have permissions to modify this grow.'})

    return json.dumps(retval)