from schema import Schema, And, Optional

user = Schema(
    {
        'name': str,
        Optional('age'): str,
        'username': str,
        'password': str,
        'user_type': str
    }
)
