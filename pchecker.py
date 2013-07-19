import xml.etree.ElementTree as ET
import re
import pdatab

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
        'nok-service':('012',)
        }

__lg1_telnos ={
        'andorra':('+376012345','+376012345678'),
        'austria':('+430123','+4301234','+43012345','+430123456','+4301234567','+43012345678','+430123456789','+4301234567890','+43012345678901','+430123456789012'),
        'belgium':('+320123456','+3201234567','+32012345678'),
        'bulgaria':('+3590123','+35901234','+359012345','+3590123456','+35901234567','+359012345678','+3590123456789','+35901234567890','+359012345678901'),
        'canada':('+10800000000','+19059999999'),
        'croatia':('+385100000','+385999999999'),
        'cyprus':('+35701234','+357012345','+3570123456','+35701234567'),
        'czech-rep':('+42001234','+420012345','+4200123456','+42001234567','+420012345678','+4200123456789','+42001234567890','+420012345678901'),
        'denmark':('+4501234567',),
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
        'norway':('+4701234567',),
        'poland':('+48012345','+480123456','+4801234567','+48012345678','+480123456789','+4801234567890','+48012345678901'),
        'portugal':('+351012345','+3510123456','+35101234567','+351012345678'),
        'romania':('+40012345','+400123456','+4001234567','+40012345678','+400123456789'),
        'san-marino':('+3780123456789','+37801234567890','+378012345678901'),
        'slovak-rep':('+42101234567','+421012345678','+4210123456789'),
        'slovenia':('+38601234567',),
        'sweden':('+46012345','+460123456','+4601234567','+46012345678','+460123456789','+4601234567890'),
        'usa':('+10123456789','+14089347274'),
        'uk':('+440123456','+4401234567','+44012345678','+440123456789','+4401234567890','+44012345678901','+440123456789012')
        }

__display_separator = "================================================="
        


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
                        print "\t",child.tag,":", allowed.attrib["type"],"(",allowed.attrib["route"],")"
        if count == 0:
                print "\t","not allowed"
                        
def __match_telno_description(conn, regex):
        regex = str(regex).replace("\\","\\\\")
        query = ["SELECT number_class_id,number_classification,readable_description ",
                 "FROM dialled_number_classifications WHERE regular_exp='",str(regex),"'"]
        return pdatab.query_permissions_db(conn, "".join(query))

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
        """Display a full list of defined service-levels."""
        levels = pdatab.quick_query("SELECT service_level FROM ucid_service_levels")
        for level in levels:
                print level[0]
        print "total: ", len(levels)

def show_service_level_combo(from_level, to_level):
        """
        Display the communication possibilities from one service-level to another.

        from_level -- service-level of the initiator (% wildcard allowed)
        to_level -- service-level the responder (% wildcard allowed)
        
        """
        conn = pdatab.connect_permissions_db()
        levelquery = ["SELECT orig_level, term_level, permissions_id FROM service_level_permissions ",
                "WHERE orig_level LIKE '",str(from_level),"' AND term_level LIKE '",str(to_level),"'"]
        combos = pdatab.query_permissions_db(conn, "".join(levelquery))
        for orig, term, pid in combos:
                print orig,"=>",term,":",pid
                permquery =["SELECT permissions_xml_stanza FROM permissions WHERE permissions_id='",str(pid),"'"]
                __print_permissions(pdatab.query_permissions_db(conn, "".join(permquery))[0][0])
        print "total: ", len(combos)
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
        creg = __compile_regexes(pdatab.query_permissions_db(conn, "SELECT regular_exp FROM dialled_number_classifications"))
        for c in creg:
                if(c.match(telno)):
                        details = __match_telno_description(conn, c.pattern)
                        query = ["SELECT orig_level,dialled_number_classification,permissions_id ",
                                 "FROM dialled_number_permissions",
                                 " WHERE orig_level LIKE '", str(from_level),
                                 "' AND dialled_number_classification = '",
                                 str(details[0][0]),"'"]
                        perms = pdatab.query_permissions_db(conn, "".join(query))
                        for orig,cid,pid in perms:
                                print orig,"=>",telno,"(",cid,"):",pid
                                permquery =["SELECT permissions_xml_stanza FROM permissions WHERE permissions_id='",str(pid),"'"]
                                __print_permissions(pdatab.query_permissions_db(conn, "".join(permquery))[0][0])
                        print "total: ", len(perms)
        pdatab.disconnect_permissions_db(conn)

def show_base_telno_classifications():
        """Displays basic telephone number classifications."""
        for key in __base_telnos.keys():
                print key

def show_lg1_telno_classifications():
        """Displays LG1 telephone number classifications."""
        for key in __lg1_telnos.keys():
                print key

def show_all_telno_classifications():
        """Display all telephone number classifications."""
        show_base_telno_classifications()
        show_lg1_telno_classifications()

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

def test_all_telno_classifications():
    """Tests match details for all telno classifications"""
    test_base_telno_classifications()
    test_lg1_telno_classifications()
