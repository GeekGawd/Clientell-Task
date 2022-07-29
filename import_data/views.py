from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import tablib
from import_export import resources
from django.db.models import Count, Exists, OuterRef
from .models import Account, Opportunity, User
from .serializers import AccountSerializer, OpportunitySerializer, UserSerializer
from .paginations import CustomPagination
from .tasks import import_user, import_account, import_opportunities, add


# Create your views here.

class HelloWorldAPI(generics.GenericAPIView):
    """The API in root path to check if API is working or not."""
    def get(self, request):
        return Response({"status": "Hello World!"})

class AccessTokenView(generics.GenericAPIView):
    """Obtain the Salesforce Token to use the Import API"""
    def get(self, request):
        payload = {
            'grant_type':'password',
            'client_id': '3MVG9pRzvMkjMb6mzmTGES2xCuzah2ZLsa4mrMhvWAwqvYMA63A.xg5sU7nKw8sLm7CO3y5tA1UrTShBnrJTd',
            'client_secret': '153D2FF33316A59B85083F3F2754CB4C6D5C34CB5957CCCC3F25D6553DFEF6F1',
            'username': 'ruthuparna1998@gmail.com',
            'password': 'clientell123'
        }

        response = requests.post('https://login.salesforce.com/services/oauth2/token', data=payload).json()
        return Response({'acess_token': response['access_token']})


class ImportSalesForceData(generics.GenericAPIView):
    """
    The Import API imports Account, User and Opportunities in the order respectively.

    1) The Logic could have been segrated and made into three different APIs, but the task required one API.

    2)The API takes a lot of time to import, so backgroud processing(with Celery) can also be added to reduce
    API call timing, however due to the time constraint and the task scope I didn't add Celery.
    """
    def get(self, request):
        
        try:
            authorization = request.META.get('HTTP_AUTHORIZATION')
            _, token = authorization.split(' ')
            headers = {'Authorization': f"Bearer {token}"}
        except AttributeError:
            return Response({"status": "Include a Bearer Token from token api"}, status=status.HTTP_401_UNAUTHORIZED)

        
        #Import Account
        import_account.delay(headers)

        # Import User
        import_user.delay(headers)

        # #Import Opportunities 
        import_opportunities.delay(headers)

        return Response({"status": "imported"})


class OpportunityGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
    """A GET API to view all Opportunties"""
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class AccountGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
    """A GET API to view all Accounts + also add 
    an extra field that is the sum of all opportunities
    under that account"""
    queryset = Account.objects.all().annotate(number_of_opportunities=Count('opportunities'))
    serializer_class = AccountSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class UserGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
    """An API to view all Users + 
    also add a boolean field that says 
    whether the user has any opportunity who's amount > 100,000"""
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        opportunity_strictly_greater_than_100000 = Opportunity.objects.filter(
            user = OuterRef('pk'),
            amount__gt = 100000
        )
        return User.objects.all().annotate(opporutinty_gt_100000 = Exists(opportunity_strictly_greater_than_100000))

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# class AddNumberAPI(APIView):

#     def post(self, request):
#         data = request.data
#         a = data.get('first_number')
#         b = data.get('second_number')
#         add.delay(a, b)
#         return Response({"status": "number added"})