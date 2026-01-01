import re

def main():
    s =  "## This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)\n"
    
    print(s.split("## "))


if __name__ == "__main__":
    main()