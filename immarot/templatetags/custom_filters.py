from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """
    Adds the CSS class to a form field.
    """
    return value.as_widget(attrs={'class': arg})

@register.filter
def getattr(obj, field_name):
    """
    Safely retrieves the value of a model field by its name.
    Handles related fields, properties, callables, and avoids recursion.
    """
    try:
        # Ensure the field exists on the object
        if hasattr(obj, field_name):
            value = getattr(obj, field_name)

            # Avoid recursion: If the value references itself or repeats, return safely
            if value == obj:
                return "Recursion Detected"

            # If the value is callable, call it safely
            if callable(value):
                try:
                    return value()
                except Exception:
                    return "Error: Cannot evaluate callable"

            # Return the value if all checks pass
            return value

        # Handle missing fields gracefully
        return "Field Not Found"
    except RecursionError:
        return "Recursion Detected"
    except Exception as e:
        return f"Error: {str(e)}"
@register.filter
def get(dictionary, key):
    """Retrieve a value from a dictionary by key."""
    return dictionary.get(key, "N/A")
@register.filter
def getattr(obj, field_name):
    """
    Safely retrieves the value of a model field by its name.
    Handles related fields, properties, callables, and avoids recursion.
    """
    try:
        if hasattr(obj, field_name):
            value = getattr(obj, field_name)

            if callable(value):
                try:
                    return value()
                except Exception:
                    return "Error: Cannot evaluate callable"

            return value

        return "Field Not Found"
    except RecursionError:
        return "Recursion Detected"
    except Exception as e:
        return f"Error: {str(e)}"

@register.filter
def get_field(instance, field_name):
    """
    Retrieves the value of a field from the instance.
    """
    try:
        return getattr(instance, field_name, None)  # Use the `getattr` function to safely access the field
    except Exception as e:
        return None

@register.filter
def add_attrs(field, attrs):
    """
    Adds HTML attributes to a Django form field.
    Accepts attributes in the format: 'key1=value1,key2=value2'.
    """
    attrs_dict = {}
    for attr in attrs.split(','):
        if '=' in attr:
            key, value = attr.split('=')
            attrs_dict[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs_dict)
@register.filter
def format_field(value):
    """Converts `field_name` to `Field Name`."""
    return value.replace("_", " ").capitalize()
