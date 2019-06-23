# Ultra Path

This module is made out of a simple C extension to help reduce the total time required to extract items from highly 
nested structures. At the moment it supports retrieving items from nested structures made out of dictionaries and lists 
but it can be easily extended to support other mappings or iterables. 

**Usage:**

`>>> from upath import getp`

`>>> getp({"level0": {"level1": [{"level3": 3}]}}, "level0.level1.0.level3")
3`

`>>> getp({"level0": {"level1": [{"level3": 3}]}}, "level0/level1/0/level3", '/', None)
3`

`>>> getp({"level0": {"level1": [{"level3": 3}]}}, "level0/level1/0/level77777777", '/', "Default value")
'Default value'`

Only positional arguments are supported, so this will not work: 

`>>> getp({"level0": {"level1": [{"level3": 3}]}}, "level0/level1/0/level3", default='Works')
None`

Check C extensions documentation here: 
https://docs.python.org/3/extending/