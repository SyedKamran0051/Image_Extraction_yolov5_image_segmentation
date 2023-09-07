# dashboard_service.py
from models.folder import Folder
from init_db import db
from constants import path
from database_connection import DatabaseConnection


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
            db.session.delete(folder)
            db.session.commit()
            # delete from s3
            return True
        return False
    
    @staticmethod
    def get_all_folders_for_user(user_id):
        try:
            # Fetch folders from the database for the given user_id
            # This is a placeholder; replace with actual database query
            folders = Folder.query.filter_by(user=user_id).all()
            
            folder_list = [folder.folder for folder in folders]  # Assuming folders have a 'name' attribute
            return folder_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

