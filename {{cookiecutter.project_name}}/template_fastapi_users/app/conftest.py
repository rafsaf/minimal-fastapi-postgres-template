"""
Used to execute code before running tests, in this case we want to use test database.
We don't want to mess up dev database.

Put here any Pytest related code (it will be executed before `app/tests/...`)
"""

import os

# This will ensure using test database
os.environ["ENVIRONMENT"] = "PYTEST"
# This will change default 12 bcrypt rounds to only 1 so hashing password func will be short
os.environ["SECURITY_BCRYPT_DEFAULT_ROUNDS"] = "1"
