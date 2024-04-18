from collections import Counter

def give_muni():
    muni = [
        "101", "201", "151", "400", "153", "155", "240", "210", "147", "250",
        "190", "157", "159", "161", "270", "260", "217", "163", "219", "167",
        "169", "223", "183", "165", "173", "230", "175", "185", "187", "320",
        "253", "376", "316", "326", "259", "350", "360", "370", "306", "329",
        "265", "330", "340", "269", "336", "390", "530", "561", "607", "510",
        "621", "540", "550", "573", "575", "630", "580", "420", "563", "430",
        "440", "482", "410", "480", "450", "461", "479", "492", "710", "766",
        "657", "661", "615", "756", "665", "707", "727", "730", "760", "741",
        "740", "746", "779", "671", "706", "791", "751", "810", "813", "860",
        "849", "825", "846", "773", "840", "787", "820", "851",
    ]
    return muni

def give_region():
    data = {
        "101": "Hovedstaden",
        "201": "Hovedstaden",
        "151": "Hovedstaden",
        "400": "Hovedstaden",
        "153": "Hovedstaden",
        "155": "Hovedstaden",
        "240": "Hovedstaden",
        "210": "Hovedstaden",
        "147": "Hovedstaden",
        "250": "Hovedstaden",
        "190": "Hovedstaden",
        "157": "Hovedstaden",
        "159": "Hovedstaden",
        "161": "Hovedstaden",
        "270": "Hovedstaden",
        "260": "Hovedstaden",
        "217": "Hovedstaden",
        "163": "Hovedstaden",
        "219": "Hovedstaden",
        "167": "Hovedstaden",
        "169": "Hovedstaden",
        "223": "Hovedstaden",
        "183": "Hovedstaden",
        "165": "Hovedstaden",
        "173": "Hovedstaden",
        "230": "Hovedstaden",
        "175": "Hovedstaden",
        "185": "Hovedstaden",
        "187": "Hovedstaden",
        "320": "Sjaelland",
        "253": "Sjaelland",
        "376": "Sjaelland",
        "316": "Sjaelland",
        "326": "Sjaelland",
        "259": "Sjaelland",
        "350": "Sjaelland",
        "360": "Sjaelland",
        "370": "Sjaelland",
        "306": "Sjaelland",
        "329": "Sjaelland",
        "265": "Sjaelland",
        "330": "Sjaelland",
        "340": "Sjaelland",
        "269": "Sjaelland",
        "336": "Sjaelland",
        "390": "Sjaelland",
        "530": "Syddanmark",
        "561": "Syddanmark",
        "607": "Syddanmark",
        "510": "Syddanmark",
        "621": "Syddanmark",
        "540": "Syddanmark",
        "550": "Syddanmark",
        "573": "Syddanmark",
        "575": "Syddanmark",
        "630": "Syddanmark",
        "580": "Syddanmark",
        "420": "Syddanmark",
        "563": "Syddanmark",
        "430": "Syddanmark",
        "440": "Syddanmark",
        "482": "Syddanmark",
        "410": "Syddanmark",
        "480": "Syddanmark",
        "450": "Syddanmark",
        "461": "Syddanmark",
        "479": "Syddanmark",
        "492": "Syddanmark",
        "710": "Midtjylland",
        "766": "Midtjylland",
        "657": "Midtjylland",
        "661": "Midtjylland",
        "615": "Midtjylland",
        "756": "Midtjylland",
        "665": "Midtjylland",
        "707": "Midtjylland",
        "727": "Midtjylland",
        "730": "Midtjylland",
        "760": "Midtjylland",
        "741": "Midtjylland",
        "740": "Midtjylland",
        "746": "Midtjylland",
        "779": "Midtjylland",
        "671": "Midtjylland",
        "706": "Midtjylland",
        "791": "Midtjylland",
        "751": "Midtjylland",
        "810": "Nordjylland",
        "813": "Nordjylland",
        "860": "Nordjylland",
        "849": "Nordjylland",
        "825": "Nordjylland",
        "846": "Nordjylland",
        "773": "Nordjylland",
        "840": "Nordjylland",
        "787": "Nordjylland",
        "820": "Nordjylland",
        "851": "Nordjylland",
    }
    return data

def count_regions():
    data = give_region()  # Retrieve the data from your function
    region_counts = Counter(data.values())  # Count occurrences of each region
    counts_only = list(region_counts.values())  # Extract only the counts
    return counts_only

def count_municipalities_in_region(region):
    # Get the region dictionary from the give_region function
    regions = give_region()
    
    # Count how many times the given region appears in the dictionary
    region_count = sum(1 for muni in regions.values() if muni == region)
    
    return region_count


def give_regionDictionary():
    # Initialize the list of municipalities for each region
    regionDictionary = {
        "Hovedstaden": [],
        "Sjaelland": [],
        "Syddanmark": [],
        "Midtjylland": [],
        "Nordjylland": [],
    }

    # Populate the regions dictionary
    for mun, region in give_region().items():
        regionDictionary[region].append(mun)
    return regionDictionary



