# binary_to_hex_text.py
# This script reads a binary file and writes each byte as a hexadecimal string prefixed with '0x' into a text file.

def convert_binary_to_hex(input_file, output_file):
    with open(input_file, 'rb') as f:
        binary_data = f.read()

    hex_lines = [f"0x{byte:02x}," for byte in binary_data]

    with open(output_file, 'w') as f:
        f.write(''.join(hex_lines))

    print(f"Converted {len(binary_data)} bytes from '{input_file}' to '{output_file}' in hex format.")

# Example usage:
# convert_binary_to_hex('TMC_HILUX_IMV_Fd.sig', 'TMC_HILUX_IMV_Fd.sig')