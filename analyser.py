def main():
    file_path = input("Enter a file to open: ")

    try:
        with open(file_path, "rb") as file:
            data = file.read(32)
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
    signatures = {
        b"\xff\xd8\xff": "JPG",
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"%PDF-": "PDF",
        b"GIF87a": "GIF 87",
        b"GIF89a": "GIF 89",
    }
    for sig, type in signatures.items():
        if data.startswith(sig):
            return type

    return "Unknown file format"

def reader(d):
    print(f"{'Offset':8} | {'Hex':^47} | Text")
    print("-" * 76)
    for offset in range(0, len(d), 16):
        chunk = d[offset:offset + 16]

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

    for o, v in enumerate(data):
        if 32 <= v <= 128:
            if current_str == "":
                start = o
            current_str += chr(v)
        else:
            if len(current_str) >= min_length:
                results.append((start, current_str)) # store results as tuples
            current_str = ""
    if len(current_str) >= min_length:
        results.append((start, current_str))
    
    return results


if __name__ == "__main__":
    main()

