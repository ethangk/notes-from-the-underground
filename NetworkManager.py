import urllib
from requests import get
from requests.exceptions import RequestException
import os.path
from contextlib import closing

CACHE_DIR = "./cache"

# I've pulled the first few functions in this file from a tutorial on web scraping in Python
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def path_to_filename(path):
  return path.split('/')[-1] + ".html"


def generate_file_path(path):
  parsed_path = path_to_filename(path)
  return CACHE_DIR + "/" + parsed_path

def cached_file_exists(path):
  expected_file_path = generate_file_path(path)
  return (os.path.isfile(expected_file_path), expected_file_path)

def fetch_and_cache(host, path):
  content = simple_get(host + path)
  open(generate_file_path(path), "w").write(str(content))
  return content

# Running this over and over again without caching became a bottleneck very quickly
# This attempts to read from the cached version, and fetches+caches the page if not
def fetch(host, path):
  (file_exists, file_path) = cached_file_exists(path)
  if (file_exists):
    # file exists, load from the cache
    return open(file_path).read()
  else:
    return fetch_and_cache(host, path)
