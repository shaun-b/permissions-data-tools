import MySQLdb

def connect_permissions_db(ip="localhost", port=3306, db="pcomp_srv_sb", u="root", p="FUgi&2013"):
	"""
	Connect to the Permissions Service Database.

	ip -- address of MYSQL DB (default: localhost)
	port -- port of MYSQL DB (default: 3306)
	db -- database name (default: pcomp_srv_sb)
	u -- username (default: root)
	p -- password (default: FUgi&2013)
	return -- database connection

	"""
	conn = MySQLdb.connect(host=ip, port=port, user=u, passwd=p, db=db)
	return conn

def disconnect_permissions_db(conn):
	"""
	Disconnect from the Permissions Service Database.

	conn -- connection obtained from connect_permissions_db()

	"""
	conn.close()

def query_permissions_db(conn, sql):
	"""
	Query Permissions Service Database.

	conn -- connection obtained from connect_permissions_db()
	sql -- SQL query
	return result tuple

	"""
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def quick_query(sql):
	"""
	Quick query of Permissions Service Database.

	connect_permissions_db() - query_permissions_db() - disconnect_permissions_db encapsulated all in one.
	sql -- SQL query
	return result tuple

	"""
        c = connect_permissions_db()
        cursor = c.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        disconnect_permissions_db(c)
        return results       
