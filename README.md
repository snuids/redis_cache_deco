# Redis Cache Decorator

## Installation

```bash
pip install redis-cache-deco
```

# Example

```python
from datetime import datetime
import redis
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

## parameters

init_redis_cache(redis_client_in,prefix_in="",debug_in=False)

* prefix_in: The prefix to use in redis
* debug_in: Bypass the redis cache


