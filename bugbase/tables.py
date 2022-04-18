import django_tables2 as tables
from .models import Sample
from django_tables2.utils import A

class SampleListTable(tables.Table):
    id = tables.LinkColumn('sample-detail', args=[A('id')])
    class Meta:
        model = Sample
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id','site', 'unit', 'date_sampled',)
