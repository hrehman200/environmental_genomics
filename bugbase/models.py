from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.urls import reverse
from django.utils.text import slugify

from random import random

# Create your models here.

class Client(models.Model):
    client = models.CharField('Client', max_length=100, null=False, blank=False)
    
    class Meta:
        ordering = ['client',]
    
    def __str__(self):
        return f'{self.client}'
        
class Site(models.Model):
    site = models.CharField('Site', max_length=100, null=False, blank=False)
    
    class Meta:
        ordering = ['site',]
    
    def __str__(self):
        return f'{self.site}'
        
class Contact(models.Model):
    first_name = models.CharField('First Name', max_length=40, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=40, null=True, blank=True)
    email = models.EmailField('Email Address', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['first_name',]
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
        
class Sample(models.Model):
    date_sampled = models.DateField('Date Sampled', default = timezone.now, blank=True, null=True, help_text='Date sample was collected')
    date_submitted = models.DateField('Date Submitted', default = timezone.now, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField('Site Notes', max_length=100, null=True, blank=True)
    mca_bact = models.BooleanField('Bac', default = False, null=True, blank=True)
    mca_arch = models.BooleanField('Arc', default = False, null=True, blank=True)
    qpcr = models.BooleanField('qPCR', default = False, null=True, blank=True)
    qpcr_tests = models.CharField('qPCR Tests', max_length=60, blank=True, null=True)
    barcode = models.CharField('Barcode', max_length=10, null=True, blank=True)
    seqrun = models.IntegerField(blank=True, null=True)
    # arch_bc = models.CharField('BC-A', max_length=10, null=True, blank=True)
    gdna = models.FloatField('gDNA', default=0.0, blank=True, null=True)
    completed = models.BooleanField(default = False, null=True, blank=True)
    invoiced = models.BooleanField(default = False, null=True, blank=True)
    invoice_no = models.IntegerField(blank=True, null=True)
    comments = MarkdownxField(blank = True)
    include = models.BooleanField('incl', default = False, blank = True, null = True)
    
    def __str__(self):
        return f'{self.id}'
        
class Bug(models.Model):      
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField(max_length=255, null=True)
    lineage = models.CharField(max_length=256, null=True)
    v1v3 = models.IntegerField('v1v3', default=0, help_text = 'Core Microbe')
    v4 = models.IntegerField('v4', default=0, help_text = 'Core Microbe')
    
    oxy_choices = (
        ('a', 'Aero/Resp'),
        ('f', 'Fac. An.'),
        ('o', 'Obl. An.'),
        ('u', 'n.d.')
    )
    
    bug_choices = (
        ('y', 'yes'),
        ('n', 'no'),
        ('v', 'var'),
        ('u', 'n.d.'),
    )
    
    oxy = models.CharField('OXY', max_length = 1, choices = oxy_choices, default = 'u', help_text = 'Aerobic/Anaerobic')
    aob = models.CharField('AOB', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Ammonia Oxidizer')
    nob = models.CharField('NOB', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Nitrite Oxidizer')
    nrb = models.CharField('NRB', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Nitrate Reducer')
    sob = models.CharField('SOB', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Sulfur Oxidizer')
    srb = models.CharField('SRB', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Sulfur Reducer')
    pao = models.CharField('PAO', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Polyphosphate Accumulator')
    gao = models.CharField('GAO', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Glycogen Accumulator')
    eps = models.CharField('EPS', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Extracellular Polysaccharide/Bulking')
    foa = models.CharField('FOA', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Foaming/Hydrophobic')
    fil = models.CharField('FIL', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Filament')
    c1s = models.CharField('C1S', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Methylotroph')
    ch4 = models.CharField('CH4', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Methanogen')
    ace = models.CharField('ACE', max_length = 1, choices = bug_choices, default = 'u', help_text = 'Acetogen')
    comments = MarkdownxField(blank = True)
    references = MarkdownxField(blank = True)
    
    def __str__(self):
        return f'{self.name}'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Bug, self).save(*args, **kwargs)

    @property
    def formatted_comments(self):
        return markdownify(self.comments)

    @property
    def formatted_references(self):
        return markdownify(self.references)
        
class Sample_Data(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.SET_NULL, null = True, blank = True)
    kingdom = models.CharField('kingdom', max_length=256, null = True, blank = True)
    phylum = models.CharField('phylum', max_length=256, null = True, blank = True)
    klass = models.CharField('class', max_length=256, null = True, blank = True)
    order = models.CharField('order', max_length=256, null = True, blank = True)
    family = models.CharField('family', max_length=256, null = True, blank = True)
    genus = models.CharField('genus', max_length=256, null = True, blank = True)
    counts = models.IntegerField(blank = True, null = True)
    rel_freq = models.FloatField(blank = True, null = True)
    
    class Meta:
        verbose_name_plural = 'Sample Data'
        
class To_Do(models.Model):
    task = models.CharField('Task', max_length=256, null = True, blank = True)
    date = models.DateField('Date Added', default = timezone.now, null=True, blank=True)
    notes = MarkdownxField('Notes', blank = True)
    completed = models.BooleanField('Completed', default = False)
    
    class Meta:
        verbose_name_plural = 'To Do'
        
class TimeLog(models.Model):
    start = models.DateTimeField('Start Time', default = timezone.now)
    stop = models.DateTimeField('Stop Time', default = timezone.now)
    task = models.CharField('Task', max_length=256, null = True, blank = True)
    bill_to = models.CharField('Bill To', max_length=32, null = True, blank = True)
    billed = models.BooleanField('Billed', default = False)
    
    def duration(self):
        return self.stop - self.start
        
    class Meta:
        verbose_name_plural = 'Time Log'