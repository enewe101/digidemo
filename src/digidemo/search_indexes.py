import datetime;
from haystack import indexes;
from digidemo.models import *;

class SearchIndex(indexes.SearchIndex, indexes.Indexable):
    text =  indexes.CharField(document=True, use_template=True,model_attr='text')
    title =   indexes.CharField(model_attr='title')
    summary =  indexes.CharField(model_attr='summary')
    creation_date =  indexes.CharField(model_attr='creation_date')

    def get_model(self):
        return Proposal

    def index_queryset(self, using=None):
         """Used when the entire index for model is updated."""
         return self.get_model().objects
    
