from selenium.webdriver import Firefox, FirefoxProfile
from bs4 import BeautifulSoup
from time import sleep, time
from urllib.error import HTTPError
from urllib.request import urlopen, Request
import webbrowser
from argparse import ArgumentParser
from socket import gethostbyname, gaierror
from os import getcwd, walk, remove, rename
from os.path import getsize, join, realpath
# from pdfkit import from_file
# TODO Fix pyDNS and check for emails with given username
# TODO Add arugment for specific county
# TODO Move HTML and pdfs to an "output" dir
b = ArgumentParser(description = "Collects social engineering data on an username", epilog = "Written by Thomas Gerot, Millard West Computer Science Club", prefix_chars = "-")
b.add_argument("-d", "--douglas", help = "Search the Douglas County Assesor", action = "store_true")
b.add_argument("-f", "--full", help = "Checks against every TLD", action = "store_true")
b.add_argument("-i", "--images", help = "Adds profile images to HTML output", action = "store_true")
b.add_argument("-l", "--links", help = "Open links to discovered accounts", action = "store_true")
b.add_argument("-m", "--multiple", help = "If multiple usernames are found, search them", action = "store_true")
b.add_argument("-p", "--pdf", help = "Output results to a PDF", action="store_true")
b.add_argument("-v", "--verbose", help = "Increases how wordy the program's output will be", action = "store_true")
b.add_argument("-w", "--webpage", help = "Write and open a nice HTML file of your results", action = "store_true")
c = b.add_argument_group("required arguements")
c.add_argument("-u", "--username", help = "The username to look for", required = True)
a = b.parse_args()
def d(m):
	if a.verbose is True:
		print(m)
d("Initializing data")
g = []
h = []
i = []
j = []
usernames = []
accounts = []
profiles = []
real_names = []
companies = []
locations = []
emails = []
sites = []
bios = []
events = []
public_keys = []
bitcoin_addresses = []
genders = []
ages = []
birthdays = []
images = []
domains = [".aaa", ".aarp", ".abb", ".abbott", ".abbvie", ".able", ".abogado", ".abudhabi", ".ac", ".academy", ".accenture", ".accountant", ".accountants", ".aco", ".active", ".actor", ".ad", ".adac", ".ads", ".adult", ".ae", ".aeg", ".aero", ".aetna", ".af", ".afl", ".ag", ".agakhan", ".agency", ".ai", ".aig", ".airbus", ".airforce", ".airtel", ".akdn", ".al", ".alibaba", ".alipay", ".allfinanz", ".allstate", ".ally", ".alsace", ".alstom", ".am", ".amica", ".amsterdam", ".an", ".analytics", ".android", ".anquan", ".anz", ".ao", ".apartments", ".app", ".apple", ".aq", ".aquarelle", ".ar", ".aramco", ".archi", ".army", ".arpa", ".art", ".arte", ".as", ".asia", ".associates", ".at", ".attorney", ".au", ".auction", ".audi", ".audible", ".audio", ".author", ".auto", ".autos", ".avianca", ".aw", ".aws", ".ax", ".axa", ".az", ".azure", ".ba", ".baby", ".baidu", ".band", ".bank", ".bar", ".barcelona", ".barclaycard", ".barclays", ".barefoot", ".bargains", ".bauhaus", ".bayern", ".bb", ".bbc", ".bbt", ".bbva", ".bcg", ".bcn", ".bd", ".be", ".beats", ".beauty", ".beer", ".bentley", ".berlin", ".best", ".bet", ".bf", ".bg", ".bh", ".bharti", ".bi", ".bible", ".bid", ".bike", ".bing", ".bingo", ".bio", ".biz", ".bj", ".bl", ".black", ".blackfriday", ".blanco", ".blog", ".bloomberg", ".blue", ".bm", ".bms", ".bmw", ".bn", ".bnl", ".bnpparibas", ".bo", ".boats", ".boehringer", ".bom", ".bond", ".boo", ".book", ".boots", ".bosch", ".bostik", ".bot", ".boutique", ".bq", ".br", ".bradesco", ".bridgestone", ".broadway", ".broker", ".brother", ".brussels", ".bs", ".bt", ".budapest", ".bugatti", ".build", ".builders", ".business", ".buy", ".buzz", ".bv", ".bw", ".by", ".bz", ".bzh", ".ca", ".cab", ".cafe", ".cal", ".call", ".cam", ".camera", ".camp", ".cancerresearch", ".canon", ".capetown", ".capital", ".car", ".caravan", ".cards", ".care", ".career", ".careers", ".cars", ".cartier", ".casa", ".cash", ".casino", ".cat", ".catering", ".cba", ".cbn", ".cbre", ".cc", ".cd", ".ceb", ".center", ".ceo", ".cern", ".cf", ".cfa", ".cfd", ".cg", ".ch", ".chanel", ".channel", ".chase", ".chat", ".cheap", ".chintai", ".chloe", ".christmas", ".chrome", ".church", ".ci", ".cipriani", ".circle", ".cisco", ".citic", ".city", ".cityeats", ".ck", ".cl", ".claims", ".cleaning", ".click", ".clinic", ".clinique", ".clothing", ".cloud", ".club", ".clubmed", ".cm", ".cn", ".co", ".coach", ".codes", ".coffee", ".college", ".cologne", ".com", ".comcast", ".commbank", ".community", ".company", ".compare", ".computer", ".comsec", ".condos", ".construction", ".consulting", ".contact", ".contractors", ".cooking", ".cookingchannel", ".cool", ".coop", ".corsica", ".country", ".coupon", ".coupons", ".courses", ".cr", ".credit", ".creditcard", ".creditunion", ".cricket", ".crown", ".crs", ".cruises", ".csc", ".cu", ".cuisinella", ".cv", ".cw", ".cx", ".cy", ".cymru", ".cyou", ".cz", ".dabur", ".dad", ".dance", ".date", ".dating", ".datsun", ".day", ".dclk", ".dds", ".de", ".deal", ".dealer", ".deals", ".degree", ".delivery", ".dell", ".deloitte", ".delta", ".democrat", ".dental", ".dentist", ".desi", ".design", ".dev", ".dhl", ".diamonds", ".diet", ".digital", ".direct", ".directory", ".discount", ".dj", ".dk", ".dm", ".dnp", ".do", ".docs", ".dog", ".doha", ".domains", ".doosan", ".dot", ".download", ".drive", ".dtv", ".dubai", ".dunlop", ".dupont", ".durban", ".dvag", ".dz", ".earth", ".eat", ".ec", ".edeka", ".edu", ".education", ".ee", ".eg", ".eh", ".email", ".emerck", ".energy", ".engineer", ".engineering", ".enterprises", ".epost", ".epson", ".equipment", ".er", ".ericsson", ".erni", ".es", ".esq", ".estate", ".et", ".eu", ".eurovision", ".eus", ".events", ".everbank", ".exchange", ".expert", ".exposed", ".express", ".extraspace", ".fage", ".fail", ".fairwinds", ".faith", ".family", ".fan", ".fans", ".farm", ".farmers", ".fashion", ".fast", ".fedex", ".feedback", ".ferrero", ".fi", ".film", ".final", ".finance", ".financial", ".fire", ".firestone", ".firmdale", ".fish", ".fishing", ".fit", ".fitness", ".fj", ".fk", ".flickr", ".flights", ".flir", ".florist", ".flowers", ".flsmidth", ".fly", ".fm", ".fo", ".foo", ".foodnetwork", ".football", ".ford", ".forex", ".forsale", ".forum", ".foundation", ".fox", ".fr", ".fresenius", ".frl", ".frogans", ".frontdoor", ".frontier", ".ftr", ".fujitsu", ".fujixerox", ".fund", ".furniture", ".futbol", ".fyi", ".ga", ".gal", ".gallery", ".gallo", ".gallup", ".game", ".games", ".garden", ".gb", ".gbiz", ".gd", ".gdn", ".ge", ".gea", ".gent", ".genting", ".gf", ".gg", ".ggee", ".gh", ".gi", ".gift", ".gifts", ".gives", ".giving", ".gl", ".glass", ".gle", ".global", ".globo", ".gm", ".gmail", ".gmbh", ".gmo", ".gmx", ".gn", ".godaddy", ".gold", ".goldpoint", ".golf", ".goo", ".goodhands", ".goodyear", ".goog", ".google", ".gop", ".got", ".gov", ".gp", ".gq", ".gr", ".grainger", ".graphics", ".gratis", ".green", ".gripe", ".group", ".gs", ".gt", ".gu", ".guardian", ".gucci", ".guge", ".guide", ".guitars", ".guru", ".gw", ".gy", ".hamburg", ".hangout", ".haus", ".hdfcbank", ".health", ".healthcare", ".help", ".helsinki", ".here", ".hermes", ".hgtv", ".hiphop", ".hisamitsu", ".hitachi", ".hiv", ".hk", ".hkt", ".hm", ".hn", ".hockey", ".holdings", ".holiday", ".homedepot", ".homegoods", ".homes", ".homesense", ".honda", ".horse", ".host", ".hosting", ".hoteles", ".hotmail", ".house", ".how", ".hr", ".hsbc", ".ht", ".htc", ".hu", ".hyundai", ".ibm", ".icbc", ".ice", ".icu", ".id", ".ie", ".ifm", ".iinet", ".ikano", ".il", ".im", ".imamat", ".imdb", ".immo", ".immobilien", ".in", ".industries", ".infiniti", ".info", ".ing", ".ink", ".institute", ".insurance", ".insure", ".int", ".international", ".intuit", ".investments", ".io", ".ipiranga", ".iq", ".ir", ".irish", ".is", ".iselect", ".ismaili", ".ist", ".istanbul", ".it", ".itau", ".itv", ".iwc", ".jaguar", ".java", ".jcb", ".jcp", ".je", ".jetzt", ".jewelry", ".jlc", ".jll", ".jm", ".jmp", ".jnj", ".jo", ".jobs", ".joburg", ".jot", ".joy", ".jp", ".jpmorgan", ".jprs", ".juegos", ".kaufen", ".kddi", ".ke", ".kerryhotels", ".kerrylogistics", ".kerryproperties", ".kfh", ".kg", ".kh", ".ki", ".kia", ".kim", ".kinder", ".kindle", ".kitchen", ".kiwi", ".km", ".kn", ".koeln", ".komatsu", ".kosher", ".kp", ".kpmg", ".kpn", ".kr", ".krd", ".kred", ".kuokgroup", ".kw", ".ky", ".kyoto", ".kz", ".la", ".lacaixa", ".lamborghini", ".lamer", ".lancaster", ".lancome", ".land", ".landrover", ".lanxess", ".lasalle", ".lat", ".latrobe", ".law", ".lawyer", ".lb", ".lc", ".lds", ".lease", ".leclerc", ".lefrak", ".legal", ".lego", ".lexus", ".lgbt", ".li", ".liaison", ".lidl", ".life", ".lifeinsurance", ".lifestyle", ".lighting", ".like", ".limited", ".limo", ".lincoln", ".linde", ".link", ".lipsy", ".live", ".living", ".lixil", ".lk", ".loan", ".loans", ".locker", ".locus", ".lol", ".london", ".lotte", ".lotto", ".love", ".lr", ".ls", ".lt", ".ltd", ".ltda", ".lu", ".lundbeck", ".lupin", ".luxe", ".luxury", ".lv", ".ly", ".ma", ".macys", ".madrid", ".maif", ".maison", ".makeup", ".man", ".management", ".mango", ".market", ".marketing", ".markets", ".marriott", ".marshalls", ".mattel", ".mba", ".mc", ".md", ".me", ".med", ".media", ".meet", ".melbourne", ".meme", ".memorial", ".men", ".menu", ".meo", ".metlife", ".mf", ".mg", ".mh", ".miami", ".microsoft", ".mil", ".mini", ".mint", ".mit", ".mitsubishi", ".mk", ".ml", ".mlb", ".mls", ".mm", ".mma", ".mn", ".mo", ".mobi", ".mobily", ".moda", ".moe", ".moi", ".mom", ".monash", ".money", ".montblanc", ".mormon", ".mortgage", ".moscow", ".motorcycles", ".mov", ".movie", ".movistar", ".mp", ".mq", ".mr", ".ms", ".mt", ".mtn", ".mtpc", ".mtr", ".mu", ".museum", ".mutual", ".mutuelle", ".mv", ".mw", ".mx", ".my", ".mz", ".na", ".nadex", ".nagoya", ".name", ".nationwide", ".natura", ".navy", ".nc", ".ne", ".nec", ".net", ".netbank", ".netflix", ".network", ".neustar", ".new", ".news", ".next", ".nextdirect", ".nexus", ".nf", ".nfl", ".ng", ".ngo", ".nhk", ".ni", ".nico", ".nike", ".nikon", ".ninja", ".nissan", ".nissay", ".nl", ".no", ".nokia", ".northwesternmutual", ".norton", ".now", ".nowruz", ".nowtv", ".np", ".nr", ".nra", ".nrw", ".ntt", ".nu", ".nyc", ".nz", ".obi", ".office", ".okinawa", ".olayan", ".olayangroup", ".ollo", ".om", ".omega", ".one", ".ong", ".onl", ".online", ".onyourside", ".ooo", ".oracle", ".orange", ".org", ".organic", ".orientexpress", ".origins", ".osaka", ".otsuka", ".ott", ".ovh", ".pa", ".page", ".pamperedchef", ".panasonic", ".panerai", ".paris", ".pars", ".partners", ".parts", ".party", ".passagens", ".pccw", ".pe", ".pet", ".pf", ".pfizer", ".pg", ".ph", ".pharmacy", ".philips", ".photo", ".photography", ".photos", ".physio", ".piaget", ".pics", ".pictet", ".pictures", ".pid", ".pin", ".ping", ".pink", ".pioneer", ".pizza", ".pk", ".pl", ".place", ".play", ".playstation", ".plumbing", ".plus", ".pm", ".pn", ".pnc", ".pohl", ".poker", ".politie", ".porn", ".post", ".pr", ".praxi", ".press", ".prime", ".pro", ".prod", ".productions", ".prof", ".progressive", ".promo", ".properties", ".property", ".protection", ".ps", ".pt", ".pub", ".pw", ".pwc", ".py", ".qa", ".qpon", ".quebec", ".quest", ".racing", ".re", ".read", ".realestate", ".realtor", ".realty", ".recipes", ".red", ".redstone", ".redumbrella", ".rehab", ".reise", ".reisen", ".reit", ".ren", ".rent", ".rentals", ".repair", ".report", ".republican", ".rest", ".restaurant", ".review", ".reviews", ".rexroth", ".rich", ".richardli", ".ricoh", ".rio", ".rip", ".ro", ".rocher", ".rocks", ".rodeo", ".room", ".rs", ".rsvp", ".ru", ".ruhr", ".run", ".rw", ".rwe", ".ryukyu", ".sa", ".saarland", ".safe", ".safety", ".sakura", ".sale", ".salon", ".samsung", ".sandvik", ".sandvikcoromant", ".sanofi", ".sap", ".sapo", ".sarl", ".sas", ".save", ".saxo", ".sb", ".sbi", ".sbs", ".sc", ".sca", ".scb", ".schaeffler", ".schmidt", ".scholarships", ".school", ".schule", ".schwarz", ".science", ".scor", ".scot", ".sd", ".se", ".seat", ".security", ".seek", ".select", ".sener", ".services", ".ses", ".seven", ".sew", ".sex", ".sexy", ".sfr", ".sg", ".sh", ".shangrila", ".sharp", ".shaw", ".shell", ".shia", ".shiksha", ".shoes", ".shop", ".shopping", ".shouji", ".show", ".shriram", ".si", ".silk", ".sina", ".singles", ".site", ".sj", ".sk", ".ski", ".skin", ".sky", ".skype", ".sl", ".sm", ".smart", ".smile", ".sn", ".sncf", ".so", ".soccer", ".social", ".softbank", ".software", ".sohu", ".solar", ".solutions", ".song", ".sony", ".soy", ".space", ".spiegel", ".spot", ".spreadbetting", ".sr", ".srl", ".ss", ".st", ".stada", ".staples", ".star", ".starhub", ".statebank", ".statefarm", ".statoil", ".stc", ".stcgroup", ".stockholm", ".storage", ".store", ".stream", ".studio", ".study", ".style", ".su", ".sucks", ".supplies", ".supply", ".support", ".surf", ".surgery", ".suzuki", ".sv", ".swatch", ".swiss", ".sx", ".sy", ".sydney", ".symantec", ".systems", ".sz", ".tab", ".taipei", ".talk", ".taobao", ".tatamotors", ".tatar", ".tattoo", ".tax", ".taxi", ".tc", ".tci", ".td", ".tdk", ".team", ".tech", ".technology", ".tel", ".telecity", ".telefonica", ".temasek", ".tennis", ".teva", ".tf", ".tg", ".th", ".thd", ".theater", ".theatre", ".tickets", ".tienda", ".tiffany", ".tips", ".tires", ".tirol", ".tj", ".tjmaxx", ".tjx", ".tk", ".tkmaxx", ".tl", ".tm", ".tmall", ".tn", ".to", ".today", ".tokyo", ".tools", ".top", ".toray", ".toshiba", ".total", ".tours", ".town", ".toyota", ".toys", ".tp", ".tr", ".trade", ".trading", ".training", ".travel", ".travelchannel", ".travelers", ".travelersinsurance", ".trust", ".trv", ".tt", ".tube", ".tui", ".tunes", ".tushu", ".tv", ".tvs", ".tw", ".tz", ".ua", ".ubs", ".ug", ".uk", ".um", ".unicom", ".university", ".uno", ".uol", ".ups", ".us", ".uy", ".uz", ".va", ".vacations", ".vana", ".vc", ".ve", ".vegas", ".ventures", ".verisign", ".versicherung", ".vet", ".vg", ".vi", ".viajes", ".video", ".vig", ".viking", ".villas", ".vin", ".vip", ".virgin", ".vision", ".vista", ".vistaprint", ".viva", ".vivo", ".vlaanderen", ".vn", ".vodka", ".volkswagen", ".vote", ".voting", ".voto", ".voyage", ".vu", ".vuelos", ".wales", ".walter", ".wang", ".wanggou", ".warman", ".watch", ".watches", ".weather", ".weatherchannel", ".webcam", ".weber", ".website", ".wed", ".wedding", ".weibo", ".weir", ".wf", ".whoswho", ".wien", ".wiki", ".williamhill", ".win", ".windows", ".wine", ".winners", ".wme", ".wolterskluwer", ".woodside", ".work", ".works", ".world", ".ws", ".wtc", ".wtf", ".xbox", ".xerox", ".xfinity", ".xihuan", ".xin", ".xperia", ".xxx", ".xyz", ".yachts", ".yahoo", ".yamaxun", ".yandex", ".ye", ".yodobashi", ".yoga", ".yokohama", ".you", ".youtube", ".yt", ".yun", ".za", ".zappos", ".zara", ".zero", ".zip", ".zippo", ".zm", ".zone", ".zuerich", ".zw"]
common_domains = [".com", ".org", ".edu", ".gov", ".uk", ".net", ".ca", ".de", ".au", ".us", ".ru", ".ch", ".it", ".nl", ".me", ".co"]
default_ips = ["92.242.140.2", "127.0.53.53", "45.79.222.138", "91.144.20.76", "88.198.29.97", "64.70.19.203", "46.242.144.130", "54.221.207.100", "208.73.210.204"]
def tld(username,ext):
	d("Trying a" + ext + "domain")
	try:
		ip = gethostbyname("www." + username + ext)
	except gaierror as e:
		d(e)
		ip = "127.0.53.53"
	if ip not in default_ips:
		sites.append("http://www." + username + ext)
def scrape_github(page):
	d("Interpreting GitHub page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	d("Splitting GitHub page")
	parts = soup.find_all("li", {"class" : "vcard-detail py-1 css-truncate css-truncate-target"})
	for part in parts:
		for div in part.find_all("div"):
			if len(div.contents[0]) is not 0:
				d("Gathering companies from GitHub")
				companies.append(div.contents[0])
		links = part.find_all("a")
		for link in links:
			if len(link.contents[0]) is not 0:
				d("Gathering emails from GitHub")
				if "@" in link.contents[0] and not ("http://" in link.contents[0] or "https://" in link.contents[0]):
					emails.append(link.contents[0])
				else:
					d("Gathering domains from GitHub")
					sites.append(link.contents[0])
		local_times = part.find_all("local-time")
		for local_time in local_times:
			d("Gathering GitHub events")
			if len(local_time.contents[0]) is not 0:
				events.append("Joined GitHub on " + local_time.contents[0])
	try:
		d("Gathering biographies from GitHub")
		bioparent = soup.find("div", {"class" : "user-profile-bio"})
		if bioparent is not None:
			bios.append(bioparent.contents[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering location from GitHub")
		locations.append(soup.find_all("li", {"aria-label" : "Home location"})[0].attrs["title"].strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			images.append(soup.find("img", {"class" : "avatar rounded-2"}).attrs["src"])
	except Exception as e:
		d(e)
def scrape_keybase(page):
	d("Gathering information from keybase")
	d("Interpreting Keybase page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering keys from Keybase")
		kparts = []
		odds = soup.find_all("span", {"class" : "odd"})
		evens = soup.find_all("span", {"class" : "even"})
		for even in evens:
			kparts.append(even.contents[0])
		for odd in odds:
			kparts.append(odd.contents[0])
		public_keys.append(kparts[0] + kparts[2] + kparts[1] + kparts[3])
	except Exception as e:
		d(e)
	links = soup.find_all("a", {"rel" : "me"})
	d("Gathering links from keybase")
	for link in links:
		if "twitter" in link.attrs["href"] or "github" in link.attrs["href"] or "reddit" in link.attrs["href"]:
			profiles.append("www." + link.attrs["href"].replace("https://", "").replace("http://", "").replace("www.", ""))
		else:
			sites.append(link.attrs["href"])
	try:
		d("Gathering bitcoin addresses from keybase")
		bitcoin_addresses.append(soup.find("a", {"class" : "currency-address view-currency-address"}).contents[0])
	except AttributeError as e:
		d(e)
	try:
		d("Gathering biographies from Keybase")
		bios.append(soup.find("div", {"class" : "bio"}).contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering locations from keybase")
		locations.append(soup.find_all("div", {"class" : "location"})[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			i_url = soup.find("div", {"class" : "picture"}).findChildren()[0].attrs["src"]
			if "no-photo" not in i_url:
				images.append(i_url)
	except Exception as e:
		d(e)
	try:
		if a.multiple is True:
			unames = soup.find_all("a", {"rel" : "me"})
			for uname in unames:
				usernames.append(uname.contents[0])
	except Exception as e:
		print(e)
def scrape_twitter(page):
	d("Gathering information from Twitter")
	d("Interpreting Twitter page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering real names from Twitter")
		real_names.append(soup.find("a", {"class" : "ProfileHeaderCard-nameLink u-textInheritColor js-nav\n"}).contents[0])
	except AttributeError as e:
		d(e)
	try:
		d("Gathering Twitter events")
		events.append("Joined Twitter on " + soup.find("span", {"class" : "ProfileHeaderCard-joinDateText js-tooltip u-dir"}).contents[0].replace("Joined ", ""))
	except AttributeError as e:
		d(e)
	try:
		d("Gathering locations from Twitter")
		locations.append(soup.find("span", {"class" : "ProfileHeaderCard-locationText u-dir"}).contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering sites from Twitter")
		sites.append(soup.find_all("a", {"rel" : "me nofollow", "class" : "u-textUserColor"})[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering biographies from Twitter")
		bios.append(soup.find("p", {"class" : "ProfileHeaderCard-bio u-dir"}).contents[0])
	except Exception as e:
		d(e)
	try:
		birthdays.append(soup.find_all("span", {"class" : "ProfileHeaderCard-birthdateText u-dir"})[0].findChildren()[0].contents[0].replace("Born on", "").strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			images.append(soup.find("img", {"class" : "ProfileAvatar-image u-bgUserColor"}).attrs["src"])
	except Exception as e:
		d(e)
def scrape_youtube(page):
	d("Gathering information from YouTube")
	d("Interpreting YouTube page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering real names from YouTube")
		real_names.append(soup.find_all("a", {"class" : "spf-link branded-page-header-title-link yt-uix-sessionlink"})[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			images.append(soup.find("img", {"class" : "channel-header-profile-image"}).attrs["src"].strip())
	except Exception as e:
		d(e)
def scrape_myspace(page):
	d("Gathering information from MySpace")
	d("Interpreting MySpace page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering locations from MySpace")
		locations.append(soup.find_all("div", {"class" : "location_white location "})[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
				images.append(soup.find("a", {"id" : "profileImage"}).findChildren()[1].attrs["src"].strip())
	except Exception as e:
		d(e)
def scrape_medium(page):
	d("Gathering information from Medium")
	d("Interpreting Medium page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering real names from Medium")
		real_names.append(soup.find_all("a", {"dir" : "auto"})[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			images.append(soup.find("img", {"class" : "avatar-image u-size100x100 u-xs-size80x80 imagePicker-target"}).attrs["src"].strip())
	except Exception as e:
		d(e)
def scrape_aboutme(page):
	d("Gathering information from About.me")
	d("Interpreting About.me page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering biographies from About.me")
		bios.append(soup.find_all("p")[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering real names from About.me")
		real_names.append(soup.find_all("h1")[0].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering images from About.me")
		if a.images is True:
			i_url = soup.find("div", {"class" : "image"}).attrs["style"].split("(")[1].split(")")[0].strip()
			if "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+Cjxzdmcgd2lkdGg9IjkyMXB4IiBoZWlnaHQ9IjYxNHB4IiB2aWV3Q" not in i_url:
				images.append(i_url)
	except Exception as e:
		d(e)
	try:
		d("Gathering other usernames from About.me")
		if a.multiple is True:
			social_links = soup.find_all("a", {"class" : "social-link"})
			for social_link in social_links:
				if "twitter.com" in social_link.attrs["href"] or "flickr.com" in social_link.attrs["href"] or "youtube.com" in social_link.attrs["href"] or "instagram.com" in social_link.attrs["href"]:
					if len(social_link.attrs["href"].split("/")[-1]) < 1:
						usernames.append(social_link.attrs["href"].split("/")[-2])
					else:
						usernames.append(social_link.attrs["href"].split("/")[-1])
	except Exception as e:
		d(e)
	try:
		lnks = soup.find_all("a", {"target" : "_blank", "rel" : "noopener noreferrer"})
		for lnk in lnks:
			if "discover" in lnk.attrs["href"]:
				j.append(lnk.attrs["href"].split("/")[-1])
	except Exception as e:
		d(e)
def scrape_deivant(page):
	d("Gathering information from DeviantArt")
	d("Interpreting DeviantArt page")
	countries = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname", "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic", "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering real names from DeviantArt")
		real_names.append(soup.find_all("title")[0].contents[0].split("(")[1].split(")")[0].strip())
	except Exception as e:
		d(e)
	classifiers = soup.find_all("dd", {"class" : "f h"})[0].contents[0].split("/")
	for classifier in classifiers:
		if "Male" in classifier:
			d("Gathering genders from DeviantArt")
			genders.append(classifier)
		if "Female" in classifier:
			d("Gathering genders from DeviantArt")
			genders.append(classifier)
		if classifier in countries:
			d("Gathering locations from DeviantArt")
			locations.append(classifier)
		try:
			d("Gathering ages from DeviantArt")
			age = int(classifier)
			ages.append(str(age))
		except ValueError as e:
			d(e)
		try:
			if a.images is True:
				images.append(soup.find("img", {"class" : "avatar float-left"}).attrs["src"].strip())
		except Exception as e:
			d(e)
def scrape_flickr(page):
	d("Gathering information from Flickr")
	d("Interpreting Flickr page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	try:
		d("Gathering locations from Flickr")
		locations.append(soup.find_all("div", {"class" : "metadata-content"})[0].findChildren()[1].contents[0].strip())
	except Exception as e:
		d(e)
	try:
		d("Gathering Flickr Events")
		events.append(soup.find_all("div", {"class" : "metadata-content"})[0].findChildren()[2].contents[0].replace("Joined", "Joined Flickr in"))
	except Exception as e:
		d(e)
	try:
		if a.images is True:
			images.append(soup.find("div", {"class" : "avatar no-menu person large no-edit"}).attrs["style"].split("(")[1].split(")")[0].strip())
	except Exception as e:
		d(e)
def scrape_etsy(page):
	d("Gathering information from Etsy")
	d("Interpreting Etsy page")
	doc = page.read().decode("UTF-8")
	soup = BeautifulSoup(doc, "lxml")
	children = soup.find("ul", {"class" : "extra wrap"}).findChildren()
	for child in children:
		try:
			if "Female" in child.contents[0]:
				d("Gathering genders from Flickr")
				genders.append("Female")
			if "Male" in child.contents[0]:
				d("Gathering genders from Flickr")
				genders.append("Male")
			if "Joined" in child.contents[0]:
				d("Gathering Flickr events")
				events.append(child.contents[0].replace("Joined", "Joined Etsy on ").replace(" ", ""))
			if "Born on" in child.contents[0]:
				d("Gathering birthdays from Flickr")
				birthdays.append(child.contents[0].replace("Born on", "").strip())
		except Exception as e:
			d(e)
	try:
		if a.images is True:
			i_url = soup.find("img", {"class" : "user-avatar-circle-img user-avatar-external"}).attrs["src"].strip()
			if "default_avatar" not in i_url:
				images.append(i_url)
	except Exception as e:
		d(e)
def u(username):
	if username not in i:
		try:
			d("Scanning GitHub")
			page = urlopen("http://www.github.com/" + username)
			profiles.append("www.github.com/" + username)
			profiles.append("http://gist.github.com/" + username)
			accounts.append("GitHub")
			try:
				scrape_github(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning Keybase")
			page = urlopen("https://keybase.io/" + username)
			profiles.append("www.keybase.io/" + username)
			accounts.append("Keybase")
			try:
				scrape_keybase(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning Twitter")
			page = urlopen("https://twitter.com/" + username)
			profiles.append("www.twitter.com/" + username)
			accounts.append("Twitter")
			try:
				scrape_twitter(username)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning Reddit")
			page = urlopen("https://reddit.com/user/" + username)
			profiles.append("www.reddit.com/user/" + username)
			accounts.append("Reddit")
		except HTTPError as e:
			d(e)
		try:
			d("Scanning YouTube")
			page = urlopen("https://youtube.com/user/" + username)
			profiles.append("www.youtube.com/user/" + username)
			accounts.append("YouTube")
			try:
				scrape_youtube(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning MySpace")
			page = urlopen("https://myspace.com/" + username)
			profiles.append("www.myspace.com/" + username)
			accounts.append("MySpace")
			try:
				scrape_myspace(page)
			except Exception as e:
				d(e)
		except HTTPError:
			pass
		try:
			d("Scanning Tumblr")
			page = urlopen("https://" + username + ".tumblr.com")
			profiles.append("www." + username.replace(".", "") + ".tumblr.com")
			accounts.append("Tumblr")
		except Exception as e:
			d(e)
		d("Creating proxy headers")
		headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"}
		try:
			d("Scanning Medium")
			request = Request("https://medium.com/@" + username,None,headers)
			page = urlopen(request)
			profiles.append("www.medium.com/@" + username)
			accounts.append("Medium")
			try:
				scrape_medium(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning About.me")
			page = urlopen("https://about.me/" + username)
			profiles.append("www.about.me/" + username)
			accounts.append("About.me")
			try:
				scrape_aboutme(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning DeviantArt")
			page = urlopen("http://" + username + ".deviantart.com")
			profiles.append("www." + username + ".deviantart.com")
			accounts.append("DeviantArt")
			try:
				scrape_deivant(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning Flickr")
			page = urlopen("http://www.flickr.com/photos/" + username)
			profiles.append("www.flickr.com/photos/" + username)
			accounts.append("Flickr")
			try:
				scrape_flickr(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		try:
			d("Scanning Etsy")
			page = urlopen("https://www.etsy.com/people/" + username)
			profiles.append("www.etsy.com/people/" + username)
			accounts.append("Etsy")
			try:
				scrape_etsy(page)
			except Exception as e:
				d(e)
		except HTTPError as e:
			d(e)
		if a.full is True:
			d("Scanning all domains")
			for domain in domains:
				tld(username,domain)
		else:
			d("Scanning common domains")
			for domain in common_domains:
				tld(username,domain)
	i.append(username)
def douglas_county(name):
	d("Creating preferences")
	profile = FirefoxProfile()
	profile.set_preference("browser.download.dir", getcwd())
	profile.set_preference("browser.download.defaultFolder", getcwd())
	profile.set_preference("browser.download.panel.shown", False)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting", False)
	profile.set_preference("browser.helperApps.alwaysAsk.force", False)
	d("Opening Firefox driver")
	driver = Firefox(firefox_profile = profile)
	d("Navigating to the Douglas County Assessor")
	driver.get("http://douglascone.wgxtreme.com/?d=1")
	d("Navigating to advanced tabs")
	driver.find_elements_by_class_name("x-tab-right")[2].click()
	inputElement = driver.find_element_by_name("owner_name_searchA")
	d("Typing name")
	inputElement.send_keys(name)
	sleep(5)
	d("Searching")
	driver.find_element_by_xpath("//*[@id='ext-gen300']").click()
	sleep(4)
	d("Processing source code")
	s = driver.page_source
	soup = BeautifulSoup(s, "lxml")
	potentials = soup.find_all("div", {"class" : "x-grid3-cell-inner"})
	found = False
	def narrow(name, address):
		d("Creating new profile")
		profile2 = FirefoxProfile()
		profile2.set_preference("network.cookie.cookieBehavior", 2)
		d("Opening new Firefox")
		driver2 = Firefox(firefox_profile=profile2)
		if a.images is True:
			d("Finding home")
			driver2.get("https://www.google.com/maps/place/" + address.replace(" ", "+"))
			sleep(2)
			d("Selecting home image")
			driver2.find_element_by_class_name("widget-pane-section-header-hero").click()
			sleep(6)
			d("Minimizing menu")
			driver2.find_element_by_class_name("widget-expand-button-label").click()
			sleep(2)
			d("Maximizing window")
			driver2.maximize_window()
			sleep(1)
			d("Saving screenshot")
			driver2.save_screenshot("house.png")
			h.append("file:///" + getcwd().replace("\\\\", "/") + "/house.png")
		driver2.get("https://www.google.com/maps/dir/" + address.replace(" ", "+") + ",+Omaha,+NE/Millard+West+High+School,+5710+South+176th+Avenue,+Omaha,+NE+68135")
		sleep(3)
		d("Processing source code")
		s = driver2.page_source
		soup = BeautifulSoup(s, "lxml")
		times = soup.find_all("div", {"class" : "widget-pane-section-directions-trip-duration"})
		time_ints = []
		returns = []
		d("Finding shortest travel time")
		for time in times:
			try:
				time_ints.append(int(time.contents[1].contents[0].replace(" min", "")))
			except IndexError:
				time_ints.append(int(time.contents[0].replace(" min", "")))
		driver2.close()
		return min(time_ints)
	names = []
	addresses = []
	d("Interating over potential names")
	for n in range(len(potentials)):
		if n % 8 is 1:
			names.append(potentials[n].contents[0])
		elif n % 8 is 2:
			addresses.append(potentials[n].contents[0])
	close = []
	for x in range(len(names)):
		y = narrow(names[x], addresses[x])
		if y < 20:
			close.append(names[x])
	matches = []
	d("Finding name")
	for clos in close:
		matches.append(driver.find_element_by_xpath("//*[(text()='" + clos + "')]"))
	for match in matches:
		match.click()
		d("Selecting entry")
		sleep(4)
		download_pdf = driver.find_element_by_class_name("tb_pdf").click()
		sleep(4)
		d("Downloading and checking pdf")
		if not getsize("output.pdf") > 0:
			remove("output.pdf")
		else:
			rename("output.pdf", name + ".pdf")
			g.append(name + ".pdf")
			found = True
	driver.close()
	return found
def display(html):
	d("Accessing result data")
	global accounts, real_names, companies, locations, emails, sites, bios, public_keys, bitcoin_addresses, sites, genders, ages, birthdays, profiles, j, g
	d("Removing duplicate data")
	accounts = list(set(accounts))
	real_names = list(set(real_names))
	companies = list(set(companies))
	locations = list(set(locations))
	emails = list(set(emails))
	sites = list(set(sites))
	bios = list(set(bios))
	public_keys = list(set(public_keys))
	bitcoin_addresses = list(set(bitcoin_addresses))
	sites = list(set(sites))
	genders = list(set(genders))
	ages = list(set(ages))
	birthdays = list(set(birthdays))
	profiles = list(set(profiles))
	j = list(set(j))
	profile_links = []
	for profile in profiles:
		if "http://" in profile:
			profile_links.append(profile)
		elif "https://" in profile:
			profile_links.append(profile.replace("https://", "http://"))
		else:
			profile_links.append("http://" + profile)
	if html is True:
		d("Opening HTML file")
		html_clearing = open("sengineered.html", "w")
		html_clearing.write("")
		html_clearing.close()
		html_writer = open("sengineered.html", "a")
		html_writer.write("<!DOCTYPE html><html><head><title>" + a.username + "</title></head><body style='text-align:center;'><h2 style='text-align:center;'>Images</h2>")
		if a.images is True:
			d("Writing images")
			if len(images) > 0:
				for image in images:
					html_writer.write("<img style='color:black;' height='200' width='200' src='" + image + "' alt='Collected Image' />")
		else:
			d("Skipping images")
			html_writer.write("<p>Program was set not to select images.</p>")
		if len(h) > 0:
			d("Writing header image")
			html_writer.write("<img style='color:black;' height='600' width='1600' src='" + h[0] + "' alt='Header Image' /><br>")
		html_writer.write("<hr><h2>Accounts:</h2>")
		d("Writing accounts")
		for account in accounts:
			if len(account) is not 0:
				html_writer.write("<p>" + account + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Websites</h2>")
		d("Writing websites")
		for site in sites:
			if len(site) is not 0:
				html_writer.write("<p>" + site + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Names</h2>")
		d("Writing real names")
		for real_name in real_names:
			if len(real_name) is not 0:
				html_writer.write("<p>" + real_name + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Companies</h2>")
		d("Writing companies")
		for company in companies:
			if len(company) is not 0:
				html_writer.write("<p>" + company + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Locations</h2>")
		d("Writing locations")
		for location in locations:
			if len(location) is not 0:
				html_writer.write("<p>" + location + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Emails</h2>")
		d("Writing emails")
		for email in emails:
			if len(email) is not 0:
				html_writer.write("<p>" + email + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Interests</h2>")
		d("Writing interests")
		for interest in j:
			if len(interest) is not 0:
				html_writer.write("<p>" + interest + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Descriptions</h2>")
		d("Writing biographies")
		for bio in bios:
			if len(bios) is not 0:
				html_writer.write("<p>" + bio + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>PGP Keys</h2>")
		d("Writing public keys")
		for key in public_keys:
			if len(key) is not 0:
				html_writer.write("<p>" + key + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Bitcoin</h2>")
		d("Writing bitcoin addresses")
		for address in bitcoin_addresses:
			if len(address) is not 0:
				html_writer.write("<p>" + address + "</p>")
		html_writer.write("<hr><h2>Gender</h2>")
		d("Writing genders")
		for gender in genders:
			if len(gender) is not 0:
				html_writer.write("<p>" + gender + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Age</h2>")
		d("Writing ages")
		for age in ages:
			if len(age) is not 0:
				html_writer.write("<p>" + age + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Birthdays</h2>")
		d("Writing birthdays")
		for birthday in birthdays:
			if len(birthday) is not 0:
				html_writer.write("<p>" + birthday + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Events</h2>")
		d("Writing events")
		for event in events:
			if len(event) is not 0:
				html_writer.write("<p>" + event + "</p>")
		html_writer.write("<hr><h2 style='text-align:center;'>Links</h2>")
		d("Writing links")
		for profile_link in profile_links:
			if len(profile_link) is not 0:
				html_writer.write("<a href='" + profile_link + "' target='_blank'>" + profile_link + "</a><br>")
		for pdf in g:
			print(pdf)
			html_writer.write("<br><br><div style='width:100%;text-align:center;'><iframe style='margin-left:auto;margin-right:auto;' src='" + pdf + "' width='90%' height='700'></iframe>")
		html_writer.write("<p>Thomas Gerot<br>Social Engineering with Python<br>Millard West High School Computer Science Club</p></body></html>")
		d("Closing HTML file")
		html_writer.close()
		# if a.pdf is True:
		# 	with open("sengineered.html") as f:
		# 		from_file(f, "sengineered.pdf")
		webbrowser.open("file://" + realpath("sengineered.html"))
	else:
		d("Printing data")
		print("Accounts:")
		for account in accounts:
			if len(account) is not 0:
				print("\t - " + account)
		print("Websites:")
		for site in sites:
			if len(site) is not 0:
				print("\t- " + site)
		print("Names:")
		for real_name in real_names:
			if len(real_name) is not 0:
				print("\t- " + real_name)
		print("Companies:")
		for company in companies:
			if len(company) is not 0:
				print("\t- " + company)
		print("Locations:")
		for location in locations:
			if len(location) is not 0:
				print("\t- " + location)
		print("Emails:")
		for email in emails:
			if len(email) is not 0:
				print("\t- " + email)
		print("Interests:")
		for interest in j:
			if len(interest) is not 0:
				print("\t- " + interest)
		print("Descriptions:")
		for bio in bios:
			if len(bio) is not 0:
				print("\t- " + bio)
		print("PGP Keys:")
		for key in public_keys:
			if len(key) is not 0:
				print("\t- " + key)
		print("Bitcoin:")
		for address in bitcoin_addresses:
			if len(address) is not 0:
				print("\t- " + address)
		print("Events:")
		for event in events:
			if len(event) is not 0:
				print("\t- " + event)
		print("Gender:")
		for gender in genders:
			if len(gender) is not 0:
				print("\t- " + gender)
		print("Age:")
		for age in ages:
			if len(age) is not 0:
				print("\t- " + age)
		print("Birthdays:")
		for birthday in birthdays:
			if len(birthday) is not 0:
				print("\t- " + birthday)
		print("Links:")
		for profile_link in profile_links:
			if len(profile_link) is not 0:
				print("\t- " + profile_link)
if __name__ == "__main__":
	try:
		print("Scanning")
		ti = time()
		u(a.username)
		for username in usernames:
			u(username)
		for root, dirs, files in walk(getcwd()):
			for currentFile in files:
				exts = (".pdf")
				if any(currentFile.lower().endswith(ext) for ext in exts):
					remove(join(root, currentFile))
		if a.douglas is True:
			real_names = list(set(real_names))
			for real_name in real_names:
				found = False
				if len(real_name.split(" ")) is 2:
					found = douglas_county(real_name)
				if found is not True:
					douglas_county(real_name.split(" ")[-1])
		tf = time()
		print("Scan time: " + str(round(tf - ti, 3)) + " seconds")
		display(a.webpage)
		if a.links is True:
			d("Opening links")
			for profile in profiles:
				webbrowser.open(profile)
		d("Exiting")
		exit()
	except KeyboardInterrupt:
		print("\nUser halted the program.")
