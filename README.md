# yolotask

#### Structure:
- yolotask/server.py - FastAPI app
- yolotask/models.py - Pydantic request/response models
- yolotask/config.py - Pydantic settings
- yolotask/utils/stats.py - functions for metric calculations
- yolotask/db/redis_storage.py - aioredis wrapper

#### Implementation details:
I have chosen redis as a key-value storage because it naturally fits counting requests and impressions. Counters don't use much memory so this should scale to a large number of users (just as async FastAPI app).

I decided to do aggregations in GetStats with process pool as I supposed that this is not a frequent operation and reponse time is less important (e.g we check stats few times a day).

SQL storage such as Postgres could also be a viable solution, but would probably require a little more effort and some kind of task queue (or just creating tasks without awaiting the result) for GetAd and Impression. It also fits better for frequent aggregations.

It is also worth mentioning that GetAd is a POST method (has body) for API to be REST-compliant and should probably be renamed. Request body fields should also be renamed, I handled this with aliases (see yolotask/models.py).

#### Commands
Running:    
- make build
- make start

Stopping:    
- make stop

Testing:    
- make test

