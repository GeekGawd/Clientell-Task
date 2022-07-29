from celery import shared_task
import requests
import tablib
from import_export import resources
from .models import Account, User, Opportunity

@shared_task(bind=True)
def add(self, a, b):
    return a + b

# @shared_task(bind=True)
# def print_hello_world(self):
#     return "hello world"

@shared_task(bind=True)
def import_account(self, headers):
    query = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name From Account', headers=headers).json()
    data = [(i['Id'], i['Name']) for i in query['records']]
    account_resource = resources.modelresource_factory(model=Account)()
    dataset = tablib.Dataset(headers=['id', 'name'])
    for i in data:
        dataset.append(i)
    result = account_resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        result = account_resource.import_data(dataset, dry_run=False)
        return "Import Accounts Successfully"
    else:
        return "Import Accounts failed"

@shared_task(bind=True)
def import_user(self, headers):
    query = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name From User', headers=headers).json()
    data = [(i['Id'], i['Name']) for i in query['records']]
    user_resource = resources.modelresource_factory(model=User)()
    dataset = tablib.Dataset(headers=['id', 'name'])
    for i in data:
        dataset.append(i)
    result = user_resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        result = user_resource.import_data(dataset, dry_run=False)
        return "Import Users Successfully"
    else:
        return "Import Users failed"

@shared_task(bind=True)
def import_opportunities(self, headers):
    query = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query/?q=SELECT Id, Name, Amount, AccountId, OwnerId From Opportunity', headers=headers).json()
    data = [(i['Id'], i['Name'], i['Amount'], i['AccountId'], i['OwnerId']) for i in query['records']]
    opportunity_resource = resources.modelresource_factory(model=Opportunity)()
    dataset = tablib.Dataset(headers=['id', 'name', 'amount', 'account', 'user'])
    for i in data:
        dataset.append(i)
    result = opportunity_resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        result = opportunity_resource.import_data(dataset, dry_run=False)
        return "Import Opportunities Successfully"
    else:
        return "Import Opportunities failed"
