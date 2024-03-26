#!/usr/bin/env python3
"""Python function that inserts a new
document in a collection based on kwargs"""
from typing import Any
from pymongo import collection


def insert_school(mongo_collection: collection, **kwargs: Any) -> str:
    """inserts a new
    document in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id