# Secure Bootloader for STM32F303RE

## Overview
This repository contains the development of a custom, secure bootloader designed for the STM32F303RE microcontroller. The primary focus of this project is to implement a robust secure boot mechanism that verifies the authenticity and integrity of the application firmware before handing over execution control. 

## Features
*   **Secure Boot Mechanism:** Ensures that only authenticated firmware is executed by the microcontroller.
*   **Secure Flashing Mechanism** Ensures that only authenticated firmware is flashed to the microcontroller.
*   **Cryptographic Verification:** Implements ECDSA (Elliptic Curve Digital Signature Algorithm) for verifying firmware signatures prior to booting.
*   **Custom Memory Partitioning:** Configured memory boundaries to safely separate the bootloader operations from the main application space.

## Hardware & Software Requirements
*   **Target Microcontroller:** STM32F303RE (e.g., STM32 Nucleo-64 development board)
*   **Development Environment:** STM32CubeIDE
*   **Toolchain:** ARM GCC

## Memory Mapping
The internal flash memory is strictly partitioned between the bootloader and the user application. 

*   **Bootloader Base Address:** `0x08000000`
*   **Application Base Address:** `0x08020000` 

*Important: The vector table offset (`VECT_TAB_OFFSET`) in the main application's `system_stm32f3xx.c` file must be updated to match the application base address (`0x08020000`) to ensure interrupts are handled correctly after the bootloader completes the jump.*

## Cryptography Details
*   **Algorithm:** ECDSA
*   **Key Specifications:** The implementation utilizes a 64-byte public key (excluding the prefix byte) to verify the incoming application binary. 
*   **Fault Handling:** Memory alignment and hardware floating-point considerations have been accounted for to prevent hardfaults during the signature verification process.

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/hegde08/Bootloader_Developement.git](https://github.com/hegde08/Bootloader_Developement.git)
    ```
2.  **Open in STM32CubeIDE:** Import the project into your IDE workspace.
3.  **Compile the Application:** Build your main application firmware, ensuring your linker script (`.ld`) is configured with ROM starting at `0x08020000`.
4.  **Sign the Firmware:** Generate the ECDSA signature for your application binary using your private key.
5.  **Flash the Device:** 
    *   Flash the bootloader executable at `0x08000000`.
    *   Flash the signed application binary at `0x08020000`.
6.  **Execute:** Upon system reset, the bootloader will initialize, parse the 64-byte public key, and verify the ECDSA signature of the application. If the authentication passes, the program counter will jump to the application's Reset Handler.

## Author
**Surendra Radhakrishna Hegde**  
Automotive Cybersecurity Engineer
