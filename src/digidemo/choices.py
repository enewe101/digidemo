def get_choice(choices, pick):
	return filter(lambda x: x[0]==pick, choices)[0][1]

VALENCE_CHOICES = [
	(1, 'support'),
	(-1, 'oppose'),
	(0, 'ammend'),
]

VOTE_CHOICES = [
	(-1, 'down vote'),
	(0, 'non vote'),
	(1, 'up vote'),
]

FACTOR_CHOICES = [
	(-1, 'risk'),
	(1, 'benefit')
]

FACTOR_SECTORS = [
	('ECO', 'economy'),
	('ENV', 'environment'),
	('HEA', 'health'),
	('EDU', 'education'),
	('IR', 'international relations'),	
	('SOC', 'society and culture'),
	('SEC', 'security and rediness'),
	('DEM', 'democratic mechanisms'),
]

LEGAL_CLASSIFICATIONS = [
	('NP', 'non profit'),
	('NFP', 'not for profit'),
	('CH', 'charity'),
	('CPN', 'corporation'),
	('CRN', 'crown corporation'),
	('GVA', 'government agency'),
	('NPT', 'national political party'),
	('PPT', 'provincial political party'),
	('CTY', 'city / municipal administration'),
	('FND', 'foundation'),
	('COL', 'university or college'),
	('PRO', 'professional standards body'),
	('PRG', 'provincial regulatory association'),
	('NRG', 'national regulatory association'),
	('NGO', 'non-governmental organization'),
	('IG', 'industry group'),
	('LBU', 'labour union'),
	('OIG', 'other interest group'),
]

PROVINCES = [
	('AB', 'Alberta'),
	('BC', 'British Columbia'),
	('MB', 'Manitoba'),
	('SK', 'Saskatchewan'),
	('PE', 'Prince Edward Island'),
	('QC', 'Quebec'),
	('NL', 'Newfoundland and Labrador'),
	('NU', 'Nunavut'),
	('YT', 'Yukon'),
	('NS', 'Nova Scotia'),
	('NB', 'New Brunswick'),
	('NT', 'Northwest Territories'),
	('ON', 'Ontario')
]

COUNTRIES = [
	('ABW', 'Aruba'),
	('AFG', 'Afghanistan'),
	('AGO', 'Angola'),
	('AIA', 'Anguilla'),
	('ALA', '\xc3\x85land Islands'),
	('ALB', 'Albania'),
	('AND', 'Andorra'),
	('ARE', 'United Arab Emirates'),
	('ARG', 'Argentina'),
	('ARM', 'Armenia'),
	('ASM', 'American Samoa'),
	('ATA', 'Antarctica'),
	('ATF', 'French Southern Territories'),
	('ATG', 'Antigua and Barbuda'),
	('AUS', 'Australia'),
	('AUT', 'Austria'),
	('AZE', 'Azerbaijan'),
	('BDI', 'Burundi'),
	('BEL', 'Belgium'),
	('BEN', 'Benin'),
	('BES', 'Bonaire, Sint Eustatius and Saba'),
	('BFA', 'Burkina Faso'),
	('BGD', 'Bangladesh'),
	('BGR', 'Bulgaria'),
	('BHR', 'Bahrain'),
	('BHS', 'Bahamas'),
	('BIH', 'Bosnia and Herzegovina'),
	('BLM', 'Saint Barth\xc3\xa9lemy'),
	('BLR', 'Belarus'),
	('BLZ', 'Belize'),
	('BMU', 'Bermuda'),
	('BOL', 'Bolivia, Plurinational State of'),
	('BRA', 'Brazil'),
	('BRB', 'Barbados'),
	('BRN', 'Brunei Darussalam'),
	('BTN', 'Bhutan'),
	('BVT', 'Bouvet Island'),
	('BWA', 'Botswana'),
	('CAF', 'Central African Republic'),
	('CAN', 'Canada'),
	('CCK', 'Cocos (Keeling) Islands'),
	('CHE', 'Switzerland'),
	('CHL', 'Chile'),
	('CHN', 'China'),
	('CIV', "C\xc3\xb4te d'Ivoire"),
	('CMR', 'Cameroon'),
	('COD', 'Congo, the Democratic Republic of the'),
	('COG', 'Congo'),
	('COK', 'Cook Islands'),
	('COL', 'Colombia'),
	('COM', 'Comoros'),
	('CPV', 'Cabo Verde'),
	('CRI', 'Costa Rica'),
	('CUB', 'Cuba'),
	('CUW', 'Cura\xc3\xa7ao'),
	('CXR', 'Christmas Island'),
	('CYM', 'Cayman Islands'),
	('CYP', 'Cyprus'),
	('CZE', 'Czech Republic'),
	('DEU', 'Germany'),
	('DJI', 'Djibouti'),
	('DMA', 'Dominica'),
	('DNK', 'Denmark'),
	('DOM', 'Dominican Republic'),
	('DZA', 'Algeria'),
	('ECU', 'Ecuador'),
	('EGY', 'Egypt'),
	('ERI', 'Eritrea'),
	('ESH', 'Western Sahara'),
	('ESP', 'Spain'),
	('EST', 'Estonia'),
	('ETH', 'Ethiopia'),
	('FIN', 'Finland'),
	('FJI', 'Fiji'),
	('FLK', 'Falkland Islands (Malvinas)'),
	('FRA', 'France'),
	('FRO', 'Faroe Islands'),
	('FSM', 'Micronesia, Federated States of'),
	('GAB', 'Gabon'),
	('GBR', 'United Kingdom'),
	('GEO', 'Georgia'),
	('GGY', 'Guernsey'),
	('GHA', 'Ghana'),
	('GIB', 'Gibraltar'),
	('GIN', 'Guinea'),
	('GLP', 'Guadeloupe'),
	('GMB', 'Gambia'),
	('GNB', 'Guinea-Bissau'),
	('GNQ', 'Equatorial Guinea'),
	('GRC', 'Greece'),
	('GRD', 'Grenada'),
	('GRL', 'Greenland'),
	('GTM', 'Guatemala'),
	('GUF', 'French Guiana'),
	('GUM', 'Guam'),
	('GUY', 'Guyana'),
	('HKG', 'Hong Kong'),
	('HMD', 'Heard Island and McDonald Islands'),
	('HND', 'Honduras'),
	('HRV', 'Croatia'),
	('HTI', 'Haiti'),
	('HUN', 'Hungary'),
	('IDN', 'Indonesia'),
	('IMN', 'Isle of Man'),
	('IND', 'India'),
	('IOT', 'British Indian Ocean Territory'),
	('IRL', 'Ireland'),
	('IRN', 'Iran, Islamic Republic of'),
	('IRQ', 'Iraq'),
	('ISL', 'Iceland'),
	('ISR', 'Israel'),
	('ITA', 'Italy'),
	('JAM', 'Jamaica'),
	('JEY', 'Jersey'),
	('JOR', 'Jordan'),
	('JPN', 'Japan'),
	('KAZ', 'Kazakhstan'),
	('KEN', 'Kenya'),
	('KGZ', 'Kyrgyzstan'),
	('KHM', 'Cambodia'),
	('KIR', 'Kiribati'),
	('KNA', 'Saint Kitts and Nevis'),
	('KOR', 'Korea, Republic of'),
	('KWT', 'Kuwait'),
	('LAO', "Lao People's Democratic Republic"),
	('LBN', 'Lebanon'),
	('LBR', 'Liberia'),
	('LBY', 'Libya'),
	('LCA', 'Saint Lucia'),
	('LIE', 'Liechtenstein'),
	('LKA', 'Sri Lanka'),
	('LSO', 'Lesotho'),
	('LTU', 'Lithuania'),
	('LUX', 'Luxembourg'),
	('LVA', 'Latvia'),
	('MAC', 'Macao'),
	('MAF', 'Saint Martin (French part)'),
	('MAR', 'Morocco'),
	('MCO', 'Monaco'),
	('MDA', 'Moldova, Republic of'),
	('MDG', 'Madagascar'),
	('MDV', 'Maldives'),
	('MEX', 'Mexico'),
	('MHL', 'Marshall Islands'),
	('MKD', 'Macedonia, the former Yugoslav Republic of'),
	('MLI', 'Mali'),
	('MLT', 'Malta'),
	('MMR', 'Myanmar'),
	('MNE', 'Montenegro'),
	('MNG', 'Mongolia'),
	('MNP', 'Northern Mariana Islands'),
	('MOZ', 'Mozambique'),
	('MRT', 'Mauritania'),
	('MSR', 'Montserrat'),
	('MTQ', 'Martinique'),
	('MUS', 'Mauritius'),
	('MWI', 'Malawi'),
	('MYS', 'Malaysia'),
	('MYT', 'Mayotte'),
	('NAM', 'Namibia'),
	('NCL', 'New Caledonia'),
	('NER', 'Niger'),
	('NFK', 'Norfolk Island'),
	('NGA', 'Nigeria'),
	('NIC', 'Nicaragua'),
	('NIU', 'Niue'),
	('NLD', 'Netherlands'),
	('NOR', 'Norway'),
	('NPL', 'Nepal'),
	('NRU', 'Nauru'),
	('NZL', 'New Zealand'),
	('OMN', 'Oman'),
	('PAK', 'Pakistan'),
	('PAN', 'Panama'),
	('PCN', 'Pitcairn'),
	('PER', 'Peru'),
	('PHL', 'Philippines'),
	('PLW', 'Palau'),
	('PNG', 'Papua New Guinea'),
	('POL', 'Poland'),
	('PRI', 'Puerto Rico'),
	('PRK', "Korea, Democratic People's Republic of"),
	('PRT', 'Portugal'),
	('PRY', 'Paraguay'),
	('PSE', 'Palestine, State of'),
	('PYF', 'French Polynesia'),
	('QAT', 'Qatar'),
	('REU', 'R\xc3\xa9union'),
	('ROU', 'Romania'),
	('RUS', 'Russian Federation'),
	('RWA', 'Rwanda'),
	('SAU', 'Saudi Arabia'),
	('SDN', 'Sudan'),
	('SEN', 'Senegal'),
	('SGP', 'Singapore'),
	('SGS', 'South Georgia and the South Sandwich Islands'),
	('SHN', 'Saint Helena, Ascension and Tristan da Cunha'),
	('SJM', 'Svalbard and Jan Mayen'),
	('SLB', 'Solomon Islands'),
	('SLE', 'Sierra Leone'),
	('SLV', 'El Salvador'),
	('SMR', 'San Marino'),
	('SOM', 'Somalia'),
	('SPM', 'Saint Pierre and Miquelon'),
	('SRB', 'Serbia'),
	('SSD', 'South Sudan'),
	('STP', 'Sao Tome and Principe'),
	('SUR', 'Suriname'),
	('SVK', 'Slovakia'),
	('SVN', 'Slovenia'),
	('SWE', 'Sweden'),
	('SWZ', 'Swaziland'),
	('SXM', 'Sint Maarten (Dutch part)'),
	('SYC', 'Seychelles'),
	('SYR', 'Syrian Arab Republic'),
	('TCA', 'Turks and Caicos Islands'),
	('TCD', 'Chad'),
	('TGO', 'Togo'),
	('THA', 'Thailand'),
	('TJK', 'Tajikistan'),
	('TKL', 'Tokelau'),
	('TKM', 'Turkmenistan'),
	('TLS', 'Timor-Leste'),
	('TON', 'Tonga'),
	('TTO', 'Trinidad and Tobago'),
	('TUN', 'Tunisia'),
	('TUR', 'Turkey'),
	('TUV', 'Tuvalu'),
	('TWN', 'Taiwan, Province of China'),
	('TZA', 'Tanzania, United Republic of'),
	('UGA', 'Uganda'),
	('UKR', 'Ukraine'),
	('UMI', 'United States Minor Outlying Islands'),
	('URY', 'Uruguay'),
	('USA', 'United States'),
	('UZB', 'Uzbekistan'),
	('VAT', 'Holy See (Vatican City State)'),
	('VCT', 'Saint Vincent and the Grenadines'),
	('VEN', 'Venezuela, Bolivarian Republic of'),
	('VGB', 'Virgin Islands, British'),
	('VIR', 'Virgin Islands, U.S.'),
	('VNM', 'Viet Nam'),
	('VUT', 'Vanuatu'),
	('WLF', 'Wallis and Futuna'),
	('WSM', 'Samoa'),
	('YEM', 'Yemen'),
	('ZAF', 'South Africa'),
	('ZMB', 'Zambia'),
	('ZWE', 'Zimbabwe'),
]
