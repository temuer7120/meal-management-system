from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User
from functools import wraps
from flask import jsonify

ROLE_PERMISSIONS = {
    'admin': ['create', 'read', 'update', 'delete', 'upload', 'init'],
    'nutritionist': ['create', 'read', 'update', 'delete'],
    'chef': ['read', 'update'],
    'admin_staff': ['create', 'read', 'update', 'delete'],
    'head_nurse': ['read', 'update'],
    'nurse': ['read', 'update'],
    'caregiver': ['read', 'update'],
    'customer': ['read'],
    'guest': ['read'],
    'sales': ['create', 'read', 'update'],
    'chef_assistant': ['read', 'update'],
    'delivery_staff': ['read', 'update']
}

RESOURCE_PERMISSIONS = {
    'menu': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['read', 'update'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'dish': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['create', 'read', 'update', 'delete'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read', 'update'],
        'delivery_staff': ['read']
    },
    'customer': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read', 'update'],
        'chef': ['read'],
        'admin_staff': ['create', 'read', 'update', 'delete'],
        'head_nurse': ['read', 'update'],
        'nurse': ['read', 'update'],
        'caregiver': ['read', 'update'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['create', 'read', 'update'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'ingredient': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['create', 'read', 'update', 'delete'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read', 'update'],
        'delivery_staff': ['read']
    },
    'upload': {
        'admin': ['upload'],
        'nutritionist': ['upload'],
        'chef': ['upload'],
        'admin_staff': ['upload'],
        'head_nurse': [],
        'nurse': [],
        'caregiver': [],
        'customer': [],
        'guest': [],
        'sales': [],
        'chef_assistant': [],
        'delivery_staff': []
    },
    'order': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['create', 'read', 'update', 'delete'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['create', 'read', 'update'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read', 'update']
    },
    'meal_schedule': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['read', 'update'],
        'admin_staff': ['read'],
        'head_nurse': ['read', 'update'],
        'nurse': ['read', 'update'],
        'caregiver': ['read', 'update'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read', 'update'],
        'delivery_staff': ['read', 'update']
    },
    'service': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['create', 'read', 'update', 'delete'],
        'head_nurse': ['create', 'read', 'update'],
        'nurse': ['create', 'read', 'update'],
        'caregiver': ['create', 'read', 'update'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'confinement_meal': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['create', 'read', 'update', 'delete'],
        'chef': ['read', 'update'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['create', 'read', 'update'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'delivery': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['create', 'read', 'update', 'delete'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['create', 'read', 'update']
    },
    'ai_analysis': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'supplier': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['create', 'read', 'update', 'delete'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'ingredient_purchase': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['create', 'read', 'update'],
        'admin_staff': ['create', 'read', 'update'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read', 'update'],
        'delivery_staff': ['read']
    },
    'alert': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read', 'update'],
        'chef': ['read', 'update'],
        'admin_staff': ['read', 'update'],
        'head_nurse': ['read', 'update'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    },
    'alert_threshold': {
        'admin': ['create', 'read', 'update', 'delete'],
        'nutritionist': ['read'],
        'chef': ['read'],
        'admin_staff': ['read'],
        'head_nurse': ['read'],
        'nurse': ['read'],
        'caregiver': ['read'],
        'customer': ['read'],
        'guest': ['read'],
        'sales': ['read'],
        'chef_assistant': ['read'],
        'delivery_staff': ['read']
    }
}

def get_current_user():
    try:
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        return user
    except:
        return None

def requires_permission(action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_role = user.role
            if user_role not in ROLE_PERMISSIONS:
                return jsonify({'error': 'Role not found'}), 403
            
            if action not in ROLE_PERMISSIONS[user_role]:
                return jsonify({'error': 'Permission denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def requires_resource_permission(resource, action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_role = user.role
            if user_role not in RESOURCE_PERMISSIONS.get(resource, {}):
                return jsonify({'error': 'Role not authorized for this resource'}), 403
            
            if action not in RESOURCE_PERMISSIONS[resource][user_role]:
                return jsonify({'error': 'Permission denied for this action'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_data(data, required_fields=None):
    if not data:
        return False, {'error': 'No data provided'}
    
    if required_fields:
        for field in required_fields:
            if field not in data:
                return False, {'error': f'Required field {field} missing'}
    
    return True, None

def handle_error(e):
    return jsonify({'error': str(e)}), 500