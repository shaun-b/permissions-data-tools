import pdatab
from sets import Set,ImmutableSet
import collections
import colorama

conn_old = None
conn_new = None

separator = '------------------------------------------------------------------'

def print_green(text):
	print(colorama.Fore.GREEN + colorama.Style.BRIGHT + text)

def print_red(*text):
	print(colorama.Fore.RED + colorama.Style.BRIGHT + ''.join(text))

def print_white(*text):
	print(colorama.Fore.WHITE + colorama.Style.BRIGHT + ''.join(text))

def setup():
	"""
	Connects to old and new databases.

	Consistency checks.

	"""
	global conn_old
	conn_old = pdatab.connect_permissions_db(ip="localhost", port=3306, db="pcomp_srv_sb")
	global conn_new
	conn_new = pdatab.connect_permissions_db(ip="localhost", port=3306, db="pcomp_srv")

def destroy():
	pdatab.disconnect_permissions_db(conn_old)
	pdatab.disconnect_permissions_db(conn_new)

def check_servicelevels():
	print_white("checking ucid_service_levels to ucid_service_level_groups consistency")
	print_white(separator)
	print

	levels_old = sorted(pdatab.query_permissions_db(conn_old, 'SELECT service_level FROM ucid_service_levels'))
	levels_new = sorted(pdatab.query_permissions_db(conn_new, 'SELECT service_level FROM ucid_service_levels'))
	groups_new = pdatab.query_permissions_db(conn_new, 'SELECT service_level,service_group_id FROM ucid_service_level_groups')

	print_white("checking level and group totals")
	ok = True
	if not (len(levels_old) == len(levels_new) and len(levels_old) == len(groups_new)):
		ok = False
		print_red("levels and groupings are inconsistent")
	if ok:
		print_green("ok")
	else:
		print_red("nok")

	print_white("checking old levels present as new levels")
	ok = True
	groups = sorted(g[0] for g in groups_new)
	levels = sorted(l[0] for l in levels_old)
	for i in range(len(levels_old)):
		if not (levels_old[i] == levels_new[i]):
			ok = False
			print_red(str(levels_old[i]) + " old vs new " + str(levels_new[i]))
		if not (levels[i] == groups[i]):
			ok = False
			print_red(str(levels[i]) + " old vs new " + str(groups[i]))
	if ok:
		print_green("ok")
	else:
		print_red("nok")

def check_diallednumber_classifications():
	print_white("checking dialled_number_classifications consistency")
	print_white(separator)
	print

	dnc_old = sorted(pdatab.query_permissions_db(conn_old, 'SELECT * FROM dialled_number_classifications ORDER BY order_id'))
	dnc_new = sorted(pdatab.query_permissions_db(conn_new, 'SELECT * FROM dialled_number_classifications ORDER BY order_id'))

	print_white("checking identical")
	ok = True
	for i in range(len(dnc_old)):
		if not (dnc_old[i] == dnc_new[i]):
			ok = False
			print_red(str(dnc_old[i]) + " old vs new " + str(dnc_new[i]))
	if ok:
		print_green("ok")
	else:
		print_red("nok")

def check_servicelevel_permissions():
	print_white("checking service_level_permissions to service_group_permissions consistency")
	print_white(separator)
	print

	levels_old = pdatab.query_permissions_db(conn_old, 'SELECT * FROM service_level_permissions')
	
	print_white("checking new groups consistent with old levels")
	ok = True
	for l in levels_old:
		id = pdatab.query_permissions_db(conn_new, "SELECT permissions_id FROM service_group_permissions WHERE orig_group = \
			(SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[0] + "') AND term_group = \
			(SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[1] + "')")
		if not (l[2] == id[0][0]):
			ok = False
			group0 = pdatab.query_permissions_db(conn_new, "SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[0] + "'")
			group1 = pdatab.query_permissions_db(conn_new, "SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[1] + "'")
			print ("%s (group %d) vs %s (group %d) should be %d and not %d" % (l[0], group0[0][0], l[1], group1[0][0], l[2], id[0][0]))

	if ok:
		print_green("ok")
	else:
		print_red("nok")

	print_white("checking new copy of levels consistent with old levels")
	ok = True
	total = pdatab.query_permissions_db(conn_new, 'SELECT COUNT(*) FROM service_level_permissions')
	if not len(levels_old) == total[0][0]:
		ok = False
		print ("levels mismatch: old len %d new len %d" % (len(levels_old),total[0][0]))

	for l in levels_old:
		id =  pdatab.query_permissions_db(conn_new, "SELECT permissions_id FROM service_level_permissions WHERE orig_level = '" 
			+ l[0] + "' AND term_level = '" + l[1] + "'")
		if not (l[2] == id[0][0]):
			ok = False
			print ("%s vs %s -> %d not %d" % (l[0], l[1], l[2], id[0][0]))

	if ok:
		print_green("ok")
	else:
		print_red("nok")

def check_diallednumber_permissions():
	print_white("checking service_level_permissions to service_group_permissions consistency")
	print_white(separator)
	print

	print_white("checking new groups consistent with old levels")
	ok = True
	levels_old = pdatab.query_permissions_db(conn_old, 'SELECT * FROM dialled_number_permissions')

	for l in levels_old:
		#print l[2]
		id = pdatab.query_permissions_db(conn_new, "SELECT permissions_id FROM service_group_dialled_number_permissions WHERE \
			orig_group = (SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[0] + "') AND \
			dialled_number_classification = '" + str(l[1]) + "'")
		#print id[0][0]
		if not (l[2] == id[0][0]):
			ok = False
			group = pdatab.query_permissions_db(conn_new, "SELECT service_group_id FROM ucid_service_level_groups WHERE service_level = '" + l[0] + "'")
			print ("%s (group %d) vs dial class %d should be %d and not %d" % (l[0], group[0][0], l[1], l[2], id[0][0]))

	if ok:
		print_green("ok")
	else:
		print_red("nok")

	print_white("checking new copy of levels consistent with old levels")
	ok = True
	total = pdatab.query_permissions_db(conn_new, 'SELECT COUNT(*) FROM dialled_number_permissions')
	if not len(levels_old) == total[0][0]:
		ok = False
		print ("service mismatch: old len %d new len %d" % (len(levels_old),total[0][0]))

	for l in levels_old:
		id =  pdatab.query_permissions_db(conn_new, "SELECT permissions_id FROM dialled_number_permissions WHERE orig_level = '" 
			+ l[0] + "' AND dialled_number_classification = '" + str(l[1]) + "'")
		if not (l[2] == id[0][0]):
			ok = False
			print ("%s vs %s -> %d not %d" % (l[0], l[1], l[2], id[0][0]))

	if ok:
		print_green("ok")
	else:
		print_red("nok")


def check_permissions():
	print_white("checking permissions consistency")
	print_white(separator)
	print

	perms_old = pdatab.query_permissions_db(conn_old, 'SELECT * FROM permissions ORDER BY permissions_id')
	perms_new = pdatab.query_permissions_db(conn_new, 'SELECT * FROM permissions ORDER BY permissions_id')

	print_white("checking totals between old and new permissions")
	ok = True

	if not (len(perms_old) == len(perms_new)):
		ok = False
		print ("permissions mismatch: old len %d new len %d" % (len(perms_old), len(perms_new)))

	if ok:
		print_green("ok")
	else:
		print_red("nok")

	print_white("checking new with old permissions")
	ok = True
	for i in range(len(perms_old)):
		if not (perms_old[i] == perms_new[i]):
			ok = False
			print perms_old[i]
			print perms_new[i]
			print

	if ok:
		print_green("ok")
	else:
		print_red("nok")



if __name__ == '__main__':
	colorama.init(autoreset=True)

	setup()
	
	check_servicelevels()
	print
	check_diallednumber_classifications()
	print
	check_servicelevel_permissions()
	print
	check_diallednumber_permissions()
	print 
	check_permissions()

	destroy()

	colorama.deinit()
