#!/usr/bin/env python3
"""Redis Cache Class"""

import redis
from uuid import uuid4
from functools import wraps
from typing import Callable, Any, Optional, Union


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a function is called
    and increments the count in Redis.

    Args:
        mwthod (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapper function.
    """
    key = method.__qualname__
    
    @wraps(method)
    def wrapper(*args: Any, **kargs: Any) -> Any:
        """
        Wrapper function that increments the call count
        and calls the original function.

        Args:
            self: Instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: Result of the original function call.
        """
        self.__redis.incr(key)
        return method(*args, **kargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that records the inputs and outputs
    of a function call in Redis.

    Args:
        f (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapper function.
    """
    @wrapper(method)
    def wrapper(self, *args, **kwarg):
        """
        Wrapper function that records function inputs
        and outputs in Redis and calls the original function.

        Args:
            self: Instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: Result of the original function call.
        """
        in_key = f'{method.__qualname__}:inputs'
        out_key = f'{method.__qualname__}:outputs'
        self._redis.rpush(in_key, str(*args))
        output = method(self, *args)
        self._redis.rpush(out_key, output)
        return output
      return wrapper



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


    @call_history
    @count_calls
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

    def get(self, key: str,
      fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        """
        value = self._redis.get(key)

        if fn:
          return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from the cache using the given key.

        Args:
            key (str): The key associated with the cached string.

        Returns:
            str: The retrieved string value.
        """
        return self.get(key, fn=lambda v: v.decode('utf-8'))

    def get_int(self, key: str) -> int:
      """
      Retrieves an integer value from the cache using the given key.

      Args:
          key (str): The key associated with the cached integer.

      Returns:
          int: The retrieved integer value.
      """
      return self.get(key, fn=lambda v: int(v))
