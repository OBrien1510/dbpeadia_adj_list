import json

a = {"1":2,"2":2,"3":2}

with open("test.json", 'w+') as file:

    json.dump(a, file)