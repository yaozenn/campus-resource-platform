# 项目文件目录及作用说明

本文档详细说明了校园课程资源共享平台项目的各个文件和目录的作用。

## 📁 项目根目录

| 文件/目录 | 说明 |
|----------|------|
| `manage.py` | Django 管理脚本，用于运行服务器、数据库迁移等 |
| `requirements.txt` | Python 依赖包列表 |
| `package.json` | Node.js 项目配置和依赖 |
| `package-lock.json` | Node.js 依赖版本锁定文件 |
| `vite.config.ts` | Vite 构建工具配置 |
| `tsconfig.json` | TypeScript 编译配置 |
| `tsconfig.node.json` | Node.js 环境 TypeScript 配置 |
| `index.html` | Vite 入口 HTML 文件 |
| `start.sh` | 一键启动后端和前端的脚本 |
| `stop.sh` | 停止后端和前端服务的脚本 |
| `README.md` | 项目说明文档 |
| `PROJECT_STRUCTURE.md` | 本文档，项目结构说明 |
| `.gitignore` | Git 忽略文件配置 |
| `.env.production` | 生产环境配置文件 |
| `init_sample_data.py` | 初始化示例数据的脚本 |
| `init_test_data.py` | 初始化测试数据的脚本 |
| `create_default_types.py` | 创建默认课程类型的脚本 |
| `reset_test_users.py` | 重置测试用户的脚本 |
| `check_data.py` | 数据检查脚本 |
| `cleanup_old_data.py` | 清理旧数据的脚本 |
| `get-pip.py` | pip 安装脚本 |
| `backup_data.json` | 数据备份文件 |
| `backend.pid` | 后端进程 PID 文件（运行时生成） |
| `frontend.pid` | 前端进程 PID 文件（运行时生成） |

---

## 🐍 后端 Django 应用

### campus_platform/ - Django 项目配置

| 文件 | 说明 |
|------|------|
| `__init__.py` | Python 包标识文件 |
| `settings.py` | **核心配置文件**，包含数据库、应用、中间件、JWT、CORS 等配置 |
| `urls.py` | **主路由配置**，定义所有 API 端点的路由 |
| `wsgi.py` | WSGI 配置，用于生产环境部署 |
| `views.py` | 项目级视图函数 |

### users/ - 用户管理应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | **用户模型定义**，包含 User 模型（管理员、教师、学生） |
| `users_serializers.py` | **用户序列化器**，用于 API 数据转换 |
| `views.py` | **用户视图**，处理登录、注册、用户信息等请求 |
| `urls.py` | 用户相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### courses/ - 课程资源应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | **课程资源相关模型**：<br>- CourseType（课程类型）<br>- CourseResource（课程资源）<br>- ResourceCollection（资源收藏）<br>- ResourceComment（资源评论） |
| `serializers.py` | **课程资源序列化器** |
| `views.py` | **课程资源视图**，处理资源上传、下载、收藏、评论等 |
| `urls.py` | 课程资源相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### forum/ - 论坛应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | **论坛相关模型**：<br>- ForumPost（论坛帖子）<br>- ForumComment（帖子评论） |
| `serializers.py` | **论坛序列化器** |
| `views.py` | **论坛视图**，处理发帖、评论、浏览量等 |
| `urls.py` | 论坛相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### announcements/ - 公告应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | **公告模型**（Announcement） |
| `serializers.py` | **公告序列化器** |
| `views.py` | **公告视图**，处理公告发布、查看等 |
| `urls.py` | 公告相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### points/ - 积分应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | **积分相关模型**：<br>- PointRecord（积分记录）<br>- Prize（奖品）<br>- PrizeExchange（奖品兑换记录） |
| `serializers.py` | **积分序列化器** |
| `views.py` | **积分视图**，处理积分获取、兑换等 |
| `urls.py` | 积分相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### ai/ - AI 服务应用

| 文件/目录 | 说明 |
|----------|------|
| `__init__.py` | Python 包标识文件 |
| `models.py` | AI 相关模型 |
| `views.py` | **AI 视图**，处理豆包 AI 问答请求 |
| `urls.py` | AI 相关路由配置 |
| `admin.py` | Django 管理后台配置 |
| `apps.py` | 应用配置 |
| `tests.py` | 测试文件 |
| `migrations/` | 数据库迁移文件目录 |

### backend/ - 后端其他模块

| 文件/目录 | 说明 |
|----------|------|
| `campus_resource/views_search.py` | 资源搜索相关视图 |

---

## 🎨 前端 Vue 应用 (src/)

### src/components/ - 组件目录

#### src/components/admin/ - 管理员端组件

| 文件 | 说明 |
|------|------|
| `AdminCourseResourceManagement.vue` | **课程资源管理**，审核、删除资源 |
| `AnnouncementManagement.vue` | **公告管理**，发布、编辑、删除公告 |
| `DataAnalysis.vue` | **数据分析**，查看平台统计数据 |
| `ForumManagement.vue` | **论坛管理**，管理帖子和评论 |
| `ForumOverview.vue` | **论坛概览**，论坛数据统计 |
| `PersonalCenter.vue` | **管理员个人中心** |
| `PointsManagement.vue` | **积分管理**，管理积分和奖品 |
| `ResourceOverview.vue` | **资源概览**，资源数据统计 |
| `StudentManagement.vue` | **学生管理**，管理学生账号 |
| `SystemManagement.vue` | **系统管理** |
| `SystemSettings.vue` | **系统设置** |
| `TeacherManagement.vue` | **教师管理**，管理教师账号 |
| `TypeManagement.vue` | **课程类型管理** |
| `UserOverview.vue` | **用户概览**，用户数据统计 |

#### src/components/teacher/ - 教师端组件

| 文件 | 说明 |
|------|------|
| `AITeacherInsight.vue` | **AI 教师洞察** |
| `Announcements.vue` | **公告查看** |
| `CourseResourceComments.vue` | **资源评论管理**，审核学生评论 |
| `CourseResourceManagement.vue` | **课程资源管理**，上传、编辑资源 |
| `Forum.vue` | **论坛**，参与讨论 |
| `PersonalCenter.vue` | **教师个人中心** |
| `StudentManagement.vue` | **学生管理**，查看学生情况 |

#### src/components/student/ - 学生端组件

| 文件 | 说明 |
|------|------|
| `AIAssistantFloating.vue` | **AI 助手悬浮窗** |
| `AnnouncementDetail.vue` | **公告详情** |
| `Announcements.vue` | **公告列表** |
| `CollectionManagement.vue` | **收藏管理**，管理收藏的资源 |
| `CourseDetail.vue` | **课程资源详情**，查看、下载、收藏、评论资源 |
| `Courses.vue` | **课程资源列表**，浏览、搜索资源 |
| `Forum.vue` | **论坛列表**，浏览帖子 |
| `MyPoints.vue` | **我的积分**，查看积分记录、兑换奖品 |
| `MyUpload.vue` | **我的上传**，管理上传的资源 |
| `PersonalCenter.vue` | **学生个人中心** |
| `PostDetail.vue` | **帖子详情**，查看帖子、发表评论 |

#### src/components/common/ - 公共组件

| 文件 | 说明 |
|------|------|
| `EmptyState.vue` | **空状态组件**，无数据时显示 |
| `FormInput.vue` | **表单输入组件** |
| `GlobalSearch.vue` | **全局搜索组件** |
| `LoadingSpinner.vue` | **加载旋转动画组件** |
| `PageTransition.vue` | **页面过渡动画组件** |
| `PasswordStrength.vue` | **密码强度检测组件** |
| `SkeletonCard.vue` | **卡片骨架屏组件** |
| `SkeletonList.vue` | **列表骨架屏组件** |
| `Toast.vue` | **全局 Toast 组件**，消息提示（屏幕中央显示，自动消失） |

#### src/components/icons/ - 图标组件

| 文件 | 说明 |
|------|------|
| `SvgIcon.vue` | **SVG 图标基础组件** |
| `SvgIcons.vue` | SVG 图标集合 |
| `index.ts` | 图标导出文件 |
| `IconAlertCircle.vue` - `IconZap.vue` | 各种功能图标组件（共 60+ 个） |

#### src/components/ - 其他组件

| 文件 | 说明 |
|------|------|
| `Login.vue` | **登录页面** |
| `Skeleton.vue` | 骨架屏组件 |

### src/layouts/ - 布局组件

| 文件 | 说明 |
|------|------|
| `AdminLayout.vue` | **管理员端布局**，侧边栏、顶部导航 |
| `TeacherLayout.vue` | **教师端布局** |
| `StudentLayout.vue` | **学生端布局** |

### src/router/ - 路由配置

| 文件 | 说明 |
|------|------|
| `router_index.ts` | **路由配置文件**，定义所有页面路由 |

### src/stores/ - Pinia 状态管理

| 文件 | 说明 |
|------|------|
| `aiAssistant.ts` | **AI 助手状态管理** |

### src/composables/ - Vue 组合式函数

| 文件 | 说明 |
|------|------|
| `useToast.ts` | **Toast 服务**，提供全局消息提示功能 |

### src/utils/ - 工具函数

| 文件 | 说明 |
|------|------|
| `request.ts` | **Axios 请求封装**，统一处理 API 请求 |
| `timeFormat.ts` | **时间格式化工具** |
| `validation.ts` | **表单验证工具** |

### src/styles/ - 样式文件

| 文件 | 说明 |
|------|------|
| `variables.css` | **CSS 变量定义**，主题色、间距等 |

### src/ - 根目录文件

| 文件 | 说明 |
|------|------|
| `App.vue` | **根组件**，应用入口组件 |
| `main.ts` | **应用入口文件**，初始化 Vue 应用 |
| `index.css` | **全局样式** |
| `vite-env.d.ts` | Vite 环境类型声明 |

---

## 🗄️ 数据库迁移文件 (migrations/)

各应用的 migrations 目录包含数据库迁移文件，用于管理数据库结构变更：

- `0001_initial.py` - 初始迁移
- `0002_initial.py` - 第二次初始迁移
- `0003_*.py` - 后续字段和模型调整
- `0004_*.py` - 更多调整（如论坛的 views 字段）
- `0005_*.py` - 最新的迁移

---

## 🔑 关键文件速查

| 功能 | 文件路径 |
|------|----------|
| 后端配置 | `campus_platform/settings.py` |
| 后端路由 | `campus_platform/urls.py` |
| 用户模型 | `users/models.py` |
| 课程资源模型 | `courses/models.py` |
| 论坛模型 | `forum/models.py` |
| 前端路由 | `src/router/router_index.ts` |
| 前端入口 | `src/main.ts` |
| 根组件 | `src/App.vue` |
| Toast 组件 | `src/components/common/Toast.vue` |
| Toast 服务 | `src/composables/useToast.ts` |
| API 请求 | `src/utils/request.ts` |

---

## 📝 备注

- 所有后端 API 端点都在 `campus_platform/urls.py` 中统一配置
- 前端组件按角色分类，便于维护
- 数据库迁移文件不要手动修改，应通过 `makemigrations` 生成
- 全局样式变量在 `src/styles/variables.css` 中定义
