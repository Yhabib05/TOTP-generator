"""
Generate a a totp on click of a button, or a qr code ? 
It Should be customizable for each user, the secret: changes for each user

"""
import streamlit as st
from totp import totp  # Import the TOTP function from totp.py
import time


# Welcome message
st.title("Welcome to the TOTP Generator App!")
st.write("""
This app allows you to generate Time-based One-Time Passwords (TOTP) using various algorithms. 
Customize your token length, validity period, and algorithm to suit your needs. 
Let's get started!
""")

default_size=st.checkbox("Default size - 6 digits ( for OTPs like microsoft and google authenticator)")
# Token length slider
if default_size:
    token_length=6
else:
    token_length = st.slider("Token Length", min_value=6, max_value=100, value=10)

# Checkbox to allow infinite validity
no_expiry = st.checkbox("No Expiry (Always Valid)")

# Validity period slider (disabled if 'No Expiry' is checked)
if no_expiry:
    validity_period = float('inf')  # Infinite validity period
else:
    validity_period = st.slider("Token Validity (in seconds)", min_value=1, max_value=120, value=30)


# Algorithm selection
algorithm = st.selectbox("Select HMAC Algorithm", ["SHA1", "SHA256", "SHA512"])

# Secret key input with default option
secret_key = st.text_input("Enter Secret Key (Base32)", "JBSWY3DPEHPK3PXP")


count_down_st=st.empty()
def count_down(ts):
    #with st.empty():
    #if ts==float('inf'):
        
    while ts:
        mins, secs = divmod(ts, 60)
        time_now = '{:02d}:{:02d}'.format(mins, secs)
        count_down_st.header(f"{time_now}")
        time.sleep(1)
        ts -= 1
    count_down_st.header(f"{ts}")
    return ts        


# Generate TOTP button
generate_totp=st.empty()

time_left=float('inf')

if st.button("Generate TOTP"):
    totp_token = totp(secret_key, algorithm, token_length, validity_period)
    generate_totp.success(f"Generated TOTP Token: {totp_token}")
    
    if validity_period == float('inf'):
        st.warning("Your token has infinite validity.")

    else:
        time_left=count_down(validity_period)
   
    if time_left == 0:
        generate_totp.warning("Token expired. Please generate a new one.")
