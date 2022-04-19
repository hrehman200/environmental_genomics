from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.contrib.auth.decorators import login_required

from bugbase.models import Sample, Sample_Data


@login_required
def index(request):
    samples = Sample.objects.filter(user=request.user)
    return render(request, 'samples.html', {'samples': samples})


@login_required
def sample_data(request, sample_id):
    sample_data = Sample_Data.objects.filter(sample_id=sample_id)
    kingdoms = Sample_Data.objects.order_by().values('kingdom').distinct()
    phylums = Sample_Data.objects.order_by().values('phylum').distinct()
    klass = Sample_Data.objects.order_by().values('klass').distinct()
    orders = Sample_Data.objects.order_by().values('order').distinct()
    families = Sample_Data.objects.order_by().values('family').distinct()
    genus = Sample_Data.objects.order_by().values('genus').distinct()
    return render(request, 'sample-data.html', {
        'sample_data': sample_data,
        'kingdoms': kingdoms,
        'phylums': phylums,
        'klass': klass,
        'orders': orders,
        'families': families,
        'genus': genus,
    })
