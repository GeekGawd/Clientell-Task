from rest_framework import mixins, generics
from rest_framework.response import Response
import requests
import tablib
from import_export import resources
from django.db.models import Count, Exists, OuterRef
from .models import Account, Opportunity, User
from .serializers import AccountSerializer, OpportunitySerializer, UserSerializer
from .paginations import CustomPagination


# Create your views here.

class HelloWorldAPI(generics.GenericAPIView):

    def get(self, request):
        return Response({"status": "Hello World!"})

class AccessTokenView(generics.GenericAPIView):

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

    def get(self, request):
        
        authorization = request.META.get('HTTP_AUTHORIZATION')
        _, token = authorization.split(' ')
        headers = {'Authorization': f"Bearer {token}"}

        #Import Account
        response = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name From Account', headers=headers).json()
        data = [(i['Id'], i['Name']) for i in response['records']]
        account_resource = resources.modelresource_factory(model=Account)()
        dataset = tablib.Dataset(headers=['id', 'name'])
        for i in data:
            dataset.append(i)
        result = account_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            result = account_resource.import_data(dataset, dry_run=False)
        else:
            return Response({"status": "import failed"})

        #Import User
        response = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name From User', headers=headers).json()
        data = [(i['Id'], i['Name']) for i in response['records']]
        user_resource = resources.modelresource_factory(model=User)()
        dataset = tablib.Dataset(headers=['id', 'name'])
        for i in data:
            dataset.append(i)
        result = user_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            result = user_resource.import_data(dataset, dry_run=False)
        else:
            return Response({"status": "import failed"})

        # #Import Opportunities 
        response = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name, Amount, AccountId, OwnerId From Opportunity', headers=headers).json()
        data = [(i['Id'], i['Name'], i['Amount'], i['AccountId'], i['OwnerId']) for i in response['records']]
        opportunity_resource = resources.modelresource_factory(model=Opportunity)()
        dataset = tablib.Dataset(headers=['id', 'name', 'amount', 'account', 'user'])
        for i in data:
            dataset.append(i)
        result = opportunity_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            result = opportunity_resource.import_data(dataset, dry_run=False)
        else:
            return Response({"status": "import failed"})
        return Response({"status": "imported"})


class OpportunityGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class AccountGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
    queryset = Account.objects.all().annotate(number_of_opportunities=Count('opportunities'))
    serializer_class = AccountSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class UserGetAPI(generics.GenericAPIView, 
                        mixins.ListModelMixin):
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
