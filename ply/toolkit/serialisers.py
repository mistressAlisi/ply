"""
toolkit/serialisers.py
====================================
Toolkit utilities for [De]-Serialising Models.
"""
from django.forms import model_to_dict

from ply.toolkit.logger import getLogger
from ply.toolkit import streams
from roleplaying.stats.models import ProfileStatHistory
from roleplaying.exp.models import ProfileExperience

logging = getLogger('toolkit.stats',name='toolkit.stats')

def simple_serialiser(model_instance):
    """
    @brief SERIALISE an object and return a set of json-encodable objects suitable for AJAX/JSON requests.
    ===============================
    :param model_instance: p_model_instance: The Model instance to be serialised
    :returns: r:data, verbose_names,help_text.
    """
    verbose_names = {}
    help_text = {}
    for f in model_instance._meta.get_fields():
        if hasattr(f,'verbose_name'):
            verbose_names[f.name] = f.verbose_name
        if hasattr(f,'help_text'):
            if f.help_text != "":
                help_text[f.name] = f.help_text
    rdata = model_to_dict(model_instance)
    return rdata,verbose_names, help_text

