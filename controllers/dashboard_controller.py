# dashboard_controller.py
from flask import Blueprint, request, jsonify
from dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/create-folder', methods=['POST'])
def create_folder():
    data = request.get_json()
    user = data.get('user')
    folder_name = data.get('folder')
    new_folder = DashboardService.create_folder(user, folder_name)
    return jsonify({"message": "Folder created successfully", "folder": new_folder.folder}), 201

@dashboard_bp.route('/delete-folder/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    success = DashboardService.delete_folder(folder_id)
    if success:
        return jsonify({"message": "Folder deleted successfully"}), 200
    return jsonify({"message": "Folder not found"}), 404
