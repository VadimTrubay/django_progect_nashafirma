from datetime import datetime


class DataMixin:
    def get_menu_context(self, **kwargs):
        current_date = datetime.now().strftime("%d %B %Y")
        context = kwargs
        context["current_date"] = current_date
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(
        ',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


class GetContextDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context["is_owner"] = False  # По умолчанию пользователь не является владельцем
        if self.request.user.is_authenticated:
            context["is_owner"] = True
        return context
