from django.apps import apps

from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel

from .widgets import Autocomplete


def _can_create(page_type):
    """Returns True if the given model has implemented the autocomplete_create
    method to allow new instances to be creates from a single string value.
    """
    return callable(getattr(
        apps.get_model(page_type),
        'autocomplete_create',
        None,
    ))


class AutocompletePanel:
    def __init__(self, field_name, page_type='wagtailcore.Page', is_single=True):
        # is_single defaults to True in order to have easy drop-in
        # compatibility with wagtailadmin.edit_handlers.PageChooserPanel.
        self.field_name = field_name
        self.page_type = page_type
        self.is_single = is_single

    def bind_to_model(self, model):
        can_create = _can_create(self.page_type)
        base = dict(
            model=model,
            field_name=self.field_name,
            widget=type(
                '_Autocomplete',
                (Autocomplete,),
                dict(page_type=self.page_type, can_create=can_create, is_single=self.is_single),
            ),
        )
        return type('_AutocompleteFieldPanel', (BaseFieldPanel,), base)
