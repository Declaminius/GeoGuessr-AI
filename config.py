states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg", "Vienna"],\
                "Australia": ["australian_capital_territory", "tasmania", "northern_territory", "western_australia", "south_australia", "queensland", "victoria", "new_south_wales"],\
                "New Zealand": ["West Coast", "Marlborough", "Gisborne", "Nelson", "Tasman", "Southland", "Taranaki", "Hawke's Bay", "Northland", "Otago", "Manawatū-Whanganui", "Bay of Plenty", "Waikato", "Wellington", "Canterbury", "Auckland"],\
                "Slovakia": ["Region of Bratislava", "Nitra", "Trnava", "Trencin", "Kosice", "Region of Banska Bystrica", "Presov", "Zilina"],\
                "Czechia": ["Northwest", "Southwest", "Central Bohemia", "Prague", "Northeast", "Southeast", "Central Moravia", "Moravia-Silesia"]
                #  ["Prague", "Central Bohemian", "South Bohemian", "Plzen", "Karlovy Vary", "Usti nad Labem", "Liberec", "Hradec Kralove", "Pardubice", "Vysocina", "Olomouc", "Zlin", "Moravian-Silesian"]
                }


highway_filter = '["highway"~"motorway|trunk|primary|secondary|tertiary"]'
highway_filter_pyrosm = {"highway": ["motorway", "trunk", "primary", "secondary"]}