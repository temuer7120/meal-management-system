from flask import Blueprint, request, jsonify
from extensions import db, jwt
from models import MenuCategory, Dish, Menu, MenuDish, DailyMenu, DailyMenuDish, Customer, CustomerMenu, User, BasicMenu, Ingredient, DishIngredient, CustomerOrder, OrderItem, MealSchedule, MealScheduleItem, ServiceCategory, ServiceItem, ServiceRecord, ServiceFeedback, ConfinementMealPlan, ConfinementWeekPlan, ConfinementDayPlan, ConfinementMealItem, WeChatUser, CustomerWeChat, DeliveryRecord, AIAnalysisResult, Supplier, IngredientPurchase, Alert, AlertThreshold
import pandas as pd
import os
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.security import requires_permission, requires_resource_permission, validate_data, handle_error

api = Blueprint('api', __name__)

@api.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username, role=role)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    }), 200

@api.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role
    }), 200