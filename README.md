# TOTP Generator

This project implements a Time-based One-Time Password (TOTP) generator using different HMAC algorithms. TOTP is based on the HMAC-based One-Time Password (HOTP) algorithm and uses the current time as a counter to generate time-sensitive codes.


### Algorithms Supported:

- **HMAC-SHA1**
- **HMAC-SHA256**
- **HMAC-SHA512**

## Installation

To use this script, you need to have Python 3 installed. You can install the required packages using `pip`:

```sh
pip install -r requirements.txt
```

## Usage

You can use this script from the command line to generate TOTP tokens. Here are the command-line options:

```
script.py [-h] -s SECRET [-a {SHA1,SHA256,SHA512}] [-l LENGTH] [-v VALIDITY]
```

## Example
Generate a TOTP token with SHA256 algorithm:

```sh
python script.py -s JBSWY3DPEHPK3PXP -a SHA256
```

## References
[RFC 6238: Specification of TOTP ](https://datatracker.ietf.org/doc/html/rfc6238)

[RFC 4226: Specification of HOTP](https://datatracker.ietf.org/doc/html/rfc4226)