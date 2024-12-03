from django import template
from django.forms import ModelForm
from django.apps import apps

register = template.Library()

@register.simple_tag
def dynamic_form(app_label, model_name, *args):
    """
    Dynamically generate a form for the given model and fields.
    
    Args:
        app_label: The app containing the model.
        model_name: The name of the model.
        args: The fields to include in the form (optional).
    
    Returns:
        A dynamically created ModelForm.
    """
    # Get the model dynamically
    model = apps.get_model(app_label, model_name)

    # Dynamically get the form class for the model from forms.py
    form_class_name = f'{model_name}Form'
    form_class = None
    try:
        # Try to import the form class dynamically from the app's forms.py
        form_class = apps.get_model(app_label, form_class_name)
    except LookupError:
        pass  # Handle case where form doesn't exist

    if form_class is None:
        # If no custom form exists, create a default form using ModelForm
        class DynamicForm(ModelForm):
            class Meta:
                model = apps.get_model(app_label, model_name)
                fields = args or [field.name for field in model._meta.fields]

    return DynamicForm
