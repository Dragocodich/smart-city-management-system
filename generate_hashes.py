#!/usr/bin/env python3
"""Generate bcrypt hashes for test credentials"""

import bcrypt

credentials = [
    ("admin", "Admin@123"),
    ("worker1", "Worker@123"),
    ("officer1", "Officer@123"),  # Add this one too
    ("citizen1", "Citizen@123"),
]

print("=" * 60)
print("BCRYPT PASSWORD HASHES FOR TEST CREDENTIALS")
print("=" * 60)
print()

for username, password in credentials:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Hash:     {hashed}")
    print()

print("=" * 60)
print("SQL UPDATE STATEMENTS")
print("=" * 60)
print()

for username, password in credentials:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f"UPDATE employees SET password_hash = '{hashed}' WHERE username = '{username}';")

print()
print("UPDATE citizens SET password_hash = '{}' WHERE username = 'citizen1';".format(
    bcrypt.hashpw("Citizen@123".encode(), bcrypt.gensalt()).decode()
))
