import glob
import os
import subprocess
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from src.database.database import TRIAL_URL, DB_NAME
from src.database.database import create_database_if_not_exists
from src.dependencies.basic import get_db
from src.schemas.basic import TextOnly

router = APIRouter()


@router.post("/renew")
async def renew_database():
    from src.database.database import engine, drop_all_tables
    from src.database.database import create_all_tables
    from src.database.utils import add_test_data

    drop_all_tables(engine)
    create_all_tables(engine)
    add_test_data()
    return TextOnly(text="Database Renewed")


@router.post('/alembic')
async def alembic(
        db: Annotated[Session, Depends(get_db)],
        delete_first: Annotated[bool, Query(description="Delete python files in version directory first")] = True,
        skip_revision: Annotated[bool, Query(description="Skip the revision generation step")] = False,
        skip_upgrade: Annotated[bool, Query(description="Skip the upgrade head step")] = False,
):
    try:
        # Create database if not exists
        create_database_if_not_exists(TRIAL_URL, DB_NAME)

        if delete_first:
            print("Deleting python files in alembic versions directory")
            # Fix: Use glob to properly handle wildcard patterns
            version_files = glob.glob('/run/alembic/versions/*.py')
            for file_path in version_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

        # Remove alembic_version table
        try:
            db.execute(text("DROP TABLE IF EXISTS alembic_version"))
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to drop alembic_version table: {str(e)}")

        # Check if the script exists
        script_path = '/run/run_alembic.sh'
        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail=f"Alembic script not found at {script_path}")

        # Build command
        command = ['/bin/bash', script_path]
        if skip_revision:
            command.append('-r')
        if skip_upgrade:
            command.append('-u')

        # Execute with timeout and better error handling
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Return strings instead of bytes
            )

            # Wait for process to complete with timeout (5 minutes)
            output, error = process.communicate(timeout=300)

            # Check return code
            if process.returncode != 0:
                return {
                    "status": "error",
                    "return_code": process.returncode,
                    "output": output.split('\n') if output else [],
                    "error": error.split('\n') if error else []
                }

            return {
                "status": "success",
                "return_code": process.returncode,
                "output": output.split('\n') if output else [],
                "error": error.split('\n') if error else []
            }

        except subprocess.TimeoutExpired:
            process.kill()
            output, error = process.communicate()
            raise HTTPException(
                status_code=500,
                detail="Alembic process timed out after 5 minutes"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to execute alembic script: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
