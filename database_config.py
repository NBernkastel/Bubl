from supabase import Client, create_client

from config.instance import secrets

url: str = secrets.SUPABASE_URL
key: str = secrets.SUPABASE_KEY
supabase: Client = create_client(url, key)