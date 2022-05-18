import json
import datetime
from json import JSONEncoder


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def dumps(obj, **kwargs):
    """
    Serialize ``obj`` to a JSON formatted ``str``.
    主要解决datetime类型的序列化问题
    """
    return json.dumps(obj, **kwargs, cls=DateTimeEncoder)
