import streamlit as st
import re
import random
import string

# Common password blacklist
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "admin", "welcome", "letmein", "monkey"
]

def generate_strong_password(length=10, include_numbers=True, include_special=True):
    """Generate a strong password meeting user-selected requirements."""
    # Always include uppercase and lowercase letters.
    characters = string.ascii_uppercase + string.ascii_lowercase
    mandatory = [random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase)]
    
    # Optionally add numbers
    if include_numbers:
        characters += string.digits
        mandatory.append(random.choice(string.digits))
    # Optionally add special characters
    if include_special:
        characters += "!@#$%^&*"
        mandatory.append(random.choice("!@#$%^&*"))
    
    # Ensure the total length is at least as long as the mandatory characters
    if length < len(mandatory):
        length = len(mandatory)
    
    remaining = length - len(mandatory)
    password_list = mandatory + random.choices(characters, k=remaining)
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

def check_password_strength(password):
    """Evaluate password strength and return result with feedback."""
    score = 0
    feedback = []
    
    if password.lower() in COMMON_PASSWORDS:
        return "Weak", ["❌ This password is too common and easily guessable."]
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    if any(c.isupper() for c in password) and any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    if score == 4:
        return "Strong", ["✅ Excellent! Your password meets all security requirements."]
    elif score == 3:
        return "Moderate", ["⚠️ Good start, but your password could be stronger."] + feedback
    else:
        return "Weak", ["❌ Weak password - needs significant improvements."] + feedback

# Initialize session state for generated password if not present
if "generated_password" not in st.session_state:
    st.session_state["generated_password"] = ""

st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")
st.title("🔐 Password Strength Meter")
st.markdown("Check your password security and get improvement suggestions.")

# -- Password Input Section --
col_input, col_check = st.columns([3, 1])
with col_input:
    user_password = st.text_input("Enter Password:", type="password", key="password_input")
with col_check:
    check_pw = st.button("Check Password Strength")

# -- Password Check Feedback Section --
if check_pw:
    if user_password:
        strength, feedback = check_password_strength(user_password)
        if strength == "Strong":
            st.success("🔒 Strong Password!")
        elif strength == "Moderate":
            st.warning("⚠️ Moderate Password")
        else:
            st.error("🔓 Weak Password")
        
        for message in feedback:
            if message.startswith("✅"):
                st.success(message)
            elif message.startswith("⚠️"):
                st.warning(message)
            else:
                st.error(message)
    else:
        st.warning("Please enter a password to check.")

# -- Password Generator Section (Displayed below the check results) --
st.markdown("### Password Generator Options")
include_numbers = st.checkbox("Include Numbers", value=True)
include_special = st.checkbox("Include Special Characters", value=True)
generate_pw = st.button("Generate Strong Password")

if generate_pw:
    st.session_state["generated_password"] = generate_strong_password(include_numbers=include_numbers, include_special=include_special)

if st.session_state["generated_password"]:
    st.success(f"Generated Strong Password: {st.session_state['generated_password']}")

st.markdown("---")
st.markdown("**Security Tips:**")
st.markdown(
    "- Use a unique password for each account\n"
    "- Consider using a password manager\n"
    "- Enable two-factor authentication where available"
)
