import xml.etree.ElementTree as ET
import re
import pdatab
import colorama

"""
Lookup and check permissions rules
"""

__base_telnos = {
        'ch-fixnet':('+41201234567','+41301234567','+41401234567','+41501234567','+41601234567','+41710123456','+41810123456','+41910123456','+41510123456','+41580123456'),
        'funkruf':('+41740123456',),
        'ch-mobile':('+41760123456','+41770123456','+41780123456','+41790123456','+41754012345'),
        'free':('+41800012345','+41800800800','+41840012345','+41842012345','+41844012345','+41848012345'),
        'voicemail':('+41860760123456','+41860770123456','+41860780123456','+41860790123456','+41860201234567','+41860301234567','+41860401234567','+41860501234567','+41860601234567','+41860710123456','+41860810123456','+41860910123456','+41860754012345'),
        'test':('+41868012345',),
        'vpn':('+41869012345',),
        'vas':('+41878012345','+41900123456','1801','1145','0123'),
        'internal':('+41980123456',),
        'no-match':('+12345678','+123456789','+411234567','+4112345678','+410123456','+41012345'),
        'carrier-preselect':('10701','10801'),
        'rescue':('1414','1415'),
        'emergency':('112','117','118','999','911'),
        'ok-service':('140','143','144','145','147'),
        'nok-service':('012',),
        'internationals':('+919902785000','+914923242436')
        }

__lg1_telnos ={
        'andorra':('+376012345','+376012345678'),
        'austria':('+430123','+4301234','+43012345','+430123456','+4301234567','+43012345678','+430123456789','+4301234567890','+43012345678901','+430123456789012'),
        'belgium':('+320123456','+3201234567','+32012345678'),
        'bt-geoverse':('+88210823288570',),
        'bulgaria':('+3590123','+35901234','+359012345','+3590123456','+35901234567','+359012345678','+3590123456789','+35901234567890','+359012345678901'),
        'canada':('+10800000000','+19059999999','+11290111111','+11390111111','+11860000000','+12041111111','+12261111111','+10900000000','+11290000000','+11390000000','+11860000000','+12260000000','+12490000000','+12500000000','+12890000000','+13060000000','+13430000000','+14030000000','+14160000000','+14180000000','+14380000000','+14500000000','+15060000000','+15140000000','+15190000000','+15790000000','+15810000000','+15870000000','+16000000000','+16040000000','+16130000000','+16470000000','+17050000000','+17090000000','+17780000000','+17800000000','+18070000000','+18190000000','+18670000000','+19020000000'),
        'croatia':('+385100000','+385999999999'),
        'cyprus':('+35701234','+357012345','+3570123456','+35701234567'),
        'czech-rep':('+42001234','+420012345','+4200123456','+42001234567','+420012345678','+4200123456789','+42001234567890','+420012345678901'),
        'denmark':('+4501234567',),
        'dtag':('+88228823288570',),
        'estonia':('+3720123456',),
        'faroe-islands':('+298012345',),
        'finland':('+35801234','+358012345','+3580123456','+35801234567','+358012345678','+3580123456789','+35801234567890'),
        'france':('+33012345678',),
        'germany':('+4901234','+49012345','+490123456','+4901234567','+49012345678','+490123456789','+4901234567890','+49012345678901','+490123456789012'),
        'gibraltar':('+35001234',),
        'greece':('+300123456789',),
        'hungary':('+360123456','+3601234567','+36012345678'),
        'iceland':('+3540123456','+35401234567','+354012345678'),
        'ireland':('+353012345','+3530123456','+35301234567','+353012345678','+3530123456789'),
        'italy':('+39012345','+390123456','+3901234567','+39012345678','+390123456789','+3901234567890'),
        'latvia':('+37101234','+371012345','+3710123456','+37101234567','+371012345678'),
        'liechtenstein':('+4230123456',),
        'lithuania':('+370012345','+3700123456','+37001234567'),
        'luxembourg':('+35201234','+352012345','+3520123456','+35201234567','+352012345678','+3520123456789','+35201234567890'),
        'malta':('+35601234567',),
        'monaco':('+37701234567','+377012345678'),
        'netherlands':('+3101234567','+31012345678','+310123456789'),
        'non-geo-telnor':('+883120823288570',),
        'norway':('+4701234567',),
        'poland':('+48012345','+480123456','+4801234567','+48012345678','+480123456789','+4801234567890','+48012345678901'),
        'portugal':('+351012345','+3510123456','+35101234567','+351012345678'),
        'romania':('+40012345','+400123456','+4001234567','+40012345678','+400123456789'),
        'san-marino':('+3780123456789','+37801234567890','+378012345678901'),
        'slovak-rep':('+42101234567','+421012345678','+4210123456789'),
        'slovenia':('+38601234567',),
        'spain':('+34000000000',),
        'sweden':('+46012345','+460123456','+4601234567','+46012345678','+460123456789','+4601234567890'),
        'usa':('+10123456789','+14089347274'),
        'uk':('+440123456','+4401234567','+44012345678','+440123456789','+4401234567890','+44012345678901','+440123456789012')
        }

__non_usa = {
        'anguila':('+12641111111',),
        'antigua-barbuda':('+12681111111',),
        'bahamas':('+12421111111',),
        'barbados':('+12461111111',),
        'bermuda':('+14411111111',),
        'british-virgin-isles':('+12841111111',),
        'carribean':('+18091111111','+18291111111','+18491111111'),
        'cayman-island':('+13451111111',),
        'domenica':('+17671111111',),
        'grenada':('+14731111111',),
        'guam':('+16711111111',),
        'jamaica':('+18761111111',),
        'mariana-islands':('+16701111111',),
        'monserrat':('+16641111111',),
        'netherlands-antilles':('+17211111111',),
        'puerto-rico':('+17871111111','+19391111111'),
        'st-kitts-and-nevis':('+18691111111',),
        'st-lucia':('+17581111111',),
        'st-vincent-and-grenadines':('+17841111111',),
        'trinidad-and-tobago':('+18681111111',),
        'turks-and-caicos-islands':('+16491111111',),
        'virgin-island':('+13401111111',)
    }

__internationals = {
        'albania':('+3550000000','+355000000000'),
        'algeria':('+21300000000','+213000000000'),
        'armenia':('+37400000000',),
        'argentina':('+547777777','+54222222222222'),
        'belarus':('+375000000000',),
        'belize':('+5017777777',),
        'benin':('+22900000000',),
        'bolivia':('+59188888888',),
        'bosnia-hercegovina':('+3870055555','+38700666666'),
        'brazil':('+550000000000',),
        'burkina-faso':('+22600000000',),
        'chile':('+5688888888','+560000000000'),
        'columbia':('+57666666','+57222222222222'),
        'costa-rica':('+50688888888',),
        'cote-divoire':('+22500000000',),
        'cuba':('+5355555','+5311111111111'),
        'ecuador':('+593999999999',),
        'egypt':('+201111111','+2011111111','+20111111111'),
        'el-salvador':('+50388888888',),
        'falkland-islands':('+500555555',),
        'former-netherlands-antilles':('+599666666','+5997777777','+59997777777'),
        'french-antilles':('+5900000000000',),
        'french-guiana':('+5940000000000',),
        'gambia':('+2200000000',),
        'guatemala':('+5027777777','+50288888888'),
        'guinea':('+224000000',),
        'guyana':('+592666666',),
        'haiti':('+5097777777',),
        'honduras':('+5047777777',),
        'inmarsat-0':('+870000000000','+870100000000','+870300000000','+870390000000','+870500000000','+870600000000','+870600000000','+870700000000','+870800000000'),
        'kosovo':('+37740980000','+377409800000','+37744000000','+377440000000','+37745000000','+377450000000','+38643200000','+38643355555','+38643466666','+38643777777','+38649888888'),
        'libya':('+2180000000','+21800000000','+218000000000','+2180000000000'),
        'macedonia':('+389155555','+389227777777'),
        'mali':('+22300000000',),
        'martinique':('+5960000000000',),
        'mauritania':('+2220000000',),
        'mauritius':('+2300000000',),
        'mexico':('+5288888888','+520000000000'),
        'moldova':('+37300000000',),
        'montenegro':('+3827777777','+38288888888','+382999999999','+3820000000000'),
        'morocco':('+21200000000',),
        'nicaragua':('+50588888888',),
        'niger':('+227000000',),
        'panama':('+5077777777',),
        'paraguay':('+59555555','+59511111111111'),
        'peru':('+5188888888','+51999999999'),
        'sea-coverage':('+3548910399','+35489103990','+354891039900','+393358952','+3933589520','+39335895200','+393358952000','+3933589520000'),
        'senegal':('+2210000000',),
        'serbia-kosovo':('+3817777777','+38188888888','+381999999999','+3810000000000'),
        'south-sudan':('+20111111111','+211000000000'),
        'st-pierre-and-miquelon':('+508666666',),
        'suriname':('+597666666',),
        'togo':('+2280000000',),
        'tunisia':('+21600000000',),
        'ukraine':('+3807777777','+38088888888','+380999999999','+3800000000000','+38011111111111'),
        'uriguay':('+59855555','+5980000000000'),
        'venezuela':('+580000000000',)
    }

__display_separator = "================================================="
        

def print_green(*text):
    colorama.init(autoreset=True)
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + text)
    colorama.deinit()

def print_red(*text):
    colorama.init(autoreset=True)
    print(colorama.Fore.RED + colorama.Style.BRIGHT + ''.join(text))
    colorama.deinit()

def print_white(*text):
    colorama.init(autoreset=True)
    print(colorama.Fore.WHITE + colorama.Style.BRIGHT + ''.join(text))
    colorama.deinit()

def print_yellow(*text):
    colorama.init(autoreset=True)
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + ''.join(text))
    colorama.deinit()

def __compile_regexes(regexes):
        result = []
        for regex in regexes:
                try:
                        result.append(re.compile(regex[0]))
                except:
                        print "ERROR! regex ignored:",regex
        return result

def __print_permissions(perms):
        root = ET.XML(perms)
        count = 0
        for child in root:
                for allowed in child:
                        count = count + 1
                        print_yellow("\t",child.tag,":", allowed.attrib["type"],"(",allowed.attrib["route"],")")
        if count == 0:
                print_yellow("\t","not allowed")
                        
def __match_telno_description(conn, regex):
        regex = str(regex).replace("\\","\\\\")
        query = ["SELECT number_class_id,number_classification,readable_description ",
                 "FROM dialled_number_classifications WHERE regular_exp='",str(regex),"'"]
        return pdatab.query_permissions_db(conn, \
            "SELECT order_id,number_class_id,number_classification,readable_description \
            FROM dialled_number_classifications WHERE regular_exp='%s'" % regex )

def __match_telnos(telnos):
        conn = pdatab.connect_permissions_db()
        creg = __compile_regexes(pdatab.query_permissions_db(conn, "SELECT regular_exp FROM dialled_number_classifications"))
        for t in telnos:
                count = 0
                for c in creg:
                        if(c.match(t)):
                                count = count + 1
                                print t," matched ",c.pattern
                                details = __match_telno_description(conn, c.pattern)
                                if details == ():
                                        print "no details found"
                                else:
                                        print "\t",details[0][0]
                                        print "\t",details[0][1]
                                        print "\t",details[0][2]
                if(count == 1):
                        print "ok"
                else:
                        print "-->NOK: ",t," has ",count," matches"
        pdatab.disconnect_permissions_db(conn)


def show_service_levels():
    """Display a full list of defined service-levels, together with internal service_group_id."""
    levels = pdatab.quick_query("SELECT service_level,service_group_id FROM ucid_service_level_groups ORDER BY service_level")
    for level in levels:
        print "%s (%d)" % (level[0],level[1])
    print "total: ", len(levels)

def show_service_groups():
    """Display a full list of service_group_ids, showing corresponding service levels"""
    conn = pdatab.connect_permissions_db()

    groups = pdatab.query_permissions_db(conn, "SELECT service_group_id,service_group_name FROM service_level_groups ORDER BY service_group_id")

    for group in groups:
        print_white("%2d : %s" % (group[0],group[1]))
        levels = pdatab.query_permissions_db(conn, \
            "SELECT service_level FROM ucid_service_level_groups WHERE service_group_id ='%d' ORDER BY service_level" % group[0])
        for level in levels:
            print "\t%s" % level[0]

    pdatab.disconnect_permissions_db(conn)

def show_service_level_combo(from_level, to_level):
    """
    Display the communication possibilities from one service-level to another.

    from_level -- service-level of the initiator (% wildcard allowed)
    to_level -- service-level the responder (% wildcard allowed)
        
    """
    conn = pdatab.connect_permissions_db()

    olevels = pdatab.query_permissions_db(conn,\
        "SELECT service_level,service_group_id FROM ucid_service_level_groups WHERE service_level LIKE '%s'" % from_level)
    tlevels = pdatab.query_permissions_db(conn,\
        "SELECT service_level,service_group_id FROM ucid_service_level_groups WHERE service_level LIKE '%s'" % to_level)
        
    for olevel in olevels:
        for tlevel in tlevels:
            permid = pdatab.query_permissions_db(conn,\
                "SELECT permissions_id FROM service_group_permissions WHERE orig_group = '%s' AND term_group = '%s'" \
                 % (olevel[1],tlevel[1]))
            print_white("%s (%d) \t=>\t %s (%d) \t: %d" % (olevel[0],olevel[1],tlevel[0],tlevel[1],permid[0][0]))
            __print_permissions(pdatab.query_permissions_db(conn, \
                ("SELECT permissions_xml_stanza FROM permissions WHERE permissions_id='%d'" % permid[0][0]))[0][0])
        
    pdatab.disconnect_permissions_db(conn)
 
                
def match_telno(telno):
    """
    Display the regular expression and classification to which the telephone number matches.

    telnos - exact telephone number(s) to be matched

    """
    __match_telnos((telno,))

def show_dialled_number_combo(from_level, telno):
    """
    Display the communication possibilities from service-level to telephone number.

    from_level -- service-level of the initiator (% wildcard allowed)
    telno -- exact telephone number
        
    """
    conn = pdatab.connect_permissions_db()

    levels = pdatab.query_permissions_db(conn, \
        "SELECT service_level,service_group_id FROM ucid_service_level_groups WHERE service_level LIKE '%s'" % from_level)

    creg = __compile_regexes(pdatab.query_permissions_db(conn, "SELECT regular_exp FROM dialled_number_classifications"))
    for c in creg:
        if(c.match(telno)):
            details = __match_telno_description(conn, c.pattern)
            for level in levels:
                print_white("%s (%d) \t=>\t %s \"%s:%s\" (%d)" % (level[0],level[1],telno,details[0][2],details[0][3],details[0][1]))
                __print_permissions(pdatab.query_permissions_db(conn, \
                    "SELECT permissions_xml_stanza FROM permissions WHERE permissions_id = \
                    (SELECT permissions_id FROM service_group_dialled_number_permissions WHERE orig_group = '%d' AND dialled_number_classification = '%d')" \
                        % (level[1],details[0][1]))[0][0])
    
    print  "total: ", len(levels)
               
    pdatab.disconnect_permissions_db(conn)

def show_base_telno_classifications():
        """Displays basic telephone number classifications."""
        for key in __base_telnos.keys():
                print key

def show_lg1_telno_classifications():
        """Displays LG1 telephone number classifications."""
        for key in __lg1_telnos.keys():
                print key

def show_nonusa_telno_classifications():
        """Displays non-world1 telephone number classifications that masquerade as LG1s."""
        for key in __non_usa.keys():
                print key

def show_international_telno_classifications():
        """Displays international telephone number classifications."""
        for key in __internationals.keys():
                print key

def show_all_telno_classifications():
        """Display all telephone number classifications."""
        show_base_telno_classifications()
        show_lg1_telno_classifications()
        show_nonusa_telno_classifications()
        show_international_telno_classifications()

def test_telno_classification(classification):
        """
        Tests match details for particular classification.

        classification - classification to be matched

        """
        print "'",classification,"' CLASSIFICATION TEST"
        print __display_separator
        if classification in __base_telnos:
                __match_telnos(__base_telnos[classification])
        elif classification in __lg1_telnos:
                __match_telnos(__lg1_telnos[classification])
        elif classification in __non_usa:
                __match_telnos(__non_usa[classification])
        elif classification in __internationals:
                __match_telnos(__internationals[classification])
        else:
                print "ERROR: '",classification,"' classification unknown"
        print

def test_base_telno_classifications():
        """Tests match details for base classifications."""
        for key in __base_telnos.keys():
                test_telno_classification(key)

def test_lg1_telno_classifications():
        """Tests match details for LG1 classifications."""
        for key in __lg1_telnos.keys():
                test_telno_classification(key)

def test_nonusa_telno_classifications():
        """Tests match details for non-USA classifications."""
        for key in __non_usa.keys():
                test_telno_classification(key)

def test_international_telno_classifications():
        """Tests match details for international classifications."""
        for key in __internationals.keys():
                test_telno_classification(key)

def test_all_telno_classifications():
    """Tests match details for all telno classifications."""
    test_base_telno_classifications()
    test_lg1_telno_classifications()
    test_nonusa_telno_classifications()
    test_international_telno_classifications()

def show_available_permissions():
    """Show permissions IDs and their interpretation."""
    conn = pdatab.connect_permissions_db()

    perms = pdatab.query_permissions_db(conn, "SELECT permissions_id,permissions_xml_stanza FROM permissions")

    pdatab.disconnect_permissions_db(conn)

    for pid,pxml in perms:
        print_white("Permission ID = %d" % pid)
        __print_permissions(pxml)

    print 'Total:',len(perms)

def show_dialled_number_classifications():
    """Show number_class_ids and their interpretations"""
    conn = pdatab.connect_permissions_db()

    nids = pdatab.query_permissions_db(conn, "SELECT number_class_id,class_name FROM dialled_number_classes ORDER BY number_class_id")
    print nids
    for nid in nids:
        print_white("%2d - %s" % (nid[0],nid[1]))
        cls = pdatab.query_permissions_db(conn, \
            "SELECT order_id,regular_exp,number_classification,readable_description FROM dialled_number_classifications \
            WHERE number_class_id = '%d' ORDER BY order_id" % (nid[0]))
        for cl in cls:
            print "\t\"%s : %s\"" % (cl[2],cl[3])


    pdatab.disconnect_permissions_db(conn)

def show_service_level_combos_for_permission(permission_id,from_level='%',to_level='%',verbose=False):
    """
    Discover which combinations of service-level have this particular permission.

    permission_id -- numeric ID of permission.
    from_level -- optional service level of originator (including combinations with '%' wildcard)
    to_level -- optional service level of destination (including combinations with '%' wildcard)
    verbose -- optional true will provide readable description of service level.

    """
    conn = pdatab.connect_permissions_db()

    print_white("Service-Level combinations for Permission ID = %d" % (permission_id))

    __print_permissions(pdatab.query_permissions_db(conn, \
        "SELECT permissions_xml_stanza FROM permissions WHERE permissions_id = '%d'" % permission_id)[0][0])

    groupings = pdatab.query_permissions_db(conn, \
        "SELECT orig_group,term_group FROM service_group_permissions WHERE permissions_id = '%d'" % permission_id)
    olevels = pdatab.query_permissions_db(conn, \
        "SELECT service_group_id,service_level,readable_description FROM ucid_service_level_groups WHERE service_level LIKE '%s'" % from_level)
    tlevels = pdatab.query_permissions_db(conn, \
        "SELECT service_group_id,service_level,readable_description FROM ucid_service_level_groups WHERE service_level LIKE '%s'" % to_level)
    
    pdatab.disconnect_permissions_db(conn)

    total = 0

    for o in olevels:
        for t in tlevels:
            for g in groupings:
                if o[0] == g[0] and t[0] == g[1]:
                    total = total + 1
                    print_white("%s (%d) \t=>\t %s (%d)" % (o[1],o[0],t[1],t[0]))
                    if verbose:
                        print "orig:",o[2]
                        print "term:",t[2]

    if total == 0:
        print_red("There are no service-level combinations with permission = %d" % permission_id)
    print 'total:',total

def show_dialled_number_combos_for_permission(permission_id,from_level='%',verbose=False):
    """
    Discover which service-levels can call what dialled number classifications with this permission.

    permission_id -- numeric ID of permission.
    from_level -- optional service level of interest (or combibation with '%' wildcard).
    verbose -- optional true will provide readable description of service level.

    """
    conn = pdatab.connect_permissions_db()

    print "Dialled number combinations for Permission ID = %d" % permission_id

    permres = pdatab.query_permissions_db(conn, \
        "SELECT permissions_xml_stanza FROM permissions WHERE permissions_id = '%d'" % permission_id)
    if len(permres) > 0:
        __print_permissions(permres[0][0])
    else:
        print 'Error: not defined - permission ID =',str(permission_id)
        return

    groups = pdatab.query_permissions_db(conn, \
        "SELECT orig_group,dialled_number_classification FROM service_group_dialled_number_permissions WHERE permissions_id = '%d'" % permission_id)
    
    combos = []
    for group in groups:
        levels =  pdatab.query_permissions_db(conn, \
            "SELECT service_level,readable_description,service_group_id FROM ucid_service_level_groups \
            WHERE service_group_id = '%d' AND service_level LIKE '%s'" % (group[0],from_level))
        combos.extend([level + (group[1],) for level in levels])
 
    pdatab.disconnect_permissions_db(conn)

    total = len(combos)
    if total > 0:
        combos = sorted(combos)
        lastprinted = None
        for combo in combos:
            if not (lastprinted == combo[0]):
                print_white("%s" % (combo[0]))
                if verbose:
                    print combo[1]
                print "\t(%d) => [%d]" % (combo[2],combo[3])
            else:
                print "\t(%d) => [%d]" % (combo[2],combo[3])
            lastprinted = combo[0]
    else:
        print 'There are no dialled number combinations with permission = %d' % permission_id
    print 'total:',total


if __name__ == '__main__':
    test_all_telno_classifications()