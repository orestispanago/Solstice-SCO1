import yaml
from box import Box


with open("configs/trace.yaml", "r") as ymlfile:
    trace = Box(yaml.safe_load(ymlfile))