# dashboard_controller.py
from flask import Blueprint, request, jsonify
from services.dashboard_service import DashboardService
#from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/create-folder', methods=['POST'])
#@jwt_required() 
def create_folder():
    data = request.get_json()
    user = data.get('user')
    folder_name = data.get('folder')
    new_folder = DashboardService.create_folder(user, folder_name)
    return jsonify({"message": "Folder created successfully", "folder": new_folder.folder}), 201

@dashboard_bp.route('/delete-folder/<string:folder_name>', methods=['DELETE'])
#@jwt_required() 
def delete_folder(folder_name):
    print(folder_name)
    success = DashboardService.delete_folder(folder_name)
    if success:
        return jsonify({"message": "Folder deleted successfully"}), 200
    return jsonify({"error": "Folder not found"}), 404

@dashboard_bp.route('/get-folders', methods=['POST'])
#@jwt_required() 
def get_folders():
    try:
        data = request.json
        user = data.get('user')
        if not user:
            return jsonify({'message': 'User ID is required'}), 400

        folders = DashboardService.get_all_folders_for_user(user)

        if folders is None:
            return jsonify({'message': 'Unable to fetch folders'}), 500

        return jsonify({'folders': folders}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An internal error occurred'}), 500
