import re
from textnodeParsing import extract_regular_links_first_occurence

def main():
    s =  "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    matches = extract_regular_links_first_occurence(s)

    print(matches.group(0))

    testDict = {}

    print(testDict.get("hellp", None))


if __name__ == "__main__":
    main()