import os

# Get a dictionnary of blocks
dict_ref_blocks = {}
for module in os.listdir(os.path.dirname(__file__)):
    if module != "__init__.py" and module[-3:] == ".py":
        module_name = module[:-3]
        dict_ref_blocks[module_name] = getattr(
            __import__(f"blocks.{module[:-3]}", fromlist=[module[:-3]]), module[4:-3]
        )
