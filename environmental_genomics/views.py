from random import sample
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import csv

from bugbase.models import Sample, Sample_Data


@login_required
def index(request):
    samples = Sample.objects.filter(user=request.user)
    print(samples)
    return render(request, 'samples.html', {'samples': samples})


@login_required
def sample_data(request, sample_id):
    sample_data = Sample_Data.objects.filter(sample_id=sample_id)
    kingdoms = sample_data.values('kingdom').distinct()
    phylums = sample_data.values('phylum').distinct()
    klass = sample_data.values('klass').distinct()
    orders = sample_data.values('order').distinct()
    families = sample_data.values('family').distinct()
    genus = sample_data.values('genus').distinct()

    if request.POST:
        query_kingdom = Q()
        query_phylum = Q()
        query_klass = Q()
        query_order = Q()
        query_family = Q()
        page = request.POST.get('page', 1) 
        q_genus = request.POST.get('genus')
        q_kingdom = request.POST.getlist('kingdom[]')
        q_phylum = request.POST.getlist('phylum[]')
        q_klass = request.POST.getlist('klass[]')
        q_order = request.POST.getlist('order[]')
        q_family = request.POST.getlist('family[]')
        q_rel_freq = request.POST.get('rel_freq')
        q_csv = request.POST.get('csv')

        if(q_genus):
            query &= Q(genus__icontains=q_genus)
        
        # https://stackoverflow.com/questions/32940738/filtering-in-django-by-a-set-of-string
        if(q_kingdom):
            for value in q_kingdom:
                query_kingdom |= Q(kingdom__startswith=value)

        if(q_phylum):
            for value in q_phylum:
                query_phylum |= Q(phylum__startswith=value)

        if(q_klass):
            for value in q_klass:
                query_klass |= Q(klass__startswith=value)

        if(q_order):
            for value in q_order:
                query_order |= Q(order__startswith=value)

        if(q_family):
            for value in q_family:
                query_family |= Q(family__startswith=value)

        sample_data = sample_data.exclude(Q(rel_freq__lte = q_rel_freq)).filter(query_kingdom, query_phylum, query_klass, query_order, query_family)
                
        if q_csv:
            output = []
            response = HttpResponse (content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename=sampledata.csv'
            
            writer = csv.writer(response)
            #Header
            writer.writerow(['kingdom', 'phylum', 'klass', 'order', 'family', 'genus', 'counts', 'rel_freq'])
            for s in sample_data:
                output.append([s.kingdom, s.phylum, s.klass, s.order, s.family, s.genus, s.counts, '{:.2f}'.format(s.rel_freq)])
            #CSV Data
            writer.writerows(output)
            return response
        else:
            paginator = Paginator(sample_data, 100)
            results = list(paginator.page(page).object_list.values('id', 'kingdom', 'phylum', 'klass', 'order', 'family', 'genus', 'counts', 'rel_freq'))
            return JsonResponse({"results":results, 'page_range':list(paginator.page_range), 'page':page})

    return render(request, 'sample-data.html', {
        'fluid': 1,
        'kingdoms': kingdoms,
        'phylums': phylums,
        'klass': klass,
        'orders': orders,
        'families': families,
        'genus': genus,
        'sample_id': sample_id
    })
