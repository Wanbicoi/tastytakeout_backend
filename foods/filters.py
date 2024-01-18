import django_filters
from foods.models import Food


class FoodFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="unaccent__icontains")
    order = django_filters.OrderingFilter(fields=(("rating", "rating"),))
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

    class Meta:
        model = Food
        fields = {"rating": ["lt", "gt"]}
