import redis
import pickle
import logging
from functools import wraps
from datetime import date, datetime

cache_hits_perfunction={}
redis_client=None
prefix=""
debug=False
logger=logging.getLogger("rcd")

#---------------------------------------------------------------------------
# INIT
#---------------------------------------------------------------------------
def init_redis_cache(redis_client_in,prefix_in="",debug_in=False):
    global redis_client,cache_hits_perfunction,prefix,debug
    redis_client=redis_client_in
    cache_hits_perfunction={}
    prefix=prefix_in
    debug=debug_in

#---------------------------------------------------------------------------
# DECORATOR
#---------------------------------------------------------------------------
def use_redis_cache(*roles,ttl=60):
    def wrapper(f):        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            global redis_client,cache_hits_perfunction,prefix,debug
            finalhash=0
            for arg in args:
                finalhash+=hash(str(arg))
            key=f'{prefix}{f.__name__}_{finalhash}'
            
            if debug:
                red_obj=None
            else:
                red_obj=redis_client.get(key)
            
            if not f.__name__ in cache_hits_perfunction:
                cache_hits_perfunction[f.__name__]={"Hits":0,"Misses":0}
            
            if red_obj==None:
                ret= f(*args, **kwargs)     
                logger.debug("Not In Cache Calling:"+f.__name__)
                redis_client.set(key,pickle.dumps(ret),ex=ttl)
                cache_hits_perfunction[f.__name__]["Misses"]+=1
            else:
                logger.debug("In Cache Returning:"+f.__name__)
                cache_hits_perfunction[f.__name__]["Hits"]+=1
                ret=pickle.loads(red_obj)
            return ret
        return decorated_function
    return wrapper

#---------------------------------------------------------------------------
# Stats
#---------------------------------------------------------------------------
def cache_stats():
    return cache_hits_perfunction