from django.contrib import admin
from .models import Grow, Plant, PlantStage, Breeder, Strain

@admin.register(Grow)
class GrowAdmin(admin.ModelAdmin):
    pass

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    pass

@admin.register(PlantStage)
class PlantStageAdmin(admin.ModelAdmin):
    pass

@admin.register(Breeder)
class BreederAdmin(admin.ModelAdmin):
    pass

@admin.register(Strain)
class StrainAdmin(admin.ModelAdmin):
    pass
