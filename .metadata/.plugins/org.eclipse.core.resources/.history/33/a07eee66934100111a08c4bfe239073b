/*
 * secure_wrapper.h
 *
 *  Created on: Apr 26, 2026
 *      Author: hegde
 */

#ifndef INC_SECURE_WRAPPER_H_
#define INC_SECURE_WRAPPER_H_

#include "cmox_crypto.h"

#endif /* INC_SECURE_WRAPPER_H_ */


#define SIGNATURE_SIZE                          64U
#define PUBLIC_KEY_SIZE                         64U
#define SIGNATURE_VERIFICATION_CMD_SIZE         1U
#define SIGNATURE_MSG_BUFFER_SIZE               (SIGNATURE_SIZE+SIGNATURE_VERIFICATION_CMD_SIZE)
#define SEC_OK                                  0U
#define SEC_NOT_OK		                        1U

#define PUBLIC_KEY_ADDR   0x0807F800
#define PUB_KEY_PTR        ((const uint8_t*)(PUBLIC_KEY_ADDR))

#define SIGNATURE_STORAGE_AREA   0x0807F000
#define SIGNATURE_PTR       ((uint8_t*)(SIGNATURE_STORAGE_AREA))

typedef uint8_t  Std_Security_Return_type;

void init_ecc_system(void);
Std_Security_Return_type Calculate_Firmware_Hash(uint8_t *output_digest, uint32_t startAddress, uint16_t size);
Std_Security_Return_type Calculate_Signature(uint8_t* outputDigest, uint8_t* signatureRec);


