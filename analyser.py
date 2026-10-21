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
        reader(data)
    else:
        print("File is empty!")


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

if __name__ == "__main__":
    main()

