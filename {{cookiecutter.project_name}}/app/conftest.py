import os

# We overwrite variables from .env to hardcoded one to connect with test database
# We don't want to mess up dev database
#
# Put here any pytest-specific code (it will run before app/tests/...)

os.environ["ENVIRONMENT"] = "PYTEST"
