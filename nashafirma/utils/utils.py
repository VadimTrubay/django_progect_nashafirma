from datetime import datetime


class DataMixin:
    def get_menu_context(self, **kwargs):
        current_date = datetime.now().strftime("%d %B %Y")
        context = kwargs
        context["current_date"] = current_date
        return context
