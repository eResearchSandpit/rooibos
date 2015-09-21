from django.db import connection

def quote_db_name(name):
    """
    make sure a db/table/field name is quoted with backticks
    :param name: a string from a databse, e.g. table_name
    :return: a quoted sting, e.g. `table_name`
    """
    if name.startswith("`") and name.endswith("`"):
        return name  # Quoting once is enough.
    return "`%s`" % name


def col(model, field):
    """
    get a quoted table column from a model/field pair  e.g.  (col(OwnedWrapper, 'object_id')
    :param model: The name of a model being used
    :param field: The name of a model field
    :return: a string in the format Model.Field, e.g.: `util_ownedwrapper`.`object_id`
    """
    return '%s.%s' % (quote_db_name(model._meta.db_table), quote_db_name(model._meta.get_field(field).column))


def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()