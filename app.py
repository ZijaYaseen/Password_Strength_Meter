import streamlit as st
import re
import string
import random

COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "admin", "welcome", "letmein", "monkey"
]

def generate_strong_password(length=10, include_numbers=True, include_special=True):
    """Generate a strong password meeting user selected requirements"""
    characters = string.ascii_uppercase + string.ascii_lowercase
    mandatory = [random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase)]

    if include_numbers:
        characters += string.digits
        mandatory.append(random.choice(string.digits))

    if include_special:
        characters = '!@#$%^&*'
        mandatory.append(random.choice('!@#$%^&*'))

    if length < len(mandatory):
        length = len(mandatory)
        print(length)

generate_strong_password(5, True, True)

