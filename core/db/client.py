import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    missing = [k for k in ("SUPABASE_URL", "SUPABASE_KEY") if not st.secrets.get(k)]
    if missing:
        raise RuntimeError(f"Missing Streamlit secret(s): {', '.join(missing)}")
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
