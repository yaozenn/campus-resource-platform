# 校园课程资源共享平台

一个基于 Django + Vue.js 的校园课程资源管理与共享平台。

## 🎯 项目简介

本项目旨在为校园师生提供一个便捷的课程资源共享平台，整合课程资源管理、论坛交流、AI 智能助手等功能。

## ✨ 主要功能

- 👥 **多角色支持**：管理员、教师、学生三种角色
- 📚 **课程资源管理**：上传、下载、收藏课程资源
- 💬 **交流论坛**：师生互动、问题讨论
- 🤖 **AI 智能助手**：集成豆包 AI，提供智能问答服务
- 🎁 **积分系统**：积分兑换、激励用户参与
- 📢 **公告系统**：校园通知、重要信息发布

## 🛠️ 技术栈

### 后端
- Django 4.2
- Django REST Framework
- SQLite/MySQL
- JWT 认证

### 前端
- Vue 3
- TypeScript
- Vite
- Element Plus
- Pinia (状态管理)

### AI 集成
- 豆包 AI (字节跳动火山方舟)

## 📋 部署说明

### 环境要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端部署

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 前端部署

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## ⚙️ 配置说明

### 后端配置
在 `campus_platform/settings.py` 中配置数据库、密钥等。

### 前端配置
创建 `.env` 文件配置 API 地址：
```
VITE_API_BASE=http://127.0.0.1:8000
```

### AI 配置
在 `.env` 文件中配置豆包 AI：
```
DOUBAO_API_KEY=your_api_key
DOUBAO_ENDPOINT_ID=your_endpoint_id
```

## 📁 项目结构

```
bishe_first/
├── campus_platform/     # Django 项目配置
├── users/              # 用户管理应用
├── courses/            # 课程资源应用
├── forum/              # 论坛应用
├── announcements/      # 公告应用
├── points/             # 积分应用
├── ai/                 # AI 服务应用
├── src/                # Vue 前端源码
│   ├── components/     # 组件
│   ├── layouts/        # 布局
│   ├── stores/         # 状态管理
│   └── router/         # 路由配置
└── ...
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
python manage.py runserver
```

3. 前端启动
```bash
npm install
npm run dev
```

4. 访问
- 前端：http://localhost:5173
- 后端：http://127.0.0.1:8000
- 管理后台：http://127.0.0.1:8000/admin

## 👤 默认账号

- 管理员：admin / admin123
- 教师：t1 / t123
- 学生：s1 / s123

## 📝 开发说明

### API 文档
后端使用 Django REST Framework，访问 `/api/` 查看可浏览的 API 界面。

### 前端开发
```bash
# 开发模式
npm run dev

# 代码检查
npm run lint

# 构建
npm run build
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍ 作者

毕业设计项目

---

**更新时间**: 2026-03-19
