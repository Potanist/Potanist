from datetime import datetime
import uuid

from django.conf import settings
from django.db import models

from guardian.shortcuts import assign_perm, get_perms, get_users_with_perms, remove_perm
from guardian.utils import get_anonymous_user

from shared.utils import choices_zip, PreventCapFirst


class Grow(models.Model):
    PRIVACY_PUBLISHED = 'published'
    PRIVACY_HIDDEN = 'hidden'
    PRIVACY_PRIVATE = 'private'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(blank=True, null=True, help_text="To mark a grow as complete, specify an end date.")
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_grow', 'View grow'),
        )
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def get_plants_groupedby_groups(self):
        groups_to_plants = {}
        for plant in self.plant_set.all():
            if plant.group in groups_to_plants:
                groups_to_plants[plant.group].append(plant)
            else:
                groups_to_plants[plant.group] = [plant]

        return groups_to_plants

    def completed(self):
        return self.end_date <= datetime.today().date() if self.end_date else False

    def set_privacy(self, privacy_level):
        # TODO: Check for results of the assign_perm and remove_perm calls
        anon = get_anonymous_user()
        retval = True
        if privacy_level == Grow.PRIVACY_PUBLISHED:
            self.published = True
            assign_perm('view_grow', anon, self)
        elif privacy_level == Grow.PRIVACY_HIDDEN:
            self.published = False
            print self.published
            assign_perm('view_grow', anon, self)
        elif privacy_level == Grow.PRIVACY_PRIVATE:
            self.published = False
            remove_perm('view_grow', anon, self)
        else:
            retval = False
        self.save()
        return retval

    def get_privacy(self):
        self.refresh_from_db()
        anon = get_anonymous_user()
        if anon.has_perm('view_grow', self):
            if self.published:
                return Grow.PRIVACY_PUBLISHED
            else:
                return Grow.PRIVACY_HIDDEN
        else:
            return Grow.PRIVACY_PRIVATE

    def share_with_user(self, user, share_level):
        retval = True
        if share_level == 'view':
            assign_perm('view_grow', user, self)
            remove_perm('change_grow', user, self)
        elif share_level == 'edit':
            assign_perm('view_grow', user, self)
            assign_perm('change_grow', user, self)
        elif share_level == 'remove':
            remove_perm('view_grow', user, self)
            remove_perm('change_grow', user, self)
        else:
            retval = False
        return retval

    def get_shared_users(self, with_owner=False, with_anonymous=False, with_groups=False):
        # Do not use attach_perms, because we want to be able to filter on the queryset
        users = get_users_with_perms(self, with_group_users=with_groups)
        users_perms = {}
        if not with_owner:
            users = users.exclude(id=self.owner_id)
        if not with_anonymous:
            users = users.exclude(id=settings.ANONYMOUS_USER_ID)
        print users.query

        # Once the users are loaded, we can get the perms for each. This is how get_users_with_perms
        # would work anyway with attach_perms=True.
        # https://github.com/django-guardian/django-guardian/blob/b2171c428dbb573a55450f624cfc0f86007ac277/guardian/shortcuts.py#L167
        for user in users:
            users_perms[user] = sorted(get_perms(user, self))
        return users_perms


class Plant(models.Model):
    METHODOLOGY_SOIL = 'Soil'
    METHODOLOGY_HYDROPONICS = 'Hydroponics'

    UNGROUPED = "Ungrouped"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    strain = models.ForeignKey('Strain')
    grow = models.ForeignKey(Grow)
    group = models.CharField(max_length=35, default=UNGROUPED)
    methodology = models.CharField(choices=choices_zip([METHODOLOGY_SOIL, METHODOLOGY_HYDROPONICS]),
                                   max_length=12)

    def __str__(self):
        return self.name

    def get_current_stage(self):
        return self.plantstage_set.latest('date')

    def get_last_measurement(self):
        return self.measurement_set.latest('timestamp')


class PlantStage(models.Model):
    STAGE_SEED = "Seed"
    STAGE_SEEDLING = "Seedling"
    STAGE_VEGETATIVE = "Vegetative"
    STAGE_FLOWERING = "Flowering"
    STAGE_FLUSH = "Flush"
    STAGE_DRYING = "Drying"
    STAGE_CURING = "Curing"
    STAGE_DEAD = "Dead"

    STAGES = (
        (STAGE_SEED, STAGE_SEED),
        (STAGE_SEEDLING, STAGE_SEEDLING),
        (STAGE_VEGETATIVE, STAGE_VEGETATIVE),
        (STAGE_FLOWERING, STAGE_FLOWERING),
        (STAGE_FLUSH, STAGE_FLUSH),
        (STAGE_CURING, STAGE_CURING),
        (STAGE_DRYING, STAGE_DRYING),
        (STAGE_DEAD, STAGE_DEAD),
    )
   
    @classmethod 
    def get_stages(cls):
        return [s[0] for s in cls.STAGES]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plant = models.ForeignKey('Plant')
    stage = models.CharField(choices=choices_zip([STAGE_SEED, STAGE_SEEDLING, STAGE_VEGETATIVE, STAGE_FLOWERING,
                                                  STAGE_FLUSH, STAGE_DRYING, STAGE_CURING]),
                             max_length=12)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stage


class Breeder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Strain(models.Model):
    TYPE_SATIVA = "Sativa"
    TYPE_INDICA = "Indica"
    TYPE_RUDERALIS = "Ruderalis"
    TYPE_HYBRID = "Hybrid"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_type = models.CharField(choices=choices_zip([TYPE_SATIVA, TYPE_INDICA,TYPE_HYBRID,TYPE_RUDERALIS]),
                                   max_length=10)
    flowering_time = models.IntegerField()
    breeder = models.ForeignKey(Breeder)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.breeder.name + "::" + self.name


class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    air_temperature = models.FloatField(null=True, blank=True)
    medium_temperature = models.FloatField(verbose_name="Reservoir / Soil Temperature", null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    co2 = models.FloatField(null=True, blank=True)
    tds_ec = models.IntegerField(verbose_name="TDS/EC", null=True, blank=True)
    ph = models.FloatField(verbose_name=PreventCapFirst("pH"), null=True, blank=True)
    plant = models.ForeignKey(Plant)
    notes = models.TextField(blank=True)


class Photo(models.Model):
    class Meta:
        permissions = (
            # Default permissions include 'add', 'change', and 'delete'
            ('view_photo', 'View photo'),
        )
    img = models.ImageField(verbose_name="Image")
    plant = models.ForeignKey(Plant, null=True)
    grow = models.ForeignKey(Grow, null=True)
    taken_timestamp = models.DateTimeField(verbose_name="Taken At", default=datetime.now)
    description = models.TextField(blank=True)
