with open("sample.bin", "rb") as file:
    data = file.read(32)

def reader(d):
    print(d)
    print("Type:", type(d))
    print("Bytes read:", len(d))
    print("First byte:", d[0])
    print("Hex:", d.hex(" "))
    print("   Offset  | Hex | Decimal\n--------------------------")

    for offset, value in enumerate(d):
        print(f"  {offset:08x} | {value:02x}  |  {value}") 

if data:
    reader(data)
else:
    print("File is empty!")

