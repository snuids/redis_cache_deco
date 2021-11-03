# Redis Cache Deco

## Installation

```bash
pip install redis-cache-deco
```

# Example

```python
from redis_cache_deco import rcd

rcd.init_redis_cache(redis.Redis(host='localhost', port=6379, db=0))

@rcd.use_redis_cache(ttl=60)
def my_function(dt,array):
    print("My Function")
    return {"dt":dt,"array":array,"ret":"OK"}

res=my_function(datetime(2021,1,1,1,1),[{"a":1}])
print(res)


rcd.cache_stats()
```
