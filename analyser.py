import os

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

def main():
    file_path = input("Enter a file to open: ").strip()
    to_read = input("Enter an amount of bytes to read(or leave blank to read entire file): ").strip()
    if to_read == "":
        to_read = -1 # -1 reads entire file
    else:
        try:
            to_read = int(to_read)
        except ValueError:
            print("Please enter a whole number.")
            return

    try:
        with open(file_path, "rb") as file:
            data = file.read(to_read)
    except FileNotFoundError:
        print("That file could not be found.")
        return
    except PermissionError:
        print("You don't have permission to read that file.")
        return
    except OSError as error:
        print(f"Could not read the file: {error}")
        return
    if data:
        print("File size:", os.path.getsize(file_path))
        print("Detected format:", file_sig(data))
        reader(data)
        strings = str_extract(data)

        print("\nExtracted strings:")
        print("Offset   | String")
        print("-" * 40)

        for offset, text in strings:
            print(f"{offset:08x} | {text}")

        if not strings:
            print("No strings met the minimum length.")
    else:
        print("File is empty!")

def file_sig(data):
    
    for sig, file_type in SIGNATURES.items():
        if data.startswith(sig):
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


if __name__ == "__main__":
    main()

