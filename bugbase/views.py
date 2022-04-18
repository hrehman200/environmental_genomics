from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django_tables2 import SingleTableView
from json import dumps

from .models import Sample
from .tables import SampleListTable

# Create your views here.

class SampleListView(SingleTableView):
    model = Sample
    table_class = SampleListTable
    template_name = 'bugbase/list.html'
    paginate_by = 50
    
    # def get_queryset(self):
    #     return Sample.objects.filter(owner=self.request.user)
    
class SampleDetailView(DetailView):
    model = Sample
    fields = [
        'date_sampled',
        'site',
        'unit',
        'preservation',
        'po',
        'tracking',
        'comments',
    ]
    
def junk(request):
    return render(request, 'bugbase/junk.html')
    
def stupid(request):
    return HttpResponse("Stupid")
    
def send_dictionary(request):
    # create data dictionary
    dataDictionary = {
        'hello': 'World',
        'geeks': 'forgeeks',
        'ABC': 123,
        456: 'abc',
        14000605: 1,
        'list': ['geeks', 4, 'geeks'],
        'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
    }
    # dump data
    dataJSON = dumps(dataDictionary)
    return render(request, 'bugbase/landing.html', {'data': dataJSON})