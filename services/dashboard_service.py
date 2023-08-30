# dashboard_service.py
from folder import Folder, db

class DashboardService:
    @staticmethod
    def create_folder(user, folder_name):
        new_folder = Folder(user=user, folder=folder_name)
        db.session.add(new_folder)
        db.session.commit()
        # make folder in s3
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
