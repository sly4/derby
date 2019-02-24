from django.contrib import admin
import logging
import models
from django import forms
from django.template.context_processors import request

# import name_generator

log = logging.getLogger('admin')

# name_generator.load()

class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_first', 'name_last', 'rank', 'pack']
    list_display_links = ['id', 'name_first', 'name_last', 'rank', 'pack']
    list_filter = ('rank','pack',)
    actions = ['set_tiger', 'set_wolf', 'set_bear', 'set_webelos', 'set_aol']

    def rank(self, obj):
        return obj.rank

    def racer_id(self, obj):
        return obj.id
    
    def set_tiger(self, request, queryset):
        queryset.update(rank='Tiger')
    
    def set_wolf(self, request, queryset):
        queryset.update(rank='Wolf')
    
    def set_bear(self, request, queryset):
        queryset.update(rank='Bear')
    
    def set_webelos(self, request, queryset):
        queryset.update(rank='WEBELOS')
        
    def set_aol(self, request, queryset):
        queryset.update(rank='AOL')

class RacerAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(RacerAdminForm, self).clean()
        log.debug('cleaned_data={}'.format(cleaned_data))
        name = cleaned_data.get("name")
        choice = cleaned_data.get("name_choice")

        if (0 == len(name)):
            cleaned_data['name'] = choice

        # Always return the full collection of cleaned data.
        return cleaned_data

    class Meta:
        model = models.Racer
	fields = '__all__'

class RacerAdmin(admin.ModelAdmin):
    form = RacerAdminForm 
    fields = ['id', 'person', 'rank', 'name_choice', 'name', 'picture', 'image_tag_20']
    list_display = ['id', 'person', 'rank', 'name', 'image_tag_20']
    list_display_links = ['id', 'person', 'rank', 'name', 'image_tag_20']
    list_filter = ('person__rank','person__pack',)
    readonly_fields = ('id', 'rank', 'image_tag_20',)

    def rank(self, obj):
        return obj.person.rank

    def save_model(self, request, obj, form, change):
        log.debug('Entered save_model')
        log.debug('form.cleaned_data={}'.format(form.cleaned_data))
#         obj.name = form.cleaned_data['name_ideas'] if obj.name == None else form.cleaned_data['name'] 
        obj.save()

class RacerNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('racers',)
    readonly_fields = ('id',)
    fields = ['name', 'racers']
    list_display = ['id', 'name', 'count', 'stamp']
    list_display_links = ['id', 'name', 'count', 'stamp']

class DerbyEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name', 'event_date']
    readonly_fields = ('id',)

class RaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'derby_event', 'racer_group', 'level', 'lane_ct', 'observer_url']
    readonly_fields = ('id',)
    actions = ['seed_race']
    
    def seed_race(self, request, queryset):
        seed_results = ''
        for current in queryset:
            seed_results += current.seed_race()
        self.message_user(request, seed_results, extra_tags='pre')
            
#     def response_change(self, request, obj):
#         if "_seed-race" in request.POST:
#             matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
#             matching_names_except_this.delete()
#             obj.seed_race()
#             self.message_user(request, "Race has been seeded")
#             return HttpResponseRedirect(".")
#         return super().response_change(request, obj)

class CurrentAdmin(admin.ModelAdmin):
    list_display = ['race', 'run', 'stamp', 'control_url']
    list_display_links = ['race', 'run', 'stamp']
    readonly_fields = ('id', 'stamp')

class RunPlaceAdmin(admin.ModelAdmin):
    list_display = ['run', 'racer_name', 'person', 'lane', 'seconds']
    list_filter = ['run__race', 'racer__person']
    
    def race(self, obj):
        return obj.run.race

    def racer_name(self, obj):
        return obj.racer.name

    def person(self, obj):
        return obj.racer.person

class RunAdmin(admin.ModelAdmin):
    list_display = ['race', 'run_seq', 'run_completed']
    list_filter = ['race']
    actions = ['reset_run']

    def reset_run(self, request, queryset):
        queryset.update(run_completed=False)

    def race(self, obj):
        return obj.race
    
admin.site.register(models.DerbyEvent, DerbyEventAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Racer, RacerAdmin)
admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.Run, RunAdmin)
admin.site.register(models.RunPlace, RunPlaceAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Current, CurrentAdmin)
admin.site.register(models.RacerName, RacerNameAdmin)
admin.site.site_header = 'Pack 57 Race Management'
admin.site.site_title = 'Pack 57 Race Management'
