import os
import hashlib

SIGNATURES = {
    b"\xff\xd8\xff": "JPG",
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"%PDF-": "PDF",
    b"GIF87a": "GIF 87",
    b"GIF89a": "GIF 89",
    b"PK\x03\x04": "ZIP",
    b"\x7fELF": "ELF", # linux
    b"MZ": "EXE",
}

MAX_SIG_LEN = max(len(sig) for sig in SIGNATURES)

HEX_DUMP_DEFAULT = 256  # bytes shown in the hex dump unless the user asks for more

def main():
    file_path = input("Enter a file to open: ").strip()
    limit = input(f"Bytes to show (blank) = {HEX_DUMP_DEFAULT}, 'all' = entire file):").strip()
    if limit == "":
        limit = HEX_DUMP_DEFAULT
    elif limit == "all":
        limit = None
    else:
        try:
            limit = int(limit)
        except ValueError:
            print("Please enter a whole number or 'all'.")
            return
        if limit <= 0:
            print("Please enter a number greater than 0.")
            return

    try:
        with open(file_path, "rb") as file:
            data = file.read()
    except FileNotFoundError:
        print("That file could not be found.")
        return
    except PermissionError:
        print("You don't have permission to read that file.")
        return
    except OSError as error:
        print(f"Could not read the file: {error}")
        return
    
    if not data:
        print("File is empty!")
        return

    print("File size:", len(data), "bytes")
    md5_hash, sha256_hash = hash_file(file_path)
    print("MD5:    ", md5_hash)
    print("SHA-256:", sha256_hash)
    print("Detected format:", file_sig(file_path))

    print()
    reader(data[:limit])
    if limit is not None and len(data) > limit:
        print(f"... showing first {limit} of {len(data)} bytes")

    strings = str_extract(data)

    print("\nExtracted strings:")
    print("Offset   | String")
    print("-" * 40)

    for offset, text in strings:
        print(f"{offset:08x} | {text}")

    if not strings:
        print("No strings met the minimum length.")

def file_sig(file_path):
    with open(file_path, "rb") as file:
        header = file.read(MAX_SIG_LEN)

    for sig, file_type in SIGNATURES.items():
        if header.startswith(sig):
            return file_type

    return "Unknown file format"

def reader(data):
    print(f"{'Offset':8} | {'Hex':^47} | Text")
    print("-" * 76)
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]

        text = ""

        for value in chunk:
            if 32 <= value <= 126:
                text += chr(value)
            else:
                text += "."

        hex_values = chunk.hex(" ")
        print(f"{offset:08x} | {hex_values:<47} | {text}")

def str_extract(data,min_length=4):
    results = []
    current_str = ""
    start = 0

    for offset, value in enumerate(data):
        if 32 <= value <= 126:
            if current_str == "":
                start = offset
            current_str += chr(value)
        else:
            if len(current_str) >= min_length:
                results.append((start, current_str)) # store results as tuples
            current_str = ""
    if len(current_str) >= min_length:
        results.append((start, current_str))
    
    return results

def hash_file(file_path, chunk_size=65536): # 64kb chunk
    """ return MD5 and SHA-256 hashes of the file as hex strings """
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            md5.update(chunk)
            sha256.update(chunk)

        return md5.hexdigest(), sha256.hexdigest()




if __name__ == "__main__":
    main()

