import sqlparser


# init a oracle sql parser
parser = sqlparser.Parser(vendor=1)
sql = "select * from test_table"
r, e = parser.check_syntax(sql)
if r != 0:
    print('parse error: %s' % e)
else:
    print('parse ok!')
