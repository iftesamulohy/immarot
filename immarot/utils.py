from django import forms
from django.apps import apps

def get_dynamic_form(model_name, app_name, fields=None):
    """
    Dynamically create a ModelForm for the given model.

    :param model_name: The name of the model class for which the form is to be generated.
    :param app_name: The app name where the model is located.
    :param fields: List of fields to include in the form. Defaults to all fields.
    :return: A dynamically generated ModelForm class.
    """
    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        raise ValueError(f"Model {model_name} not found in app {app_name}.")
    
    class Meta:
        model = apps.get_model(app_name, model_name)
        fields = '__all__'

    form_class = type(
        f"{model.__name__}Form",
        (forms.ModelForm,),
        {"Meta": Meta}
    )

    return form_class
