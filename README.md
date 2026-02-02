# 餐饮管理系统

## 项目简介
餐饮管理系统是一个完整的餐饮运营管理解决方案，包含食材管理、菜品管理、菜单管理、客户管理、订单管理、排餐管理等功能。

## 技术栈

### 后端
- Flask：Python Web框架
- SQLAlchemy：ORM数据库工具
- JWT：用户认证
- CORS：跨域资源共享
- Pandas：Excel文件解析

### 前端
- HTML/CSS/JavaScript：基础前端技术

### 微信小程序
- 原生微信小程序开发

## 数据库
- SQLite（开发环境）
- MySQL（生产环境，推荐）

## 快速开始

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库
编辑 `backend/app.py` 中的数据库连接字符串：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://meal_user:meal_password@localhost:3306/meal_management'
```

### 3. 初始化数据库
```bash
python -c "from app import app; with app.app_context(): from extensions import db; db.create_all()"
```

### 4. 启动服务
```bash
python app.py
```

服务将在 `http://127.0.0.1:5000` 启动。

## 主要功能

1. **用户管理**：用户注册、登录、权限控制
2. **食材管理**：食材的增删改查、库存管理
3. **菜品管理**：菜品的增删改查、食材组成管理
4. **菜单管理**：基础菜单、每日菜单的管理
5. **客户管理**：客户信息的管理、饮食禁忌记录
6. **订单管理**：客户订单的创建、查询、状态更新
7. **排餐管理**：排餐表的创建、菜品分配、状态跟踪
8. **Excel上传**：支持上传Excel文件导入菜单和排餐数据

## 权限管理

系统采用基于角色的权限控制（RBAC），包含以下角色：

- `admin`：管理员，拥有所有权限
- `nutritionist`：营养师，负责菜品和菜单管理
- `chef`：厨师，负责食材和菜品管理
- `admin_staff`：行政人员，负责客户和订单管理
- `head_nurse`：护士长，负责客户管理
- `nurse`：护士，负责客户管理
- `caregiver`：护理员，负责客户管理
- `customer`：客户，只能查看信息
- `guest`：访客，只能查看信息

## 并发控制

系统使用乐观锁机制实现多用户并发控制，确保数据一致性。

## 项目结构

```
MealManagementSystem/
├── backend/           # 后端代码
│   ├── docs/          # 文档
│   ├── instance/      # 数据库文件
│   ├── uploads/       # 上传文件
│   ├── utils/         # 工具函数
│   ├── app.py         # 应用入口
│   ├── config.py      # 配置文件
│   ├── extensions.py  # 扩展初始化
│   ├── models.py      # 数据库模型
│   ├── routes.py      # API路由
│   └── requirements.txt # 依赖包
├── frontend/          # 前端代码
│   ├── index.html     # 首页
│   └── ui_design.html # UI设计
└── wechat-miniprogram/ # 微信小程序代码
    ├── images/        # 图片资源
    ├── pages/         # 页面
    ├── app.js         # 小程序入口
    └── app.json       # 小程序配置
```

## 许可证

MIT License