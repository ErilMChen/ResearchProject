from tastypie.resources import ModelResource
from favourites.models import StopTimesGoogle
from map.models import NameToID

class MyModelResource(ModelResource):
    '''Access this API using ../api/v1/schedule/'''
    class Meta:
        queryset = StopTimesGoogle.objects.all()
        allowed_methods = ['get']
        resource_name = 'schedule'
        excludes = ['id' ]

class BusModelResources(ModelResource):
    '''Access this API using ../api/v1/busmodels/'''
    class Meta:
        queryset = StopTimesGoogle.objects.all()
        allowed_methods = ['get']
        resource_name = 'busmodels'
        excludes = ['id']