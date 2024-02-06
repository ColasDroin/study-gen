import os

# Get a dictionnary of blocks
dict_ref_blocks = {}
for module in os.listdir(os.path.dirname(__file__)):
    if module != "__init__.py" and module[-3:] == ".py":
        module_name = "_".join(module.split("_")[1:])[:-3]
        module_filename = module[:-3]
        dict_ref_blocks[module_name] = getattr(
            __import__(f"blocks.{module_filename}", fromlist=[module_filename]),
            module_name,
        )
