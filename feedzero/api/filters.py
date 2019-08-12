from django_filters import rest_framework as filters


class FeedListFilterSet(filters.FilterSet):
    only_watched = filters.BooleanFilter(method="get_only_watched")

    def get_only_watched(self, queryset, name, value):
        """If true only return the feeds watched by the request user."""
        if value:
            return queryset.filter(watched_by=self.request.user)
        return queryset
