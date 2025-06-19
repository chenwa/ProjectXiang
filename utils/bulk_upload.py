from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from dtos.address_dto import AddressDTO
from dtos.user_dto import UserDTO
from manage_user import add_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/bulk_upload_users")
def bulk_upload_users(file: UploadFile = File(...)):
    """
    Endpoint to bulk upload users from a CSV file.

    Parameters:
        file (UploadFile): The uploaded CSV file containing user data.

    Returns:
        dict: A summary of the bulk upload process.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file.file)

        # Validate required columns
        required_columns = ["first_name", "last_name", "email", "password", "org"]
        if not all(column in df.columns for column in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV file must contain the following columns: {', '.join(required_columns)}")

        # Iterate through the rows and create users
        created_users = []
        failed_users = []
        for _, row in df.iterrows():
            try:
                # Create a UserDTO object
                user_dto = UserDTO(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    org=row["org"],
                    password=row["password"]
                )


                # Add the user to the database
                new_user = add_user(user_dto)
                if new_user:
                    created_users.append(row["email"])
                else:
                    failed_users.append(row["email"])
            except Exception as e:
                logger.error(f"Failed to create user {row['email']}: {e}")
                failed_users.append(row["email"])

        return {
            "message": "Bulk upload completed.",
            "created_users": created_users,
            "failed_users": failed_users
        }

    except Exception as e:
        logger.error(f"Error processing bulk upload: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")