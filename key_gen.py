import argparse
import random
import hashlib
from colorama import Fore


ERROR = Fore.RESET + "[" + Fore.RED + "!" + Fore.RESET + "] "
OK = Fore.RESET + "[" + Fore.GREEN + "+" + Fore.RESET + "] "


parser = argparse.ArgumentParser(description="Generate a random key")

parser.add_argument('-r', '--random', action='store_true', help='Generate random key and store it in a file')
parser.add_argument('-k', '--key', type=str, help='Convert the key in sha256 and store it in a file')
parser.add_argument('-f', '--file', help='The file to store the key', required=True)
args = parser.parse_args()


def main() -> None:
    try:
        f = open(args.file, "wb")

        if args.random:
            print(OK + "Generating random key")
            f.write(random.randbytes(32))

        elif args.key:
            print(OK + "Hashing the key in SHA256")
            hs = hashlib.sha256(args.key.encode()).digest()
            f.write(hs)

        print(OK + "Key stored in " + args.file)

        f.close()
    
    except PermissionError:
        print(ERROR + "Permission denied")
    
    except Exception as e:
        print(ERROR + "Unexpected error: " + str(e))


if __name__ == "__main__":
    main()