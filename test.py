import re

string = "Category:Teaching hospitals in Pakistan"

pattern = re.compile("Category:(.+)")

m = pattern.match(string)

print(m)
