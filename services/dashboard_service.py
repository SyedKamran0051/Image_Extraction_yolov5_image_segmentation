# dashboard_service.py
from folder import Folder, db
import boto3 

class DashboardService:
    @staticmethod
    def create_folder(user, folder_name):
        new_folder = Folder(user=user, folder=folder_name)
        db.session.add(new_folder)
        db.session.commit()
        return new_folder

    @staticmethod
    def delete_folder(folder_id):
        folder = Folder.query.get(folder_id)
        if folder:
            folder_name = folder.folder  # Extract the folder name from the folder object

            # Delete from the database
            db.session.delete(folder)

            # Delete from S3
            s3 = boto3.client('s3')
            s3_bucket_name = 'canyon-creek-cuts'
            s3_directory_key = f'/{folder_name}/'  # Use the folder name in the S3 directory structure

            try:
                s3.delete_object(Bucket=s3_bucket_name, Key=s3_directory_key)
                db.session.commit()  # Commit the database deletion after S3 deletion
                return True
            except Exception as e:
                print(f"Failed to delete S3 directory: {e}")
                db.session.rollback()  # Roll back the database changes if S3 deletion fails

        return False
