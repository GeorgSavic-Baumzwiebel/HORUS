import os
from pathlib import Path
import pdoc
from setuptools import command

here = Path(__file__).parent

for each in os.listdir(here.parent):
    if each.endswith(".py") and each.__str__() != "setup.py":
        print(f"../{each.__str__()}")
        pdoc.pdoc(
            f"../{each.__str__()}",
            output_directory=here / "docs"
        )

