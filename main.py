import argparse
import os
import sys
from source.MapRoot import MapRoot
from source.Crypt import Crypt


parser = argparse.ArgumentParser(description="Encrypt and decrypt root partitions")

parser.add_argument('-p', '--path', type=str, help='Enter the partition where the data is located', required=True)
parser.add_argument('-k', '--key', type=str, help='Enter the key on commandline')
parser.add_argument('-kf', '--keyfile', type=str, help='Use the key in a file')
parser.add_argument('-a', '--action', type=str, help='Chose to decrypt or encrypt: \'d\' for decrypt and \'e\' for encrypt', required=True)
args = parser.parse_args()


def checkArgs() -> None:
    if not args.key and not args.keyfile:
        print("Missing key")
        sys.exit(0)

    if args.keyfile and args.key:
        print("Too many keys")
        sys.exit(0)

    if not os.path.isdir(args.path):
        print("Directory not found")
        sys.exit(0)


def getKey() -> bytes:
    if args.keyfile:
        key = open(args.keyfile, "rb").read()
        
        if len(key) != 32:
            raise RuntimeError("Invalid key lenght")
        
        return key
    
    return args.key


def encrypt() -> None:
    key = getKey()

    mapper = MapRoot(args.path)
    files = mapper.tree()
    cipher = Crypt(key)

    for file in files:
        data = open(file, "rb").read()
        new_data = cipher.encrypt(data)
        encrypted_data = b''.join(new_data)
        print(file)
        os.remove(file)
        open(file + ".enc", "wb").write(encrypted_data)


def decrypt() -> None:
    key = getKey()

    mapper = MapRoot(args.path)
    files = mapper.tree()
    cipher = Crypt(key)

    for file in files:
        if file.endswith(".enc"):
            f = open(file, "rb")
            data = f.read()

            nonce = data[:12]
            tag = data[-16:]
            data = data[12:-16]

            decrypted_data = cipher.decrypt(nonce, data, tag)

            print(file[:-4])

            os.remove(file)

            f = open(file[:-4], "wb")
            f.write(decrypted_data)
            f.close()


def main() -> None:
    checkArgs()

    if args.action == 'e':
        encrypt()
    
    elif args.action == 'd':
        decrypt()

    else:
        raise RuntimeError("Invalid action")


if __name__ == "__main__":
    main()