from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

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
    return render(request, 'sample-data.html', {
        'fluid': 1,
        'sample_data': sample_data,
        'kingdoms': kingdoms,
        'phylums': phylums,
        'klass': klass,
        'orders': orders,
        'families': families,
        'genus': genus,
    })
