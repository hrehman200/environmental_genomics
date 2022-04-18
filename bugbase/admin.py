import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Client, Site, Contact, Sample, Bug, Sample_Data, To_Do, TimeLog

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'client')
    
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'site')
    
class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_sampled', 'client', 'contact', 'site', 'note', 'mca_bact', 'mca_arch', 'qpcr', 'gdna', 'barcode', 'seqrun', 'include', 'completed', 'invoiced', 'invoice_no',)
    
    list_filter = ('completed', 'invoiced', 'client', 'contact', 'site',)
    
    fields = (('date_sampled', 'date_submitted'), ('client', 'contact', 'user', 'site'), 'note', ('mca_bact', 'mca_arch', 'barcode'), ('qpcr', 'qpcr_tests'), ('gdna', 'seqrun', 'completed', 'invoiced', 'invoice_no'), 'comments',)
    
    list_editable = ('include', 'gdna', 'barcode', 'seqrun', 'completed', 'invoiced', 'invoice_no')
    
    list_per_page = 25
    
    search_fields = ['note', 'qpcr_tests', 'comments']
    
    actions = ["export_as_csv"]
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
    
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
    
        return response
        
    export_as_csv.short_description = 'Export Selected as CSV'
    
class BugAdmin(admin.ModelAdmin):
    list_display = ('name', 'v1v3', 'v4', 'oxy', 'aob', 'nob', 'nrb', 'sob', 'srb', 'pao', 'gao', 'eps', 'foa', 'fil', 'c1s', 'ch4', 'ace')
    
    fields = (('name', 'lineage'), ('v1v3', 'v4', 'oxy'), ('aob', 'nob', 'nrb'), ('sob', 'srb'), ('pao', 'gao'),       ('eps', 'foa', 'fil'), ('c1s', 'ch4', 'ace'), 'comments', 'references', )
    
    # list_editable = ('oxy', 'aob', 'nob', 'nrb', 'sob', 'srb', 'pao', 'gao', 'eps', 'foa', 'fil', 'c1s', 'ch4', 'ace')
    
    search_fields = ['name']
    list_per_page = 20
    
class SampleDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'sample', 'kingdom', 'phylum', 'klass', 'order', 'family', 'genus', 'counts', 'rel_freq',)
    
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'task', 'completed',)
    list_filter = ('completed',)
    list_editable = ('task', 'completed',)
    
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('task','billed', 'duration' ,'bill_to',)
    list_filter = ('billed', 'bill_to')
    list_editable = ('billed',)
    
# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Bug, BugAdmin)
admin.site.register(Sample_Data, SampleDataAdmin)
admin.site.register(To_Do, ToDoAdmin)
admin.site.register(TimeLog, TimeLogAdmin)