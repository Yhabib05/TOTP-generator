"""
                         ----------------------------------------
                        |  TOTP = HOTP(K, T),                    |
                        |  HOTP(K,T) = Truncate(HMAC-SHA-1(K,T)) |
                         ----------------------------------------

   T : integer: represents the number of time steps between the initial counter time T0 and the current Unix time.
        T = (Current Unix time - T0) / X

              o  X represents the time step in seconds 
              o  T0 is the Unix time to start counting time steps 

   And Truncate represents the function that converts an HMAC-SHA-1 value into an HOTP value
      
We will provide the possibility to create an totp with one of the three HMAC algorithms 
HmacSHA1 : 16byte(128 bit)
HmacSHA256 : 32byte(256 bit)
HmacSHA512 : 64byte(512 bit)
"""

import argparse
import base64
from math import *
import time
import hmac
import hashlib  # Use hashlib for digest algorithms

# Default Values


TOKEN_LENGTH = 10 # Length of the geenrated TOTP
VALIDITY_PERIOD = 30 #valid for 30 seconds
T0=0

# Function to get the current time step
def time_function(validity): 
        current=floor(time.time()) # Get the current Unix time
        return floor((current-T0)/validity) # Counter (T) that increases every X seconds

# HMAC function for the 3 algorithms (SHA1, SHA256, SHA512)
def HMAC(secret:str, crypto:str, counter: int):
       hash_algorithm =hashlib.sha1 #by default
         
       # Generate key from the secret
       key= base64.b32decode(secret)

       # Convert the counter (T) to an 8-byte array (big-endian)
       counter_bytes= counter.to_bytes(8,"big")

       # Match statement to select the appropriate hash algorithm       
       match crypto:
                case "SHA1":
                       hash_algorithm=hashlib.sha1
                case "SHA256":
                       hash_algorithm=hashlib.sha256                      
                case "SHA512":
                       hash_algorithm=hashlib.sha512
                case _:
                       raise ValueError(f"Unsupported crypto algorithm: {crypto}")
          
       # Create the HMAC object with the key and selected hash algorithm
       return hmac.new(key,counter_bytes,hash_algorithm).digest()
       

def truncate(hmac_result):
       
       # Extract a 4-byte chunk from the HMAC result based on the offset
       offset =  hmac_result[-1] & 0x0F 
       truncated_hash=hmac_result[offset:offset+4] 
       truncated_int=int.from_bytes(truncated_hash)

       #Return the least significant 31 bits and generate the 6-digit token
       return (truncated_int&0x7FFFFFF)%10**TOKEN_LENGTH 


def totp(secret:str, algorithm, token_length, validity):
       
       counter=time_function(validity)
       hmac_result=HMAC(secret, algorithm, counter)
       totp_token=truncate(hmac_result)

       return str(totp_token).zfill(token_length) #Pad zeros on the left to ensure the token length is satisfied

# Example testing function
def test_totp():
    secret = "JBSWY3DPEHPK3PXP"  # Base32-encoded secret
    print("TOTP (SHA1):", totp(secret, "SHA1"))
    print("TOTP (SHA256):", totp(secret, "SHA256"))
    print("TOTP (SHA512):", totp(secret, "SHA512"))


def main():
    parser = argparse.ArgumentParser(description='Generate TOTP tokens using different HMAC algorithms.')
    
    # Add arguments
    parser.add_argument('-s', '--secret', type=str, required=True, help='Base32-encoded secret key.')
    parser.add_argument('-a', '--algorithm', choices=['SHA1', 'SHA256', 'SHA512'], default='SHA1', help='HMAC algorithm to use.')
    parser.add_argument('-l', '--length', type=int, default=TOKEN_LENGTH, help='Length of the generated TOTP token.')
    parser.add_argument('-v', '--validity', type=int, default=VALIDITY_PERIOD, help='Validity period for the TOTP token in seconds.')
    
    # Parse arguments
    args = parser.parse_args()

    # Generate and print the TOTP token
    token = totp(args.secret, args.algorithm, args.length, args.validity)
    print(f"TOTP Token: {token}")

if __name__ == "__main__":
    main()