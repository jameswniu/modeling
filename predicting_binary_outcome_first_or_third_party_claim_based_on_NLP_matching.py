#! /usr/bin/env python3
import os, sys
import re

from copy import deepcopy

#----
# fn matching similar words such as first/last names and street addresses
#----
def similar(a, b):
    if a in b or b in a:
        return 1
    else:
        c = 0
        for i in re.findall('\d+', a):
            for j in re.findall('\d+', b):
                if i == j:
                    c += 1

        for i in re.findall(r'\b[A-Za-z]+\b', a):
            for j in re.findall(r'\b[A-Za-z]+\b', b):
                if i in j or j in i:
                    #print(i, j)

                    c += 1

        threshold = 0.7    ## SPECIFY confidence level

        if c > threshold * len(a.split(' ')) or c > threshold * len(b.split(' ')):
            return 1
        else:
            return 0


suffix = [
    'STATE',
    'ALLEY',
    'ALLEE',
    'ALY',
    'ALLY',
    'ANEX',
    'ANX',
    'ANNEX',
    'ANNX',
    'ARCADE',
    'ARC',
    'AVENUE',
    'AV',
    'AVE',
    'AVEN',
    'AVENU',
    'AVN',
    'AVNUE',
    'BAYOU',
    'BAYOO',
    'BYU',
    'BEACH',
    'BCH',
    'BEND',
    'BND',
    'BLUFF',
    'BLF',
    'BLUF',
    'BLUFFS',
    'BLFS',
    'BOTTOM',
    'BOT',
    'BTM',
    'BOTTM',
    'BOULEVARD',
    'BLVD',
    'BOUL',
    'BOULV',
    'BRANCH',
    'BR',
    'BRNCH',
    'BRIDGE',
    'BRDGE',
    'BRG',
    'BROOK',
    'BRK',
    'BROOKS',
    'BRKS',
    'BURG',
    'BG',
    'BURGS',
    'BGS',
    'BYPASS',
    'BYP',
    'BYPA',
    'BYPAS',
    'BYPS',
    'CAMP',
    'CP',
    'CMP',
    'CANYON ',
    'CANYN',
    'CYN',
    'CANYON',
    'CNYN',
    'CAPE ',
    'CAPE',
    'CPE',
    'CAUSEWAY',
    'CSWY',
    'CAUSWA',
    'CENTER',
    'CEN',
    'CTR',
    'CENT',
    'CENTR',
    'CENTRE',
    'CNTER',
    'CNTR',
    'CENTERS',
    'CTRS',
    'CIRCLE',
    'CIR',
    'CIRC',
    'CIRCL',
    'CRCL',
    'CRCLE',
    'CIRCLES',
    'CIRS',
    'CLIFF',
    'CLF',
    'CLIFFS',
    'CLFS',
    'CLUB',
    'CLB',
    'COMMON',
    'CMN',
    'COMMONS',
    'CMNS',
    'CORNER',
    'COR',
    'CORNERS',
    'CORS',
    'COURSE',
    'CRSE',
    'COURT',
    'CT',
    'COURTS',
    'CTS',
    'COVE',
    'CV',
    'COVES',
    'CVS',
    'CREEK',
    'CRK',
    'CRESCENT',
    'CRES',
    'CRSENT',
    'CRSNT',
    'CREST',
    'CRST',
    'CROSSING',
    'XING',
    'CRSSNG',
    'CROSSROAD',
    'XRD',
    'CROSSROADS',
    'XRDS',
    'CURVE',
    'CURV',
    'DALE',
    'DL',
    'DAM',
    'DM',
    'DIVIDE',
    'DIV',
    'DV',
    'DVD',
    'DRIVE',
    'DR',
    'DRIV',
    'DRV',
    'DRIVES',
    'DRS',
    'ESTATE',
    'EST',
    'ESTATES',
    'ESTS',
    'EXPRESSWAY',
    'EXP',
    'EXPY',
    'EXPR',
    'EXPRESS',
    'EXPW',
    'EXTENSION',
    'EXT',
    'EXTN',
    'EXTNSN',
    'EXTENSIONS',
    'EXTS',
    'FALL',
    'FALLS',
    'FLS',
    'FERRY',
    'FRY',
    'FRRY',
    'FIELD',
    'FLD',
    'FIELDS',
    'FLDS',
    'FLAT',
    'FLT',
    'FLATS',
    'FLTS',
    'FORD',
    'FRD',
    'FORDS',
    'FRDS',
    'FOREST',
    'FRST',
    'FORESTS',
    'FORGE',
    'FORG',
    'FRG',
    'FORGES',
    'FRGS',
    'FORK',
    'FRK',
    'FORKS',
    'FRKS',
    'FORT',
    'FT',
    'FRT',
    'FREEWAY',
    'FWY',
    'FREEWY',
    'FRWAY',
    'FRWY',
    'GARDEN',
    'GDN',
    'GARDN',
    'GRDEN',
    'GRDN',
    'GARDENS',
    'GDNS',
    'GRDNS',
    'GATEWAY',
    'GTWY',
    'GATEWY',
    'GATWAY',
    'GTWAY',
    'GLEN',
    'GLN',
    'GLENS',
    'GLNS',
    'GREEN',
    'GRN',
    'GREENS',
    'GRNS',
    'GROVE',
    'GROV',
    'GRV',
    'GROVES',
    'GRVS',
    'HARBOR',
    'HARB',
    'HBR',
    'HARBR',
    'HRBOR',
    'HARBORS',
    'HBRS',
    'HAVEN',
    'HVN',
    'HEIGHTS',
    'HT',
    'HTS',
    'HIGHWAY',
    'HWY',
    'HIGHWY',
    'HIWAY',
    'HIWY',
    'HWAY',
    'HILL',
    'HL',
    'HILLS',
    'HLS',
    'HOLLOW',
    'HLLW',
    'HOLW',
    'HOLLOWS',
    'HOLWS',
    'INLET',
    'INLT',
    'ISLAND',
    'IS',
    'ISLND',
    'ISLANDS',
    'ISS',
    'ISLNDS',
    'ISLE',
    'ISLES',
    'JUNCTION',
    'JCT',
    'JCTION',
    'JCTN',
    'JUNCTN',
    'JUNCTON',
    'JUNCTIONS',
    'JCTNS',
    'JCTS',
    'KEY',
    'KY',
    'KEYS',
    'KYS',
    'KNOLL',
    'KNL',
    'KNOL',
    'KNOLLS',
    'KNLS',
    'LAKE',
    'LK',
    'LAKES',
    'LKS',
    'LAND',
    'LANDING',
    'LNDG',
    'LNDNG',
    'LANE',
    'LN',
    'LIGHT',
    'LGT',
    'LIGHTS',
    'LGTS',
    'LOAF',
    'LF',
    'LOCK',
    'LCK',
    'LOCKS',
    'LCKS',
    'LODGE',
    'LDG',
    'LDGE',
    'LODG',
    'LOOP',
    'LOOPS',
    'MALL',
    'MANOR',
    'MNR',
    'MANORS',
    'MNRS',
    'MEADOW',
    'MDW',
    'MEADOWS',
    'MDWS',
    'MEDOWS',
    'MEWS',
    'MILL',
    'ML',
    'MILLS',
    'MLS',
    'MISSION',
    'MISSN',
    'MSN',
    'MSSN',
    'MOTORWAY',
    'MTWY',
    'MOUNT',
    'MNT',
    'MT',
    'MOUNTAIN',
    'MNTAIN',
    'MTN',
    'MNTN',
    'MOUNTIN',
    'MTIN',
    'MOUNTAINS',
    'MNTNS',
    'MTNS',
    'NECK',
    'NCK',
    'ORCHARD',
    'ORCH',
    'ORCHRD',
    'OVAL',
    'OVL',
    'OVERPASS',
    'OPAS',
    'PARK',
    'PRK',
    'PARKS',
    'PARKWAY',
    'PKWY',
    'PARKWY',
    'PKWAY',
    'PKY',
    'PARKWAYS',
    'PKWYS',
    'PASS',
    'PASSAGE',
    'PSGE',
    'PATH',
    'PATHS',
    'PIKE',
    'PIKES',
    'PINE',
    'PNE',
    'PINES',
    'PNES',
    'PLACE',
    'PL',
    'PLAIN',
    'PLN',
    'PLAINS',
    'PLNS',
    'PLAZA',
    'PLZ',
    'PLZA',
    'POINT',
    'PT',
    'POINTS',
    'PTS',
    'PORT',
    'PRT',
    'PORTS',
    'PRTS',
    'PRAIRIE',
    'PR',
    'PRR',
    'RADIAL',
    'RAD',
    'RADL',
    'RADIEL',
    'RAMP',
    'RANCH',
    'RNCH',
    'RANCHES',
    'RNCHS',
    'RAPID',
    'RPD',
    'RAPIDS',
    'RPDS',
    'REST',
    'RST',
    'RIDGE',
    'RDG',
    'RDGE',
    'RIDGES',
    'RDGS',
    'RIVER',
    'RIV',
    'RVR',
    'RIVR',
    'ROAD',
    'RD',
    'ROADS',
    'RDS',
    'ROUTE',
    'RTE',
    'ROW',
    'RUE',
    'RUN',
    'SHOAL',
    'SHL',
    'SHOALS',
    'SHLS',
    'SHORE',
    'SHOAR',
    'SHR',
    'SHORES',
    'SHOARS',
    'SHRS',
    'SKYWAY',
    'SKWY',
    'SPRING',
    'SPG',
    'SPNG',
    'SPRNG',
    'SPRINGS',
    'SPGS',
    'SPNGS',
    'SPRNGS',
    'SPUR',
    'SPURS',
    'SQUARE',
    'SQ',
    'SQR',
    'SQRE',
    'SQU',
    'SQUARES',
    'SQRS',
    'SQS',
    'STATION',
    'STA',
    'STATN',
    'STN',
    'STRAVENUE',
    'STRA',
    'STRAV',
    'STRAVEN',
    'STRAVN',
    'STRVN',
    'STRVNUE',
    'STREAM',
    'STRM',
    'STREME',
    'STREET',
    'ST',
    'STRT',
    'STR',
    'STREETS',
    'STS',
    'SUMMIT',
    'SMT',
    'SUMIT',
    'SUMITT',
    'TERRACE',
    'TER',
    'TERR',
    'THROUGHWAY',
    'TRWY',
    'TRACE',
    'TRCE',
    'TRACES',
    'TRACK',
    'TRAK',
    'TRACKS',
    'TRK',
    'TRKS',
    'TRAFFICWAY',
    'TRFY',
    'TRAIL',
    'TRL',
    'TRAILS',
    'TRLS',
    'TRAILER',
    'TRLR',
    'TRLRS',
    'TUNNEL',
    'TUNEL',
    'TUNL',
    'TUNLS',
    'TUNNELS',
    'TUNNL',
    'TURNPIKE',
    'TRNPK',
    'TPKE',
    'TURNPK',
    'UNDERPASS',
    'UPAS',
    'UNION',
    'UN',
    'UNIONS',
    'UNS',
    'VALLEY',
    'VLY',
    'VALLY',
    'VLLY',
    'VALLEYS',
    'VLYS',
    'VIADUCT',
    'VDCT',
    'VIA',
    'VIADCT',
    'VIEW',
    'VW',
    'VIEWS',
    'VWS',
    'VILLAGE',
    'VILL',
    'VLG',
    'VILLAG',
    'VILLG',
    'VILLIAGE',
    'VILLAGES',
    'VLGS',
    'VILLE',
    'VL',
    'VISTA',
    'VIS',
    'VIST',
    'VST',
    'VSTA',
    'WALK',
    'WALKS',
    'WALL',
    'WAY',
    'WY',
    'WAYS',
    'WELL',
    'WL',
    'WELLS',
    'WLS'
]

dir = {
    'E': 'EAST',
    'W': 'WEST',
    'N': 'NORTH',
    'S': 'SOUTH',
    'NE': 'NORTHEAST',
    'NW': 'NORTHWEST',
    'SE': 'SOUTHEAST',
    'SW': 'SOUTHWEST',
    'NORTH EAST': 'NORTHEAST',
    'NORTH WEST': 'NORTHWEST',
    'SOUTH EAST': 'SOUTHEAST',
    'SOUTH WEST': 'SOUTHWEST',
}

state = {
    "ALABAMA": "AL"
    , "ALASKA": "AK"
    , "ARIZONA": "AZ"
    , "ARKANSAS": "AR"
    , "ARMED FORCES PACIFIC": "AP"
    , "CALIFORNIA": "CA"
    , "COLORADO": "CO"
    , "CONNECTICUT": "CT"
    , "DELAWARE": "DE"
    , "DISTRICT OF COLUMBIA": "DC"
    , "FLORIDA": "FL"
    , "GEORGIA": "GA"
    , "HAWAII": "HI"
    , "IDAHO": "ID"
    , "ILLINOIS": "IL"
    , "INDIANA": "IN"
    , "IOWA": "IA"
    , "KANSAS": "KS"
    , "KENTUCKY": "KY"
    , "LOUISIANA": "LA"
    , "MAINE": "ME"
    , "MARYLAND": "MD"
    , "MASSACHUSETTS": "MA"
    , "MICHIGAN": "MI"
    , "MINNESOTA": "MN"
    , "MISSISSIPPI": "MS"
    , "MISSOURI": "MO"
    , "MONTANA": "MT"
    , "NEBRASKA": "NE"
    , "NEVADA": "NV"
    , "NEW HAMPSHIRE": "NH"
    , "NEW JERSEY": "NJ"
    , "NEW MEXICO": "NM"
    , "NEW YORK": "NY"
    , "NORTH CAROLINA": "NC"
    , "NORTH DAKOTA": "ND"
    , "OHIO": "OH"
    , "OKLAHOMA": "OK"
    , "OREGON": "OR"
    , "PENNSYLVANIA": "PA"
    , "RHODE ISLAND": "RI"
    , "SOUTH CAROLINA": "SC"
    , "SOUTH DAKOTA": "SD"
    , "TENNESSEE": "TN"
    , "TEXAS": "TX"
    , "UTAH": "UT"
    , "VERMONT": "VT"
    , "VIRGINIA": "VA"
    , "VIRGIN ISLANDS": "VI"
    , "WASHINGTON": "WA"
    , "WEST VIRGINIA": "WV"
    , "WISCONSIN": "WI"
    , "WYOMING": "WY"
    , ",": ""
    , ".": ""
    , "CORPORATION": "CORP"
    , "CORPORA": "CORP"
    , "COMPANY": "CO"
    , "INSURANCE": "INS"
    , "INC": ""
    , "LLC": ""
    , "MANAGEMENT": "MGMT"
    , "GROUP": "GRP"
    , "SOLUTION": "SOLN"
    , "SERVICE": "SVC"
    , "EMPLOYMENT": "EMPL"
    , "DEPARTMENT": "DEPT"
    , "COM PANY": ""
    , "SCHOOL": "SCH"
    , "METROPOLITAN ATLANTA RAPID TRANSIT AUTHORITY": "MARTA"
    , "GENERAL PARTNERSHIP": "GP"
    , "LIMITED PARTNERSHIP": "LP"
    , "LIMITED LIABILITY PARTNERSHIP": "LLP"
}

nums = {
    'FIRST': '1ST',
    'SECOND': '2ND',
    'THIRD': '3RD',
    'FOURTH': '4TH',
    'FIFTH': '5TH',
    'SIXTH': '6TH',
    'SEVENTH': '7TH',
    'EIGHTH': '8TH',
    'NINTH': '9TH',
    'TENTH': '10TH',
}

wc = []


#----
# grep list of relevant (work-comp) claims only
#----
ip = sys.stdin.readlines()   # save stream into list of lines

[wc.append(re.match(r'\d{7}', l).group()) for l in ip if 'should be' in l]


for line0 in ip:
    if 'should be' in line0 or re.match(r'\d{7}', line0).group() in wc:    # WC stays TP
        continue

    if not re.search(r'(?<=[:]).*?(?=[|])', line0).group().strip():
        continue    # COMMERCIAL stays TP 

    if len(line0.split('--')) < 3:
        continue    # filter TP in name fields 

    d = 0

    line0 = line0.strip()

    line = deepcopy(line0)
    line = line.split(' - ')[0].split(' : ')


    ky = line[0]
    v = line[1]

    val = v.split(' -- ')
    
    fname_i = val[0].strip().split('|')[0]
    fname_p = val[0].strip().split('|')[1]
    lname_i = val[1].strip().split('|')[0]
    lname_p = val[1].strip().split('|')[1]

    for j in ('f', 'l'):
        globals()[f'{j}name'] = []

        for k in ('i', 'p'): 
            globals()[f'{j}name'].append(globals()[f'{j}name_{k}'])

    valcompare = val[2:]

    addr_l = [x.strip() for x in valcompare[0].split('|')]
    phone_l = [x.strip() for x in valcompare[1].split('|')]

    addr_l = [re.sub(r'\s+', ' ', x) for x in addr_l]

    addr_l1 = []
    for addr in addr_l:

        for i in suffix:    # remove type of street
            for j in addr.split(' '):
                if i == j:
                    addr = re.sub(r'\b{}\b'.format(j), '', addr).strip()
                    addr = re.sub(r'\s+', ' ', addr)

        for k, v in dir.items():    # convert to word direction
            for j in addr.split(' '):
                if k == j:
                    addr = re.sub(r'\b{}\b'.format(j), v, addr).strip()

        for k, v in nums.items():    # covert to number street num
            for j in addr.split(' '):
                if k == j or v == j:
                    addr = re.sub(r'\b{}\b'.format(j), v, addr).strip()

        for k, v in state.items():    # remove full and short state
            for j in addr.split(' '):
                if k == j or v == j:
                    addr = re.sub(r'\b{}\b'.format(j), '', addr).strip()
        addr_l1.append(addr)

    # ----
    # check if two similar addresses mean the same place
    # ----
    if similar(addr_l1[0], addr_l1[1]):
        d += 1
    if similar(addr_l1[0], addr_l1[2]):
        d += 1

    # ----
    # check phone numbers
    #----
    if (phone_l[0] == phone_l[1]) and phone_l[0].strip() and phone_l[1].strip():
        d += 1
    if (phone_l[0] == phone_l[2]) and phone_l[0].strip() and phone_l[2].strip():
        d += 1

    # ----
    # check if two similar first/last names belong to same person
    # ----
    if similar(fname_i, fname_p) and similar(lname_i, lname_p):
        d += 1

    # if no similiar matches at all
    if not d == 0:
        print(line0)
        pass

