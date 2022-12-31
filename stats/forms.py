from django import forms
from stats.models import ProfileStat
class AssignStatForm(forms.Form):

    def __init__(self,*args,**kwargs):
        profile = kwargs.pop('profile')
        community = kwargs.pop('community')
        exp = kwargs.pop('exp')
        super(AssignStatForm,self).__init__(*args,**kwargs)
        stats = []
        stats.append(('-1','Select Stat!'))
        #try:
        ss = ProfileStat.objects.filter(profile=profile,community=community)
        for s in ss:
            stats.append((s.uuid,f'[{s.stat.name}]->|{s.value}/{s.stat.maximum}|'))
        # Workaround to allow installation on blank databases:
        #except:
        #    pass
        self.fields["stat"].choices=stats
        self.fields["increase"] = forms.IntegerField(label='Increase by:',initial=1,min_value=1,max_value=exp.statpoints)

    stat = forms.ChoiceField(label='Select Stat',choices=[])
    increase = forms.IntegerField(label='Increase by:',initial=1,min_value=1)


