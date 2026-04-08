# 校园课程资源共享平台

一个基于 Django + Vue.js 的校园课程资源管理与共享平台，支持师生资源上传下载、论坛交流、AI 智能助手、积分激励等功能。

## 🎯 项目简介

本项目旨在为校园师生提供一个便捷的课程资源共享平台，整合课程资源管理、论坛交流、AI 智能助手、积分激励等功能，促进校园内知识共享与师生互动。

## ✨ 主要功能

### 核心功能模块

- **👥 多角色系统**：管理员、教师、学生三种角色，权限分明
- **📚 课程资源管理**：资源上传、下载、收藏、评论、评分
- **💬 论坛交流**：发帖、评论、互动，支持公开/指定范围可见
- **🤖 AI 智能助手**：集成豆包 AI，提供智能问答服务
- **🎁 积分激励系统**：积分获取、积分兑换、激励用户参与
- **📢 公告系统**：校园通知、重要信息发布
- **📊 数据统计**：用户行为分析、资源使用统计

### 角色功能

#### 学生端
- 浏览、搜索、下载课程资源
- 收藏喜欢的资源
- 参与论坛讨论、发帖、评论
- 使用 AI 智能助手
- 查看积分、兑换奖品
- 管理个人中心

#### 教师端
- 上传、管理课程资源
- 审核资源评论
- 参与论坛讨论
- 查看学生情况
- 管理个人中心

#### 管理员端
- 用户管理（学生、教师账号）
- 资源管理与审核
- 论坛管理
- 公告发布与管理
- 积分系统管理
- 系统设置与数据统计

## 🛠️ 技术栈

### 后端技术
- **框架**: Django 4.2.9
- **API**: Django REST Framework 3.14.0
- **认证**: JWT (djangorestframework-simplejwt 5.3.1)
- **跨域**: django-cors-headers 4.3.1
- **数据库**: SQLite（开发）/ MySQL（生产）
- **其他**: Pillow 10.1.0, requests 2.31.0, python-dotenv 1.0.0

### 前端技术
- **框架**: Vue 3.4.0 (Composition API)
- **语言**: TypeScript 5.2.2
- **构建工具**: Vite 5.0.8
- **UI 组件库**: Element Plus 2.4.4
- **状态管理**: Pinia 2.3.1
- **路由**: Vue Router 4.2.5
- **HTTP 客户端**: Axios 1.6.7

### AI 集成
- **模型**: 豆包 AI (字节跳动火山方舟)

## 📋 部署说明

### 环境要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端部署

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 3. 初始化示例数据（可选）
python init_sample_data.py

# 4. 创建超级管理员
python manage.py createsuperuser

# 5. 启动开发服务器
python manage.py runserver
```

### 前端部署

```bash
# 1. 安装 Node.js 依赖
npm install

# 2. 启动开发服务器
npm run dev

# 3. 构建生产版本
npm run build
```

### 一键启动脚本

项目提供了便捷的启动和停止脚本：

```bash
# 同时启动后端和前端
./start.sh

# 停止后端和前端服务
./stop.sh
```

## ⚙️ 配置说明

### 后端配置
在 `campus_platform/settings.py` 中配置数据库、密钥等：

```python
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}
```

### 前端配置
创建 `.env` 文件配置 API 地址：

```env
VITE_API_BASE=http://127.0.0.1:8000
```

### AI 配置
在 `.env` 文件中配置豆包 AI：

```env
DOUBAO_API_KEY=your_api_key
DOUBAO_ENDPOINT_ID=your_endpoint_id
```

## 🚀 快速开始

1. 克隆项目
```bash
git clone <repository-url>
cd bishe_first
```

2. 后端启动
```bash
pip install -r requirements.txt
python manage.py migrate
python init_sample_data.py
python manage.py runserver
```

3. 前端启动
```bash
npm install
npm run dev
```

4. 访问系统
- 前端：http://localhost:5173
- 后端：http://127.0.0.1:8000
- Django 管理后台：http://127.0.0.1:8000/admin

## 👤 测试账号

系统提供以下测试账号（通过 `init_sample_data.py` 初始化）：

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 系统管理员 |
| 教师 | t1 | t123 | 教师账号 |
| 学生 | s1 | s123 | 学生账号 |

## 📁 项目结构

```
bishe_first/
├── campus_platform/     # Django 项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主路由配置
│   └── wsgi.py          # WSGI 配置
├── users/               # 用户管理应用
├── courses/             # 课程资源应用
├── forum/               # 论坛应用
├── announcements/       # 公告应用
├── points/              # 积分应用
├── ai/                  # AI 服务应用
├── src/                 # Vue 前端源码
│   ├── components/      # 组件
│   │   ├── admin/       # 管理员端组件
│   │   ├── teacher/     # 教师端组件
│   │   ├── student/     # 学生端组件
│   │   ├── common/      # 公共组件
│   │   └── icons/       # 图标组件
│   ├── layouts/         # 布局组件
│   ├── router/          # 路由配置
│   ├── stores/          # Pinia 状态管理
│   ├── composables/     # Vue 组合式函数
│   ├── utils/           # 工具函数
│   ├── styles/          # 样式文件
│   ├── App.vue          # 根组件
│   └── main.ts          # 入口文件
├── manage.py            # Django 管理脚本
├── requirements.txt     # Python 依赖
├── package.json         # Node.js 依赖
├── vite.config.ts       # Vite 配置
├── tsconfig.json        # TypeScript 配置
├── start.sh             # 一键启动脚本
├── stop.sh              # 停止服务脚本
└── README.md            # 项目说明
```

详细的项目文件目录及作用请查看 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。

## 📝 开发说明

### API 文档
后端使用 Django REST Framework，访问 `/api/` 查看可浏览的 API 界面。

### 数据库管理
```bash
# 创建新迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations
```

### 前端开发
```bash
# 开发模式
npm run dev

# 类型检查
npx vue-tsc --noEmit

# 构建生产版本
npm run build
```

## 🎨 设计特点

- **响应式布局**: 支持多种屏幕尺寸，移动端友好
- **现代化 UI**: 采用 Element Plus 组件库，美观易用
- **全局 Toast**: 统一的消息提示组件，屏幕中央显示，自动消失
- **加载动画**: 优雅的加载状态和骨架屏
- **主题定制**: 支持自定义主题色和样式变量

## 🔐 安全特性

- **JWT 认证**: 无状态的 token 认证机制
- **权限控制**: 基于角色的访问控制（RBAC）
- **CORS 配置**: 跨域请求安全控制
- **密码加密**: Django 内置的密码哈希机制

## 📊 数据库模型

主要数据模型包括：

- **User**: 用户（管理员、教师、学生）
- **CourseType**: 课程类型
- **CourseResource**: 课程资源
- **ResourceCollection**: 资源收藏
- **ResourceComment**: 资源评论
- **ForumPost**: 论坛帖子
- **ForumComment**: 帖子评论
- **Announcement**: 公告
- **PointRecord**: 积分记录
- **Prize**: 奖品
- **PrizeExchange**: 奖品兑换记录

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

毕业设计项目

---

**更新时间**: 2026-04-08
