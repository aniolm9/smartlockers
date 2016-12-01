import MySQLdb

### Connexio DB ###
db = MySQLdb.connect("HOST", "USER", "PASSWORD", "DATABASE")
cur = db.cursor()
######
