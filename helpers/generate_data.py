

from faker import Faker

fake = Faker()

def generate_email(prefix="test"):
    """Генерация уникального email"""
    return f"{prefix}.{fake.md5()}@example.com"