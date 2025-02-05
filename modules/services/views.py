from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from modules.services.models import Subscription, Client
from modules.services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
     queryset=Client.objects.all().select_related('user').only('company_name',
                                                               'user__email'))
        )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response