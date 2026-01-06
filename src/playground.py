import re

def main():
    s =  "1.  This is text with a link 2. [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)\n"
    
    res = s.split("2. ", maxsplit= 1)
    print(res)


if __name__ == "__main__":
    main()