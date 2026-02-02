from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    """基础模型，包含乐观锁"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=0, nullable=False)

class MenuCategory(BaseModel):
    """菜单分类模型"""
    __tablename__ = 'menu_category'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<MenuCategory {self.name}>'

class Dish(BaseModel):
    """菜品模型"""
    __tablename__ = 'dish'
    name = db.Column(db.String(100), nullable=False, index=True)
    ingredients = db.Column(db.String(500))
    restrictions = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), index=True)
    category = db.relationship('MenuCategory', backref=db.backref('dishes', lazy=True))
    
    def __repr__(self):
        return f'<Dish {self.name}>'

class Menu(BaseModel):
    """菜单模型"""
    __tablename__ = 'menu'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(200))
    week_number = db.Column(db.Integer, index=True)
    
    def __repr__(self):
        return f'<Menu {self.name}>'

class MenuDish(BaseModel):
    """菜单与菜品的关联模型"""
    __tablename__ = 'menu_dish'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False, index=True)
    
    menu = db.relationship('Menu', backref=db.backref('menu_dishes', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('menu_dishes', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('menu_dishes', lazy=True))

class DailyMenu(BaseModel):
    """每日菜单模型"""
    __tablename__ = 'daily_menu'
    date = db.Column(db.Date, nullable=False, unique=True, index=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<DailyMenu {self.date}>'

class DailyMenuDish(BaseModel):
    """每日菜单与菜品的关联模型"""
    __tablename__ = 'daily_menu_dish'
    daily_menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1)
    
    daily_menu = db.relationship('DailyMenu', backref=db.backref('daily_menu_dishes', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('daily_menu_dishes', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('daily_menu_dishes', lazy=True))

class Customer(BaseModel):
    """客户模型"""
    __tablename__ = 'customer'
    name = db.Column(db.String(100), nullable=False, index=True)
    restrictions = db.Column(db.String(500))
    check_in_date = db.Column(db.Date, index=True)
    check_out_date = db.Column(db.Date, index=True)
    id_card_number = db.Column(db.String(20), unique=True, index=True)
    id_card_image = db.Column(db.String(500))
    physical_exam_image = db.Column(db.String(500))
    health_conditions = db.Column(db.JSON)
    stay_days = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class CustomerMenu(BaseModel):
    """客户菜单模型"""
    __tablename__ = 'customer_menu'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    daily_menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    
    customer = db.relationship('Customer', backref=db.backref('customer_menus', lazy=True))
    daily_menu = db.relationship('DailyMenu', backref=db.backref('customer_menus', lazy=True))

class User(BaseModel):
    """用户模型"""
    __tablename__ = 'user'
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', index=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Supplier(BaseModel):
    """供应商模型"""
    __tablename__ = 'supplier'
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20), index=True)
    address = db.Column(db.String(200))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class Ingredient(BaseModel):
    """食材模型"""
    __tablename__ = 'ingredient'
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(200))
    stock = db.Column(db.Float, default=0, index=True)
    unit = db.Column(db.String(20), default='g')
    nutrition_info = db.Column(db.JSON)
    calorie = db.Column(db.Float)
    shelf_life = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

class IngredientPurchase(BaseModel):
    """食材采购记录模型"""
    __tablename__ = 'ingredient_purchase'
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False, index=True)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    batch_number = db.Column(db.String(100), index=True)
    shelf_life = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    
    ingredient = db.relationship('Ingredient', backref=db.backref('purchases', lazy=True))
    supplier = db.relationship('Supplier', backref=db.backref('purchases', lazy=True))
    creator = db.relationship('User', backref=db.backref('purchases', lazy=True))
    
    def __repr__(self):
        return f'<IngredientPurchase Ingredient:{self.ingredient_id} Supplier:{self.supplier_id}>'

class DishIngredient(BaseModel):
    """菜品与食材的关联模型"""
    __tablename__ = 'dish_ingredient'
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False, index=True)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='g')
    
    dish = db.relationship('Dish', backref=db.backref('dish_ingredients', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('dish_ingredients', lazy=True))

class CustomerOrder(BaseModel):
    """客户订单模型"""
    __tablename__ = 'customer_order'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    order_date = db.Column(db.Date, nullable=False, default=datetime.now().date(), index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    total_amount = db.Column(db.Float, default=0)
    
    customer = db.relationship('Customer', backref=db.backref('customer_orders', lazy=True))

class OrderItem(BaseModel):
    """订单详情模型"""
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, default=0)
    
    order = db.relationship('CustomerOrder', backref=db.backref('order_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('order_items', lazy=True))

class MealSchedule(BaseModel):
    """排餐表模型"""
    __tablename__ = 'meal_schedule'
    date = db.Column(db.Date, nullable=False, unique=True, index=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='draft', index=True)
    
    def __repr__(self):
        return f'<MealSchedule {self.date}>'

class MealScheduleItem(BaseModel):
    """排餐表详情模型"""
    __tablename__ = 'meal_schedule_item'
    schedule_id = db.Column(db.Integer, db.ForeignKey('meal_schedule.id'), nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='scheduled', index=True)
    
    schedule = db.relationship('MealSchedule', backref=db.backref('schedule_items', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('schedule_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('schedule_items', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('schedule_items', lazy=True))

class BasicMenu(BaseModel):
    """基础餐单模型"""
    __tablename__ = 'basic_menu'
    week_number = db.Column(db.Integer, nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False, index=True)
    dish_name = db.Column(db.String(100), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, index=True)
    
    category = db.relationship('MenuCategory', backref=db.backref('basic_menus', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('basic_menus', lazy=True))
    
    def __repr__(self):
        return f'<BasicMenu Week:{self.week_number} Day:{self.day_of_week} Dish:{self.dish_name}>'

class ServiceCategory(BaseModel):
    """服务分类模型"""
    __tablename__ = 'service_category'
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<ServiceCategory {self.name}>'

class ServiceItem(BaseModel):
    """服务项目模型"""
    __tablename__ = 'service_item'
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), index=True)
    duration = db.Column(db.Integer)
    price = db.Column(db.Float, default=0)
    
    category = db.relationship('ServiceCategory', backref=db.backref('service_items', lazy=True))
    
    def __repr__(self):
        return f'<ServiceItem {self.name}>'

class ServiceRecord(BaseModel):
    """服务记录模型"""
    __tablename__ = 'service_record'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    service_item_id = db.Column(db.Integer, db.ForeignKey('service_item.id'), nullable=False, index=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, index=True)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(20), default='scheduled', index=True)
    notes = db.Column(db.String(500))
    
    customer = db.relationship('Customer', backref=db.backref('service_records', lazy=True))
    service_item = db.relationship('ServiceItem', backref=db.backref('service_records', lazy=True))
    staff = db.relationship('User', backref=db.backref('service_records', lazy=True))
    
    def __repr__(self):
        return f'<ServiceRecord Customer:{self.customer_id} Service:{self.service_item_id}>'

class ServiceFeedback(BaseModel):
    """服务反馈模型"""
    __tablename__ = 'service_feedback'
    service_record_id = db.Column(db.Integer, db.ForeignKey('service_record.id'), nullable=False, unique=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    
    service_record = db.relationship('ServiceRecord', backref=db.backref('feedback', uselist=False, lazy=True))
    customer = db.relationship('Customer', backref=db.backref('feedbacks', lazy=True))
    
    def __repr__(self):
        return f'<ServiceFeedback Record:{self.service_record_id} Rating:{self.rating}>'

class ConfinementMealPlan(BaseModel):
    """月子餐计划模型"""
    __tablename__ = 'confinement_meal_plan'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(20), default='active', index=True)
    type = db.Column(db.String(20), default='inhouse', index=True)
    
    customer = db.relationship('Customer', backref=db.backref('confinement_meal_plan', uselist=False, lazy=True))
    
    def __repr__(self):
        return f'<ConfinementMealPlan Customer:{self.customer_id} Type:{self.type}>'

class ConfinementWeekPlan(BaseModel):
    """月子餐周计划模型"""
    __tablename__ = 'confinement_week_plan'
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_meal_plan.id'), nullable=False, index=True)
    week_number = db.Column(db.Integer, nullable=False, index=True)
    
    meal_plan = db.relationship('ConfinementMealPlan', backref=db.backref('week_plans', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementWeekPlan Plan:{self.meal_plan_id} Week:{self.week_number}>'

class ConfinementDayPlan(BaseModel):
    """月子餐日计划模型"""
    __tablename__ = 'confinement_day_plan'
    week_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_week_plan.id'), nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)
    
    week_plan = db.relationship('ConfinementWeekPlan', backref=db.backref('day_plans', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementDayPlan Week:{self.week_plan_id} Day:{self.day_of_week}>'

class ConfinementMealItem(BaseModel):
    """月子餐单项模型"""
    __tablename__ = 'confinement_meal_item'
    day_plan_id = db.Column(db.Integer, db.ForeignKey('confinement_day_plan.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False, index=True)
    
    day_plan = db.relationship('ConfinementDayPlan', backref=db.backref('meal_items', lazy=True))
    category = db.relationship('MenuCategory', backref=db.backref('confinement_meal_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('confinement_meal_items', lazy=True))
    
    def __repr__(self):
        return f'<ConfinementMealItem Day:{self.day_plan_id} Category:{self.category_id} Dish:{self.dish_id}>'

class WeChatUser(BaseModel):
    """微信用户模型"""
    __tablename__ = 'wechat_user'
    openid = db.Column(db.String(100), nullable=False, unique=True, index=True)
    nickname = db.Column(db.String(100))
    avatar = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    
    def __repr__(self):
        return f'<WeChatUser {self.nickname}>'

class CustomerWeChat(BaseModel):
    """客户微信关联模型"""
    __tablename__ = 'customer_wechat'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True, index=True)
    wechat_user_id = db.Column(db.Integer, db.ForeignKey('wechat_user.id'), nullable=False, unique=True, index=True)
    
    customer = db.relationship('Customer', backref=db.backref('wechat关联', uselist=False, lazy=True))
    wechat_user = db.relationship('WeChatUser', backref=db.backref('customer关联', uselist=False, lazy=True))
    
    def __repr__(self):
        return f'<CustomerWeChat Customer:{self.customer_id} WeChat:{self.wechat_user_id}>'

class DeliveryRecord(BaseModel):
    """送餐记录模型"""
    __tablename__ = 'delivery_record'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    delivery_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), index=True)
    meal_schedule_item_id = db.Column(db.Integer, db.ForeignKey('meal_schedule_item.id'), index=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, index=True)
    duration = db.Column(db.Integer)
    distance = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending', index=True)
    notes = db.Column(db.String(500))
    
    customer = db.relationship('Customer', backref=db.backref('delivery_records', lazy=True))
    delivery_staff = db.relationship('User', backref=db.backref('delivery_records', lazy=True))
    order = db.relationship('CustomerOrder', backref=db.backref('delivery_records', lazy=True))
    meal_schedule_item = db.relationship('MealScheduleItem', backref=db.backref('delivery_records', lazy=True))
    
    def __repr__(self):
        return f'<DeliveryRecord Customer:{self.customer_id} Staff:{self.delivery_staff_id}>'

class AIAnalysisResult(BaseModel):
    """AI分析结果模型"""
    __tablename__ = 'ai_analysis_result'
    analysis_type = db.Column(db.String(50), nullable=False, index=True)
    analysis_data = db.Column(db.JSON)
    result = db.Column(db.JSON)
    recommendation = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    
    def __repr__(self):
        return f'<AIAnalysisResult Type:{self.analysis_type}>'