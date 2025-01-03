# ByteCrypt - Directory Encryption and Decryption Tool

**ByteCrypt** is a powerful tool for encrypting and decrypting entire directories. By using an encryption key provided via the command line or from a file, ByteCrypt allows you to secure your data or recover it from an encrypted version.

## Requirements
- Python 3.x
- Python modules:
    - `argparse`
    - `pycryptodome`
    - `colorama`

## Installation

1. Clone the repository

```bash
git clone https://github.com/0Lunar/ByteCrypt.git
```

2. install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```
ByteCrypt - v1.0.0

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Enter the partition where the data is located
  -k KEY, --key KEY     Enter the key in hex
  -kf KEYFILE, --keyfile KEYFILE
                        Use the key in a file
  -a ACTION, --action ACTION
                        Chose to decrypt or encrypt: 'd' for decrypt and 'e' for encrypt
  -v, --verbose         Print all the encrypted files
  -s, --show            Print information about encryption/decryption
```

## Examples

**Encrypt a directory with a key provided manually:**

```bash
python3 bytecrypt.py -p /path/to/directory -k "mySecretKey" -a e
```

**Decrypt a directory using a key from a file:**

```bash
python3 bytecrypt.py -p /path/to/directory -kf /path/to/keyfile.bin -a d
```

**Encrypt a directory and print details about the encrypted files:**

```bash
python bytecrypt.py -p /path/to/directory -k "mySecretKey" -a e -v
```

**Decrypt a directory and show additional information:**

```bash
python bytecrypt.py -p /path/to/directory -kf /path/to/keyfile.txt -a d -s
```


## Security

**ByteCrypt** uses secure encryption algorithms, but it is important to protect your encryption key. **Do not share the key or the keyfile in unsecured environments**, and make sure that key files are stored safely.