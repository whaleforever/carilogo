import sqlite3
import settings

conn = sqlite3.connect(settings.DATABASE)
c = conn.cursor()


def initial(**values):
    table = values.get('table')
    columns = values

    # remove from table
    columns.pop('table', None)
    c.execute("CREATE TABLE %s ( %s ) " % (table, ','.join(["%s %s" % (k, v) for k, v in
                                                             columns.iteritems()])))
    conn.commit()


def insert(table, *values):
    # import pdb; pdb.set_trace()
    data = [str(v) for v in values]
    c.execute("INSERT INTO %s (%s)" %
              (table, ",".join(data)))
    conn.commit()


def query(table, select, where=None):
    if where:
        where = "WHERE %s" % where
    c.execute("SELECT %s FROM %s %s" % (select, table, where))
    return c.fetchall()
