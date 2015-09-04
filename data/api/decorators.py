from functools import wraps

def field(method):
    @wraps(method)
    def wrapper(obj):
        # If a field cannot be parsed with the specified instructions for
        # whatever reason, return it as None
        try:
            result = method(obj).replace(u'\xa0', ' ').strip()
        except:
            return None
        return result
    w = wrapper
    w.__field__ = True
    return w
