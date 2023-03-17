"""Stores usefull tools and magic"""
import json


def serialize_everything(obj):
    d1 = {}
    for attr, val in obj.__dict__.items():
        if callable(val):
            continue
        try:
            json.dumps({attr: val})
            d1[attr] = val
        except TypeError:

            if hasattr(val, "__dict__"):
                d1[attr] = serialize_everything(val)
            elif isinstance(val, list) or isinstance(val, set):
                d1[attr] = [serialize_everything(v1) for v1 in val]
            else:
                d1[attr] = str(val)
        except Exception:
            print(f"key={attr} val={val} were not serialized")
    return d1


def get_cleared_dict(d1: dict):
    return {k: v for k, v in d1.items() if k is not None}

