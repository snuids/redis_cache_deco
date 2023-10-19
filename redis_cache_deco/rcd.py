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
            for kwarg in kwargs:
                finalhash+=hash(str(kwarg)+str(kwargs[kwarg]))
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

# from datetime import datetime
# import redis
# #from redis_cache_deco import rcd

# init_redis_cache(redis.Redis(host='localhost', port=6379, db=0))

# @use_redis_cache(ttl=60)
# def my_function(dt,array):
#     print("My Function")
#     return {"dt":dt,"array":array,"ret":"OK"}

# @use_redis_cache(ttl=60)
# def my_function2(user="toto"):
#     print("My Function")
#     return {"user":user}


# res=my_function(datetime(2021,1,1,1,1),[{"a":1}])
# print(res)
# res=my_function2(user="tata")
# print(res)
# res=my_function2(user="titi")
# print(res)
# res=my_function2(user="toto")
# print(res)
# res=my_function2(user="tata")
# print(res)
# res=my_function2(user="titi")
# print(res)
# res=my_function2(user="toto")
# print(res)


# print(cache_stats())