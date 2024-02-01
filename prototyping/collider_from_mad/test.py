# %%
from blocks import dict_ref_blocks

from study_gen import StudyGen

# %%
study = StudyGen(
    path_configuration="config.yaml", path_master="master.yaml", dict_ref_blocks=dict_ref_blocks
)

# %%
l_gen = study.generate_all()
for gen in l_gen:
    print(gen)

# %%
