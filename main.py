import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def nftcounts(collection_name, template_id):
    url = f"https://wax.api.atomicassets.io/atomicassets/v1/templates/{collection_name}/{template_id}/stats"
    req = requests.get(url)
    result = req.json()
    return result


def accounts(collection_name, schema_name, template_id, page, minimumholding=None):
    url = 'https://atomicassets.ledgerwise.io/atomicassets/v1/accounts'
    params = {"collection_name": collection_name,
              "schema_name": schema_name, "template_id": template_id, "limit": 1000, "page": page}
    req = requests.get(url, params=params)
    result = req.json()
    if minimumholding != None:
        data = filter(lambda holdings: int(
            holdings['assets']) >= minimumholding, result['data'])
        result['data'] = list(data)
    return result


def assets_by_attributes(collection_name, schema_name, page, kwargs):
    url = 'https://wax.api.atomicassets.io/atomicassets/v1/assets'
    data = {}
    for key, value in kwargs.items():
        data[f"template_data.{key}"] = value
    data['collection_name'] = collection_name
    data['schema_name'] = schema_name
    data['page'] = page
    data['limit'] = 1000
    req = requests.get(url, params=data)
    return req.json()


def accounts_by_attributes(collection_name, schema_name, kwargs):
    results = None
    while results is None:
        try:
            result = []
            x = ThreadPoolExecutor(max_workers=5)
            fut = [x.submit(assets_by_attributes, collection_name, schema_name,
                            i, kwargs) for i in range(1, 10)]
            for r in as_completed(fut):
                if len(r.result()['data']) == 0:
                    x.shutdown()
                else:
                    result.append(r.result())
            results = result
        except:
            pass
    return results


def accounts_by_number_of_holdings(collection_name, schema_name, template_id, minimum_holding=1):
    results = None
    while results is None:
        try:
            result = []
            x = ThreadPoolExecutor(max_workers=10)
            fut = [x.submit(accounts, collection_name, schema_name,
                            template_id, i, minimum_holding) for i in range(1, 10)]
            for r in as_completed(fut):
                print(r.result())
                if len(r.result()['data']) == 0:
                    x.shutdown(wait=True)
                else:
                    result.append(r.result())
            results = result
        except:
            pass
    return results


def assets(page, collection_name, schema_name, template_id, numberofdays, **kwargs):
    url = 'https://wax.api.atomicassets.io/atomicassets/v1/assets'
    kwargs['page'] = page
    kwargs['limit'] = 1000
    kwargs['collection_name'] = collection_name
    kwargs['schema_name'] = schema_name
    kwargs['template_id'] = template_id
    req = requests.get(url, params=kwargs)
    res = req.json()
    seconds = int(numberofdays) * 24 * 60 * 60
    result = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
    data = res['data']
    accounts_ = filter(lambda x: int(x['transferred_at_time']) < result.timestamp() * 1000, data)
    account_name = map(lambda data: data['owner'], list(accounts_))
    return (list(dict.fromkeys(account_name)))


def accounts_by_time_of_holdings(collection_name, schema_name, template_id, number_of_days):
    results = None
    while results is None:
        try:
            result = []
            x = ThreadPoolExecutor(max_workers=10)
            fut = [x.submit(assets, i, collection_name, schema_name,
                            template_id, number_of_days) for i in range(1, 35 )]
            for r in as_completed(fut):
                result += r.result()
            results = result
        except:
            pass
    return results
