from django.utils.translation import ugettext_noop as _

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

#FACTOR_SECTORS = [
#	('ECO', 'economy'),
#	('ENV', 'environment'),
#	('HEA', 'health'),
#	('EDU', 'education'),
#	('IR', 'international relations'),	
#	('SOC', 'society and culture'),
#	('SEC', 'security and rediness'),
#	('DEM', 'democratic mechanisms'),
#]

LEGAL_CLASSIFICATIONS = [
	('NP', _('non profit')),
	('NFP', _('not for profit')),
	('CH', _('charity')),
	('CPN', _('corporation')),
	('CRN', _('crown corporation')),
	('GVA', _('government agency')),
	('NPT', _('national political party')),
	('PPT', _('provincial political party')),
	('CTY', _('city / municipal administration')),
	('FND', _('foundation')),
	('COL', _('university or college')),
	('PRO', _('professional standards body')),
	('PRG', _('provincial regulatory association')),
	('NRG', _('national regulatory association')),
	('NGO', _('non-governmental organization')),
	('IG', _('industry group')),
	('LBU', _('labour union')),
	('OIG', _('other interest group')),
]

PROVINCES = [
	('AB', _('Alberta')),
	('BC', _('British Columbia')),
	('MB', _('Manitoba')),
	('SK', _('Saskatchewan')),
	('PE', _('Prince Edward Island')),
	('QC', _('Quebec')),
	('NL', _('Newfoundland and Labrador')),
	('NU', _('Nunavut')),
	('YT', _('Yukon')),
	('NS', _('Nova Scotia')),
	('NB', _('New Brunswick')),
	('NT', _('Northwest Territories')),
	('ON', _('Ontario'))
]

COUNTRIES = [
	('ABW', _('Aruba')),
	('AFG', _('Afghanistan')),
	('AGO', _('Angola')),
	('AIA', _('Anguilla')),
	('ALA', _('\xc3\x85land Islands')),
	('ALB', _('Albania')),
	('AND', _('Andorra')),
	('ARE', _('United Arab Emirates')),
	('ARG', _('Argentina')),
	('ARM', _('Armenia')),
	('ASM', _('American Samoa')),
	('ATA', _('Antarctica')),
	('ATF', _('French Southern Territories')),
	('ATG', _('Antigua and Barbuda')),
	('AUS', _('Australia')),
	('AUT', _('Austria')),
	('AZE', _('Azerbaijan')),
	('BDI', _('Burundi')),
	('BEL', _('Belgium')),
	('BEN', _('Benin')),
	('BES', _('Bonaire, Sint Eustatius and Saba')),
	('BFA', _('Burkina Faso')),
	('BGD', _('Bangladesh')),
	('BGR', _('Bulgaria')),
	('BHR', _('Bahrain')),
	('BHS', _('Bahamas')),
	('BIH', _('Bosnia and Herzegovina')),
	('BLM', _('Saint Barth\xc3\xa9lemy')),
	('BLR', _('Belarus')),
	('BLZ', _('Belize')),
	('BMU', _('Bermuda')),
	('BOL', _('Bolivia, Plurinational State of')),
	('BRA', _('Brazil')),
	('BRB', _('Barbados')),
	('BRN', _('Brunei Darussalam')),
	('BTN', _('Bhutan')),
	('BVT', _('Bouvet Island')),
	('BWA', _('Botswana')),
	('CAF', _('Central African Republic')),
	('CAN', _('Canada')),
	('CCK', _('Cocos (Keeling) Islands')),
	('CHE', _('Switzerland')),
	('CHL', _('Chile')),
	('CHN', _('China')),
	('CIV', _("C\xc3\xb4te d'Ivoire")),
	('CMR', _('Cameroon')),
	('COD', _('Congo, the Democratic Republic of the')),
	('COG', _('Congo')),
	('COK', _('Cook Islands')),
	('COL', _('Colombia')),
	('COM', _('Comoros')),
	('CPV', _('Cabo Verde')),
	('CRI', _('Costa Rica')),
	('CUB', _('Cuba')),
	('CUW', _('Cura\xc3\xa7ao')),
	('CXR', _('Christmas Island')),
	('CYM', _('Cayman Islands')),
	('CYP', _('Cyprus')),
	('CZE', _('Czech Republic')),
	('DEU', _('Germany')),
	('DJI', _('Djibouti')),
	('DMA', _('Dominica')),
	('DNK', _('Denmark')),
	('DOM', _('Dominican Republic')),
	('DZA', _('Algeria')),
	('ECU', _('Ecuador')),
	('EGY', _('Egypt')),
	('ERI', _('Eritrea')),
	('ESH', _('Western Sahara')),
	('ESP', _('Spain')),
	('EST', _('Estonia')),
	('ETH', _('Ethiopia')),
	('FIN', _('Finland')),
	('FJI', _('Fiji')),
	('FLK', _('Falkland Islands (Malvinas)')),
	('FRA', _('France')),
	('FRO', _('Faroe Islands')),
	('FSM', _('Micronesia, Federated States of')),
	('GAB', _('Gabon')),
	('GBR', _('United Kingdom')),
	('GEO', _('Georgia')),
	('GGY', _('Guernsey')),
	('GHA', _('Ghana')),
	('GIB', _('Gibraltar')),
	('GIN', _('Guinea')),
	('GLP', _('Guadeloupe')),
	('GMB', _('Gambia')),
	('GNB', _('Guinea-Bissau')),
	('GNQ', _('Equatorial Guinea')),
	('GRC', _('Greece')),
	('GRD', _('Grenada')),
	('GRL', _('Greenland')),
	('GTM', _('Guatemala')),
	('GUF', _('French Guiana')),
	('GUM', _('Guam')),
	('GUY', _('Guyana')),
	('HKG', _('Hong Kong')),
	('HMD', _('Heard Island and McDonald Islands')),
	('HND', _('Honduras')),
	('HRV', _('Croatia')),
	('HTI', _('Haiti')),
	('HUN', _('Hungary')),
	('IDN', _('Indonesia')),
	('IMN', _('Isle of Man')),
	('IND', 'India'),
	('IOT', _('British Indian Ocean Territory')),
	('IRL', _('Ireland')),
	('IRN', _('Iran, Islamic Republic of')),
	('IRQ', _('Iraq')),
	('ISL', _('Iceland')),
	('ISR', _('Israel')),
	('ITA', _('Italy')),
	('JAM', _('Jamaica')),
	('JEY', _('Jersey')),
	('JOR', _('Jordan')),
	('JPN', _('Japan')),
	('KAZ', _('Kazakhstan')),
	('KEN', _('Kenya')),
	('KGZ', _('Kyrgyzstan')),
	('KHM', _('Cambodia')),
	('KIR', _('Kiribati')),
	('KNA', _('Saint Kitts and Nevis')),
	('KOR', _('Korea, Republic of')),
	('KWT', _('Kuwait')),
	('LAO', _("Lao People's Democratic Republic")),
	('LBN', _('Lebanon')),
	('LBR', _('Liberia')),
	('LBY', _('Libya')),
	('LCA', _('Saint Lucia')),
	('LIE', _('Liechtenstein')),
	('LKA', _('Sri Lanka')),
	('LSO', _('Lesotho')),
	('LTU', _('Lithuania')),
	('LUX', _('Luxembourg')),
	('LVA', _('Latvia')),
	('MAC', _('Macao')),
	('MAF', _('Saint Martin (French part)')),
	('MAR', _('Morocco')),
	('MCO', _('Monaco')),
	('MDA', _('Moldova, Republic of')),
	('MDG', _('Madagascar')),
	('MDV', _('Maldives')),
	('MEX', _('Mexico')),
	('MHL', _('Marshall Islands')),
	('MKD', _('Macedonia, the former Yugoslav Republic of')),
	('MLI', _('Mali')),
	('MLT', _('Malta')),
	('MMR', _('Myanmar')),
	('MNE', _('Montenegro')),
	('MNG', _('Mongolia')),
	('MNP', _('Northern Mariana Islands')),
	('MOZ', _('Mozambique')),
	('MRT', _('Mauritania')),
	('MSR', _('Montserrat')),
	('MTQ', _('Martinique')),
	('MUS', _('Mauritius')),
	('MWI', _('Malawi')),
	('MYS', _('Malaysia')),
	('MYT', _('Mayotte')),
	('NAM', _('Namibia')),
	('NCL', _('New Caledonia')),
	('NER', _('Niger')),
	('NFK', _('Norfolk Island')),
	('NGA', _('Nigeria')),
	('NIC', _('Nicaragua')),
	('NIU', _('Niue')),
	('NLD', _('Netherlands')),
	('NOR', _('Norway')),
	('NPL', _('Nepal')),
	('NRU', _('Nauru')),
	('NZL', _('New Zealand')),
	('OMN', _('Oman')),
	('PAK', _('Pakistan')),
	('PAN', _('Panama')),
	('PCN', _('Pitcairn')),
	('PER', _('Peru')),
	('PHL', _('Philippines')),
	('PLW', _('Palau')),
	('PNG', _('Papua New Guinea')),
	('POL', _('Poland')),
	('PRI', _('Puerto Rico')),
	('PRK', _("Korea, Democratic People's Republic of")),
	('PRT', _('Portugal')),
	('PRY', _('Paraguay')),
	('PSE', _('Palestine, State of')),
	('PYF', _('French Polynesia')),
	('QAT', _('Qatar')),
	('REU', _('R\xc3\xa9union')),
	('ROU', _('Romania')),
	('RUS', _('Russian Federation')),
	('RWA', _('Rwanda')),
	('SAU', _('Saudi Arabia')),
	('SDN', _('Sudan')),
	('SEN', _('Senegal')),
	('SGP', _('Singapore')),
	('SGS', _('South Georgia and the South Sandwich Islands')),
	('SHN', _('Saint Helena, Ascension and Tristan da Cunha')),
	('SJM', _('Svalbard and Jan Mayen')),
	('SLB', _('Solomon Islands')),
	('SLE', _('Sierra Leone')),
	('SLV', _('El Salvador')),
	('SMR', _('San Marino')),
	('SOM', _('Somalia')),
	('SPM', _('Saint Pierre and Miquelon')),
	('SRB', _('Serbia')),
	('SSD', _('South Sudan')),
	('STP', _('Sao Tome and Principe')),
	('SUR', _('Suriname')),
	('SVK', _('Slovakia')),
	('SVN', _('Slovenia')),
	('SWE', _('Sweden')),
	('SWZ', _('Swaziland')),
	('SXM', _('Sint Maarten (Dutch part)')),
	('SYC', _('Seychelles')),
	('SYR', _('Syrian Arab Republic')),
	('TCA', _('Turks and Caicos Islands')),
	('TCD', _('Chad')),
	('TGO', _('Togo')),
	('THA', _('Thailand')),
	('TJK', _('Tajikistan')),
	('TKL', _('Tokelau')),
	('TKM', _('Turkmenistan')),
	('TLS', _('Timor-Leste')),
	('TON', _('Tonga')),
	('TTO', _('Trinidad and Tobago')),
	('TUN', _('Tunisia')),
	('TUR', _('Turkey')),
	('TUV', _('Tuvalu')),
	('TWN', _('Taiwan, Province of China')),
	('TZA', _('Tanzania, United Republic of')),
	('UGA', _('Uganda')),
	('UKR', _('Ukraine')),
	('UMI', _('United States Minor Outlying Islands')),
	('URY', _('Uruguay')),
	('USA', _('United States')),
	('UZB', _('Uzbekistan')),
	('VAT', _('Holy See (Vatican City State)')),
	('VCT', _('Saint Vincent and the Grenadines')),
	('VEN', _('Venezuela, Bolivarian Republic of')),
	('VGB', _('Virgin Islands, British')),
	('VIR', _('Virgin Islands, U.S.')),
	('VNM', _('Viet Nam')),
	('VUT', _('Vanuatu')),
	('WLF', _('Wallis and Futuna')),
	('WSM', _('Samoa')),
	('YEM', _('Yemen')),
	('ZAF', _('South Africa')),
	('ZMB', _('Zambia')),
	('ZWE', _('Zimbabwe')),
]
