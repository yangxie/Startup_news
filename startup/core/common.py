def get_parameter(request, key, default):
     try:
          return request.GET[key]
     except:
          return default

def get_value_or_none(table, key):
    if (key in table):
        return table[key]
    return None
