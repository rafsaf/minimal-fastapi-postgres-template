from app.auth.password import get_password_hash

TESTS_USER_PASSWORD = "geralt"
TESTS_USER_PASSWORD_HASH = get_password_hash(TESTS_USER_PASSWORD)
