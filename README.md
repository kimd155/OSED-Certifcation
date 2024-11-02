# OSED Certifcation
This repository containing my journey and resources for Offensive Security Exploit Developer (OSED) certification. Includes exploit development scripts, reverse engineering notes, and custom PoCs crafted during the course.
***
# 📔 Cheat Sheet

## 1. Stack-Based Buffer Overflow
   - **🔑 Key Terms**:
     - **EIP (Extended Instruction Pointer)**: Controls program execution flow.
     - **ESP (Extended Stack Pointer)**: Points to the top of the stack.
     - **NOP Sled**: Sequence of `NOP` instructions (`\x90`) to land the shellcode.
   - **Steps**:
     - Identify buffer size with cyclic patterns.
     - Use `EIP` overwrite to redirect to shellcode.
     - Payload structure: `padding + EIP + NOP Sled + Shellcode`.

   - **Example**:
     ```python
     payload = b"A" * offset + eip_address + nop_sled + shellcode
     ```

## 2. Structured Exception Handler (SEH) Overwrite
   - **🔑 Key Terms**:
     - **SEH (Structured Exception Handler)**: Handles program exceptions and can be exploited for buffer overflows.
     - **POP POP RET**: Common SEH exploit technique for jumping to shellcode.
   - **Steps**:
     - Locate SEH overwrite offset with cyclic patterns.
     - Use `POP POP RET` to pass control to shellcode.
   
   - **Example**:
     ```python
     payload = b"A" * offset_to_seh + pop_pop_ret + nop_sled + shellcode
     ```

## 3. Egghunting
   - **Purpose**: Locate shellcode in memory when address isn’t directly accessible.
   - **Egg Signature**: 4-byte unique marker (like `w00t`) at the start of shellcode.
   - **Steps**:
     - Place shellcode in memory with egg marker.
     - Use egghunter shellcode to locate and execute.

   - **Example**:
     ```assembly
     mov eax, "w00t"    ; Mark the egg
     egghunter          ; Finds and executes shellcode with "w00t" marker
     ```

## 4. ROP (Return-Oriented Programming)
   - **🔑 Key Terms**:
     - **Gadgets**: Small pieces of code ending in `RET` found in memory, chained together for exploitation.
     - **ROP Chain**: Series of gadgets used to bypass protections like DEP.
   - **Steps**:
     - Locate gadgets with tools like `ropper` or `monas`.
     - Build ROP chain to control memory and program flow.

   - **Example**:
     ```python
     rop_chain = [gadget1, gadget2, eip, shellcode]
     ```

## 5. Windows API Calls for Shellcode
   - **Common API Functions**:
     - `VirtualAlloc()`: Allocates memory, used in shellcode to bypass DEP.
     - `WinExec()` or `CreateProcessA()`: Executes programs like `cmd.exe`.
   - **Steps**:
     - Use ROP to call `VirtualAlloc` with executable permissions.
     - Inject shellcode to execute Windows commands.

## 6. ASLR (Address Space Layout Randomization) Bypass
   - **Techniques**:
     - Use static addresses in loaded modules (DLLs without ASLR).
     - Use memory leaks to reveal dynamic addresses.
   - **Example**:
     - Target common non-ASLR modules (like `kernel32.dll`) for ROP gadgets.

## 7. Common Shellcoding Techniques
   - **Avoid Bad Characters**: Replace null bytes (`\x00`) and other problematic characters.
   - **Metasploit msfvenom**:
     - Generate shellcode with `msfvenom`, specifying bad chars.
     ```bash
     msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0a" -f python
     ```

## 8. Debugging Tips
   - **Tools**:
     - **Immunity Debugger**: Attach and observe behavior.
     - **monas**: Plugin for finding ROP gadgets, bad characters, etc.
   - **Commands**:
     - `!mona modules` – List modules and identify ASLR/DEP status.
     - `!mona jmp -r esp` – Find jump instructions for EIP control.

## 9. Obfuscation Techniques
   - **String Encoding**: Encode strings with Base64 or XOR to avoid detection.
   - **Function Obfuscation**: Hide function calls using pointers or indirection.
