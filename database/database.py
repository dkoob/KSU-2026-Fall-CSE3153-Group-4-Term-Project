import os
from mssql_python import connect
from dotenv import load_dotenv

load_dotenv()

def get_connection():

    tailscale_conn = os.getenv("TAILSCALE_CONNECTION", "").lower() == "true"

    print("TAILSCALE_CONNECTION", tailscale_conn)

    if tailscale_conn:
        connection_string = (
            f"Server={os.getenv('DB_SERVER')};"
            f"Database={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

    else:
        connection_string = (
            "Server=localhost;"
            "Database=CSE3153_Group4_Finance_Tracker;"
            "Trusted_Connection=True;"
        )

    return connect(connection_string)