import os
import importlib


for module in os.listdir("./modules"):
    if module.startswith("__"):
        continue
    importlib.import_module(f"modules.{module}")
