from django.apps import apps

def get_all_custom_models():
    """Return the names of all models defined in project apps (not Django built-ins)."""
    custom_models = []
    for model in apps.get_models():
        if model.__module__.startswith("django"):
            continue
        custom_models.append(model.__name__)
    return custom_models
