from django import forms
from core.plyscript.models import Script
class NewScriptForm(forms.Form):
    scripts = []
    scripts.append(('-1','Create New Script...'))
    try:
        ss = Script.objects.filter()
        for s in ss:
            scripts.append((s.uuid,f'[{s.function_name}]: {s.name}'))
    # Workaround to allow installation on blank databases:
    except Exception as e:
        print("Script save Exception on forms:")
        print(e)
        pass

    load_script = forms.ChoiceField(label='New Script...',choices=scripts)



class SaveScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['function_name','name','descr','body']
        widgets = {
                   'body': forms.HiddenInput()
                   }
