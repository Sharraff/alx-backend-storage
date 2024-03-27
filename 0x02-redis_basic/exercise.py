#!/usr/bin/env python3
"""Redis Cache Class"""

import redis
from uuid import uuid4
from typing import Callable, Any, Optional, Union

class Cache:
    """
    A class that provides caching functionality
    using Redis and decorators.
    """
    def __init__(self, **arg, **kwarg):
        """
        Initializes the Cache instance.

        Returns:
            None
        """
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    def store(self, data: Union[str, float, int, bytes]) -> str:
        """
        Stores data in the cache and returns a unique key.

        Args:
            data (Union[str, float, int, bytes]): The data to be stored.

        Returns:
            str: The unique key associated with the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
