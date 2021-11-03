import redis
import pickle
from functools import wraps
from datetime import date, datetime

cache_hits_perfunction={}
redis_client=None

#---------------------------------------------------------------------------
# INIT
#---------------------------------------------------------------------------
def init_redis_cache(redis_client_in):
    global redis_client,cache_hits_perfunction
    redis_client=redis_client_in
    cache_hits_perfunction={}

#---------------------------------------------------------------------------
# DECORATOR
#---------------------------------------------------------------------------
def use_redis_cache(*roles,ttl=60):
    def wrapper(f):        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            global redis_client,cache_hits_perfunction
            finalhash=0
            for arg in args:
                finalhash+=hash(str(arg))
            key=f'{f.__name__}_{finalhash}'
            
            red_obj=redis_client.get(key)
            
            if not f.__name__ in cache_hits_perfunction:
                cache_hits_perfunction[f.__name__]={"Hits":0,"Misses":0}
            
            if red_obj==None:
                ret= f(*args, **kwargs)   
                print(ret)
                redis_client.set(key,pickle.dumps(ret),ex=ttl)
                cache_hits_perfunction[f.__name__]["Misses"]+=1
            else:
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