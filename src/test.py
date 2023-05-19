import json

data = {"a": "world", "b": "bar"}
out = "one,two,three,"
print(out+",".join(data.values()))