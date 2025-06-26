import django_filters

from analytics.models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    min_reviews = django_filters.NumberFilter(field_name='review_count', lookup_expr='gte')

    class Meta:
        model = Product
        fields = "__all__"
