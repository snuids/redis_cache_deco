#from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'redis_cache_deco',
  packages = ['redis_cache_deco'], # this must be the same as the name above
  version = '1.0.0',
  description = 'A decorator that memoized into redis',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'snuids',
  author_email = 'snuids@mannekentech.com',
  url = 'https://github.com/snuids/redis_cache_deco', 
  download_url = 'https://github.com/snuids/redis_cache_deco/archive/1.0.0.tar.gz',
  keywords = ['Python', 'memoize', 'decorator','redis'], # arbitrary keywords
  classifiers = [],
)
