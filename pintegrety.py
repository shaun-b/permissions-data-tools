import pdatab
from sets import Set,ImmutableSet
import collections
import colorama

servicelevels = None
servicegroupids = None
permissionsids = None
numberclassids = None

separator = '------------------------------------------------------------------'

def print_green(text):
	print(colorama.Fore.GREEN + colorama.Style.BRIGHT + text)

def print_red(*text):
	print(colorama.Fore.RED + colorama.Style.BRIGHT + ''.join(text))

def print_white(*text):
	print(colorama.Fore.WHITE + colorama.Style.BRIGHT + ''.join(text))

def show_duplicates(l,name):
	"""
	Check for duplicates.

	l -- list containing values to be checked for duplication
	name -- identifier for print output
	return -- False if duplication detected; otherwise True

	"""
	dups = [x for x,y in collections.Counter(l).items() if y > 1]
	if len(dups) > 0:
		print str(name),': duplicate combination(s) found for the following:'
		for d in dups:
			print_red('\t',str(d))
		return False
	return True

def show_omissions(l,s,name):
	"""
	Check for missing combinations.

	l -- list to be checked
	s -- reference set against which contents of l will be compared
	return -- False if omissions found; otherwise True

	"""
	diffs = Set(l).symmetric_difference(s)
	if len(diffs) > 0:
		print str(name),': missing combination(s) found for the following:'
		for d in diffs:
			print_red('\t',str(d))
		return False
	return True

def setup():
	"""
	Creates reference sets of service-levels, permissions ids and number classifications.

	Also checks duplication of values.
	service-levels are read from service_level in ucid_service_levels
	permissions ids are read from permissions_id in permissions
	number classifications are read from number_class_id in dialled_number_classifications

	"""
	print 'Loading reference values and checking omissions and duplications'

	conn = pdatab.connect_permissions_db(ip="localhost", port=3306, db="pcomp_srv")

	levels = pdatab.query_permissions_db(conn, 'SELECT service_level,service_group_id FROM ucid_service_level_groups')
	groups = pdatab.query_permissions_db(conn, 'SELECT service_group_id FROM service_level_groups')
	permids = pdatab.query_permissions_db(conn, 'SELECT permissions_id FROM permissions')
	numids = pdatab.query_permissions_db(conn, 'SELECT number_class_id FROM dialled_number_classifications')

	pdatab.disconnect_permissions_db(conn)

	ok = 0
	groups = [g[0] for g in groups]
	if show_omissions([l[1] for l in levels], groups, 'ucid_service_level_groups'):
		ok = ok + 1
	global servicegroupids
	servicegroupids = ImmutableSet(groups)
	levels = [l[0] for l in levels]
	if show_duplicates(levels,'ucid_service_levels_groups'):
		ok = ok + 1
	global servicelevels
	servicelevels = ImmutableSet(levels)
	pids = [p[0] for p in permids]
	if show_duplicates(pids,'permissions'):
		ok = ok + 1
	global permissionsids
	permissionsids = ImmutableSet(pids)
	# numberclassids will contain duplicates
	global numberclassids
	numberclassids = ImmutableSet(n[0] for n in numids)

	if ok == 3:
		print_green('ok')


def check_undefineds_in_service_group_dialled_number_permissions():
	"""
	Checks for undefined values in service_group_dialled_number_permissions table.

	orig_group only has service_group_ids that are defined in service_level_groups
	dialled_number_classification only has number classifications defined as number_class_id in dialled_number_classifications
	permissions_id only has ids defined as permissions_id in permissions

	Prints 'ok' if everything is defined; otherwise prints undefined values.

	"""
	print 'Checking undefineds in service_group_dialled_number_permissions'

	conn = pdatab.connect_permissions_db()
	res = pdatab.query_permissions_db(conn, 'SELECT orig_group,dialled_number_classification,permissions_id FROM service_group_dialled_number_permissions')
	pdatab.disconnect_permissions_db(conn)

	levels = Set(l[0] for l in res)
	numids = Set(n[1] for n in res)
	permids = Set(p[2] for p in res)

	ok = True
	delta = levels.difference(servicegroupids)
	if len(delta) > 0:
		ok = False
		print 'orig_group contains the following undefined service-levels:'
		for d in delta:
			print_red('\t',str(d))
	delta = numids.difference(numberclassids)
	if len(delta) > 0:
		ok = False
		print 'dialled_number_classification contains the following undefined number classifications:'
		for d in delta:
			print_red('\t',str(d))
	delta = permids.difference(permissionsids)
	if len(delta) > 0:
		ok = False
		print 'permissions contains the following undefined permissions ids:'
		for d in delta:
			print_red('\t',str(d))
	return ok

def check_undefineds_in_service_group_permissions():
	"""
	Checks for undefined values in serviec_level_permissions table.

	orig_level only has service-levels that are defined as service_level in ucid_service_levels
	term_level only has service-levels that are defined as service_level in ucid_service_levels
	permissions_id only has ids defined as permissions_id in permissions

	Prints 'ok' if everything is defined; otherwise prints undefined values.

	"""
	print 'Checking undefineds in service_group_permissions'

	conn = pdatab.connect_permissions_db()
	res = pdatab.query_permissions_db(conn, 'SELECT orig_group,term_group,permissions_id FROM service_group_permissions')
	pdatab.disconnect_permissions_db(conn)

	ogroups = Set(l[0] for l in res)
	tgroups = Set(n[1] for n in res)
	permids = Set(p[2] for p in res)

	ok = 1
	delta = ogroups.difference(servicegroupids)
	if len(delta) > 0:
		ok = 0
		print 'orig_group contains the following undefined service_group_ids:'
		for d in delta:
			print_red('\t',str(d))
	delta = tgroups.difference(servicegroupids)
	if len(delta) > 0:
		ok = 0
		print 'term_group contains the following undefined service_group_ids:'
		for d in delta:
			print_red('\t',str(d))
	delta = permids.difference(permissionsids)
	if len(delta) > 0:
		ok = 0
		print 'permissions_id contains the following undefined permissions ids:'
		for d in delta:
			print_red('\t',str(d))
	return ok

def check_combinations_in_service_group_permissions():
	"""
	Checks combinations of service-levels.

	Checks that there is an unduplicated combination with from one service level to full set of service-levels.

	Prints 'ok' if all combinations are defined; otherwise prints omission and duplication values.

	"""
	print "Checking group combinations in service_group_permissions"

	conn = pdatab.connect_permissions_db()

	ok = 0

	#checking for missing origination groups ids
	oids = pdatab.query_permissions_db(conn, "SELECT DISTINCT orig_group FROM service_group_permissions")
	oids = [o[0] for o in oids]
	if show_omissions(oids, servicegroupids, 'orig_group'):
		ok = ok + 1
	
	#checking each origination group id has a full complement of termination group ids
	for groupid in oids:
		res = pdatab.query_permissions_db(conn, "SELECT term_group FROM service_group_permissions WHERE orig_group = '%d'" % (groupid))
		g = [r[0] for r in res]
		if show_omissions(g,servicegroupids,'term_group') and show_duplicates(g,"term_group for %d" % groupid):
			ok = ok + 1

	pdatab.disconnect_permissions_db(conn)
	if ok == (len(servicegroupids) + 1):
		return True
	else:
		return False

def check_combinations_in_service_group_dialled_number_permissions():
	"""
	Checks combinations of service-level with dialled number classifications.

	Checks that there is an unduplicated combination with from one service level to full set of dialled number classifications.

	Prints 'ok' if all combinations are defined; otherwise prints omission and duplication values.

	"""
	print "Checking group to number classification combinations in service_group_dialled_number_permissions"

	conn = pdatab.connect_permissions_db()

	ok = 0

	#checking for missing origination groups ids
	oids = pdatab.query_permissions_db(conn, "SELECT DISTINCT orig_group FROM service_group_dialled_number_permissions")
	oids = [o[0] for o in oids]
	if show_omissions(oids, servicegroupids, 'orig_group'):
		ok = ok + 1

	#checking each origination group id has a full complement of telephone number classifications
	for oid in oids:
		res = pdatab.query_permissions_db(conn, \
			"SELECT dialled_number_classification FROM service_group_dialled_number_permissions WHERE orig_group = '%d'" % oid)
		l = [r[0] for r in res]
		if show_duplicates(l,oid) and show_omissions(l,numberclassids,oid):
			ok = ok + 1

	pdatab.disconnect_permissions_db(conn)

	if ok == (len(servicegroupids) + 1):
		return True
	else:
		return False


def check_undefineds():
	"""Checks all undefined values."""
	if check_undefineds_in_service_group_dialled_number_permissions() and check_undefineds_in_service_group_permissions():
		print_green('ok')
	else:
		print_red('nok')

def check_combinations():
	"""Checks all combinations for correctness."""
	if check_combinations_in_service_group_permissions() and check_combinations_in_service_group_dialled_number_permissions():
		print_green('ok')
	else:
		print_red('nok')

if __name__ == '__main__':
	colorama.init(autoreset=True)

	print_white('LOADING VALUE SETS:')
	print_white(separator)
	setup()
	print

	print_white('CHECKING FOR UNDEFINED VALUES IN ALL TABLES:')
	print_white(separator)
	check_undefineds()
	print

	print_white('CHECKING FOR COMBINATION CORRECTNESS IN ALL TABLES:')
	print_white(separator)
	check_combinations()
	print

	colorama.deinit()
