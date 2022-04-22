import json
import datetime
from json import JSONEncoder


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


async def dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs, cls=DateTimeEncoder)
