import logging

from kensu.client import DataSourcePK, DataSource, SchemaPK, Schema, FieldDef
from kensu.utils.kensu_provider import KensuProvider
from kensu.utils.helpers import eventually_report_in_mem,flatten
from kensu.requests.models import Response

import requests as req

def wrap_get(method):
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)

        kensu = KensuProvider().instance()

        try:
            fields_dict = flatten(result.json())

            # Construct the file location

            url = kwargs['url'] if 'url' in kwargs else args[0]
            try:
                params = kwargs['params'] if 'params' in kwargs else args[1]
            except:
                params = None

            if params is not None:
                location = url + '?' + ('&').join([e+'={}' for e in params.keys()])
            else:
                location = url


            result_pk = DataSourcePK(location=location,
                                     physical_location_ref=kensu.default_physical_location_ref)
            result_ds = DataSource(name=location, format='API',
                                   pk=result_pk)._report()

            fields = [FieldDef(name = k,  field_type=fields_dict[k], nullable=True ) for k in  fields_dict]
            sc_pk = SchemaPK(result_ds.to_ref(),
                             fields=fields)

            result_sc = Schema(name="schema:" + result_ds.name, pk=sc_pk)._report()

            result.__class__ = Response
            result.ksu_schema = result_sc
            result.ds_location = result.url
            try:
                import json
                d = json.loads(result.text)
                count_json = len(d)
                stats = {'count':count_json}

            except:
                stats = None
            kensu.real_schema_df[result_sc.to_guid()] = None
            result.ksu_stats = stats
        except:
            None

        return result

    wrapper.__doc__ = method.__doc__
    return wrapper

get = wrap_get(req.get)