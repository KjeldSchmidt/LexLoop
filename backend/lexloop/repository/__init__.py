from supabase import create_client
from lexloop.config import environment

supabase = create_client(environment.SUPABASE_URL, environment.SUPABASE_KEY)
