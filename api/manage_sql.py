import data as db


def get_related_ids(obj, attr):
    if hasattr(obj, attr):
        return [item.id for item in getattr(obj, attr)]


def get_related_objects(obj, attr):
    if hasattr(obj, attr):
        return list(map(get_object_data, getattr(obj, attr)))


def get_all_instances(cls):
    sql = db.create_session()
    res = []
    for obj in sql.query(cls).all():
        data = get_object_data(obj)
        res.append(data)
    sql.close()
    return res


def get_one_instance(cls, id):
    sql = db.create_session()
    object = sql.query(cls).get(id)
    data = get_object_data(object)
    sql.close()
    return data


def get_object_data(obj):
    non_related_fields = obj.to_dict(only=obj.get_non_related_attrs())
    related_fields = {rel: get_related_ids(obj, rel)
                      for rel in obj.get_related_attrs()}
    data = {**non_related_fields, **related_fields}  # их сумма
    return data
