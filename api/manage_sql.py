import data as db


def unwrap_sql_relation(cls, attr):
    res = []
    for item in getattr(cls, attr):
        res.append(item.id)
    return res


def set_sql_relation(object, value_class, attr, value_ids):
    array = getattr(object, attr)
    for id in value_ids:
        item = fetch_one_instance(value_class, id)
        array.append(item)


def get_all_instances(cls):
    sql = db.create_session()
    res = []
    for obj in sql.query(cls).all():
        data = get_object_data(obj)
        res.append(data)
    sql.close()
    return res


def get_one_instance(arg):
    sql = db.create_session()
    object = sql.query(cls).get(id)
    sql.close()
    return get_object_data(object)


def get_object_data(obj):
    required_fields = obj.to_dict(only=obj.get_non_related_attrs())
    specific_fields = {rel: unwrap_sql_relation(obj, rel)
                       for rel in obj.get_related_attrs()}
    data = {**required_fields, **specific_fields}  # их сумма
    return data
