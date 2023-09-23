import re
import sys

my_file = open(sys.argv[1], 'r')
for line in my_file:
    tmp = line.replace("'","\"").replace("\\","").rstrip().replace("@- << EOF","").replace("EOF","")
    if re.search('".*://.*/.*"', tmp):
        URL=re.search('".*://.*/.*"', tmp).group(0)
        print(re.sub('".*://.*/.*"','', tmp), "^")
    elif re.search('-d', tmp):
        print(URL, "-d \"^")
    elif tmp=="}":
        print(tmp, "\"")
    elif tmp=="":
        pass
    else:
        print(tmp, "^")
