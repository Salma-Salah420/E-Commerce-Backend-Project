import pandas as pd
import os

FILE_NAME = "users.xlsx"

def init_users():
    """Initialize the Excel file if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["id", "email", "password", "role"])
        df.to_excel(FILE_NAME, index=False)

def read_users():
    """Read users from the Excel file."""
    return pd.read_excel(FILE_NAME)

def save_users(df):
    """Save users DataFrame to the Excel file."""
    df.to_excel(FILE_NAME, index=False)
