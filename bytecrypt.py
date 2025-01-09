import argparse
import os
import sys
from source.MapRoot import MapRoot
from source.Crypt import Crypt
from colorama import Fore
import hashlib


ERROR = Fore.RESET + "[" + Fore.RED + "!" + Fore.RESET + "] "
OK = Fore.RESET + "[" + Fore.GREEN + "+" + Fore.RESET + "] "
WARNING = Fore.RESET + "[" + Fore.YELLOW + "?" + Fore.RESET + "] "


parser = argparse.ArgumentParser(description="ByteCrypt - v1.0.0")

parser.add_argument('-p', '--path', type=str, help='Enter the partition where the data is located', required=True)
parser.add_argument('-k', '--key', type=str, help='Enter the key in hex')
parser.add_argument('-kf', '--keyfile', type=str, help='Use the key in a file')
parser.add_argument('-a', '--action', type=str, help='Chose to decrypt or encrypt: \'d\' for decrypt and \'e\' for encrypt', required=True)
parser.add_argument('-v', '--verbose', action='store_true', help='Print all the encrypted files')
parser.add_argument('-s', '--show', action='store_true', help='Print information about encryption/decryption')
args = parser.parse_args()


def checkArgs() -> None:
    if not args.key and not args.keyfile:
        print(ERROR + "Missing key")
        sys.exit(0)

    if args.keyfile and args.key:
        print(ERROR + "Too many keys")
        sys.exit(0)

    if not os.path.isdir(args.path):
        print(ERROR + "Directory not found")
        sys.exit(0)


def getKey() -> bytes:
    if args.keyfile:
        key = open(args.keyfile, "rb").read()
        
        if len(key) != 32:
            print(ERROR + "Invalid key length")
            sys.exit(0)
        
        return key
        
    else:
        return hashlib.sha256(args.key.encode()).digest()


def encrypt() -> None:
    key = getKey()

    if args.verbose or args.show:
        print(OK + "Loaded key: " + key.hex())

    mapper = MapRoot(args.path)
    files = mapper.tree()
    cipher = Crypt(key)

    for file in files:
        if file.endswith(".enc"):
            print("\n" + WARNING + "The file already have .enc extension")

        try:
            if args.show:
                if not file.endswith(".enc"):
                    print("\n")

                print(OK + "Encrypting: " + file)

            data = open(file, "rb").read()
            new_data = cipher.encrypt(data)

            if args.show:
                print(OK + "Nonce: " + new_data[0].hex())
                print(OK + "Tag: " + new_data[-1].hex())

            encrypted_data = b''.join(new_data)

            if args.verbose:
                print(OK + file)

            os.remove(file)
            open(file + ".enc", "wb").write(encrypted_data)
        
        except PermissionError:
            print(ERROR + "Permission error on file " + file)
        
        except Exception as e:
            print(ERROR + "Unexpected error: " + str(e))


def decrypt() -> None:
    key = getKey()

    if args.verbose or args.show:
        print(OK + "Loaded key: " + key.hex())

    mapper = MapRoot(args.path)
    files = mapper.tree()
    cipher = Crypt(key)

    for file in files:
        if file.endswith(".enc"):
            try:
                if args.show:
                    print("\n" + OK + "Decrypting: " + file)

                f = open(file, "rb")
                data = f.read()

                nonce = data[:12]
                tag = data[-16:]
                data = data[12:-16]
                
                f.close()

                if args.show:
                    print(OK + "Nonce: " + nonce.hex())
                    print(OK + "Tag: " + tag.hex())

                decrypted_data = cipher.decrypt(nonce, data, tag)

                if args.verbose:
                    print(OK + file[:-4])

                os.remove(file)

                f = open(file[:-4], "wb")
                f.write(decrypted_data)
                f.close()
            
            except PermissionError:
                print(ERROR + "Permission error on file " + file)
        
            except RuntimeError:
                print(ERROR + "Error decrypting: " + file)

            except Exception as e:
                print(ERROR + "Unexpected error: " + str(e))
            
        else:
            print(WARNING + "invalid extension: " + file)



def main() -> None:
    checkArgs()

    if args.action == 'e':
        encrypt()
    
    elif args.action == 'd':
        decrypt()

    else:
        print(ERROR + "Invalid action")


if __name__ == "__main__":
    main()
