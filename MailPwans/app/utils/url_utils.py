from tld import get_tld 
from urllib.parse import urlparse 
from googlesearch import search 
import re
import pandas as pd

def google_index(url):
    site = search(url, 5)
    return 1 if site else 0

def having_ip_address(url: str) -> int:
    return 1 if re.search(r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])', url) else 0

def abnormal_url(url):
    hostname = str(urlparse(url).hostname)
    return 1 if re.search(hostname, url) else 0

def suspicious_words(url):
    return 1 if re.search(r'PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr', url) else 0

def shortening_service(url):
    return 1 if re.search(r'bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co', url) else 0

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['hostname_length'] = len(urlparse(url).netloc)
    features['count-www'] = url.count('www')
    features['count-https'] = url.count('https')
    features['count-http'] = url.count('http')
    features['count.'] = url.count('.')
    features['count%'] = url.count('%')
    features['count?'] = url.count('?')
    features['count-'] = url.count('-')
    features['count='] = url.count('=')
    features['count@'] = url.count('@')
    features['count_dir'] = urlparse(url).path.count('/')
    features['count_embed_domian'] = urlparse(url).path.count('//')
    features['short_url'] = shortening_service(url)
    features['fd_length'] = len(urlparse(url).path.split('/')[1]) if len(urlparse(url).path.split('/')) > 1 else 0
    tld = get_tld(url, fail_silently=True)
    features['tld_length'] = len(tld) if tld else -1
    features['sus_url'] = suspicious_words(url)
    features['count-digits'] = sum(c.isdigit() for c in url)
    features['count-letters'] = sum(c.isalpha() for c in url)
    features['abnormal_url'] = abnormal_url(url)
    features['use_of_ip_address'] = having_ip_address(url)
    features['google_index'] = google_index(url)
    return features