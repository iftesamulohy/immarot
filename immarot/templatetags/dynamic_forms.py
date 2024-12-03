# # from django import forms
# # from django.apps import apps
# # from django import template

# # register = template.Library()

# # @register.simple_tag
# # def get_model_form(app_name, model_name, fields=None):
# #     """
# #     Template tag to dynamically generate a ModelForm.

# #     :param app_name: The name of the app containing the model.
# #     :param model_name: The name of the model class.
# #     :param fields: A comma-separated string of field names or None for all fields.
# #     :return: An unbound form instance.
# #     """
# #     try:
# #         # Fetch the model dynamically
# #         model = apps.get_model(app_name, model_name)
# #     except LookupError:
# #         raise ValueError(f"Model {model_name} not found in app {app_name}.")

# #     # Convert comma-separated fields string into a list of field names if necessary
# #     fields = fields.split(',') if fields else '__all__'
    
# #     # Create a form class dynamically
# #     form_class = type(
# #         f"{model.__name__}Form",  # Name of the form class
# #         (forms.ModelForm,),     # Base class
# #         {
# #             'Meta': type(
# #                 'Meta',  # Name of the Meta class
# #                 (),
# #                 {'model': model, 'fields': fields}  # Attributes for Meta
# #             )
# #         }
# #     )

# #     return form_class()


# from django import forms
# from django.apps import apps
# from django import template

# register = template.Library()

# @register.simple_tag
# def get_model_form(app_name, model_name, fields=None):
#     """
#     Template tag to dynamically generate a ModelForm with Bootstrap styling.

#     :param app_name: The name of the app containing the model.
#     :param model_name: The name of the model class.
#     :param fields: A comma-separated string of field names or None for all fields.
#     :return: An unbound form instance with 'form-control' class added to all fields.
#     """
#     try:
#         # Fetch the model dynamically
#         model = apps.get_model(app_name, model_name)
#     except LookupError:
#         raise ValueError(f"Model {model_name} not found in app {app_name}.")

#     # Convert comma-separated fields string into a list of field names if necessary
#     fields = fields.split(',') if fields else '__all__'

#     # Define the form class dynamically
#     form_class = type(
#         f"{model.__name__}Form",  # Name of the form class
#         (forms.ModelForm,),      # Base class
#         {
#             'Meta': type(
#                 'Meta',  # Name of the Meta class
#                 (),
#                 {'model': model, 'fields': fields}  # Attributes for Meta
#             ),
#             '__init__': init_with_form_control  # Attach a custom __init__ method
#         }
#     )

#     return form_class()


# def init_with_form_control(self, *args, **kwargs):
#     """
#     Custom __init__ method to add 'form-control' class to all fields' widgets.
#     """
#     super(self.__class__, self).__init__(*args, **kwargs)
#     for field in self.fields.values():
#         if not isinstance(field.widget, forms.CheckboxInput):  # Skip checkboxes
#             field.widget.attrs.update({'class': 'form-control'})




from django import forms
from django.apps import apps
from django import template

register = template.Library()

@register.simple_tag
def get_model_form(app_name, model_name, fields=None, instance=None):
    """
    Template tag to dynamically generate a ModelForm with Bootstrap styling.

    :param app_name: The name of the app containing the model.
    :param model_name: The name of the model class.
    :param fields: A comma-separated string of field names or None for all fields.
    :param instance: The model instance for editing an existing object (optional).
    :return: An unbound form instance with 'form-control' class added to all fields.
    """
    try:
        # Fetch the model dynamically
        model = apps.get_model(app_name, model_name)
    except LookupError:
        raise ValueError(f"Model {model_name} not found in app {app_name}.")

    # Convert comma-separated fields string into a list of field names if necessary
    fields = fields.split(',') if fields else '__all__'

    # Define the form class dynamically
    form_class = type(
        f"{model.__name__}Form",  # Name of the form class
        (forms.ModelForm,),      # Base class
        {
            'Meta': type(
                'Meta',  # Name of the Meta class
                (),
                {'model': model, 'fields': fields}  # Attributes for Meta
            ),
            '__init__': init_with_form_control  # Attach a custom __init__ method
        }
    )

    # Return the form instance, passing 'instance' if provided (for edit mode)
    return form_class(instance=instance)

def init_with_form_control(self, *args, **kwargs):
    """
    Custom __init__ method to add 'form-control' class to all fields' widgets.
    """
    super(self.__class__, self).__init__(*args, **kwargs)
    for field in self.fields.values():
        if not isinstance(field.widget, forms.CheckboxInput):  # Skip checkboxes
            field.widget.attrs.update({'class': 'form-control'})
