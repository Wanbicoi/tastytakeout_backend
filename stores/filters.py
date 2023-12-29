import django_filters
from stores.models import Store


class StoreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_liked = django_filters.BooleanFilter(
        field_name="is_liked",
        method="filter_is_liked",
        label="Current user liked or not (required logged in)",
    )

    def filter_is_liked(self, queryset, name, value):
        request = self.request

        user = request.user if request and hasattr(request, "user") else None

        if user and user.is_authenticated and value:
            return queryset.filter(likers__id=user.id)
        return queryset
