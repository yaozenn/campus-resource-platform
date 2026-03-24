# 数据库同步指南

## 📋 为什么数据库文件不同步到 Git？

1. **文件过大**：SQLite 数据库文件可能很大
2. **频繁变化**：每次数据变更都会修改文件，导致大量提交
3. **冲突风险**：多设备同步容易产生冲突
4. **安全问题**：可能包含敏感数据（密码、token 等）

## 🔄 数据库同步方案

### 方案一：使用 Django 数据导出导入（推荐）

#### 在源设备上导出数据

```bash
# 导出所有数据（排除系统表）
python3 manage.py dumpdata --format json --indent 2 \
  --exclude auth.permission \
  --exclude contenttypes \
  --exclude sessions \
  > backup_data.json
```

#### 将导出文件上传到 Git

```bash
git add backup_data.json
git commit -m "Backup database data"
git push
```

#### 在目标设备上导入数据

```bash
# 1. 克隆项目
git clone https://github.com/Kasa1u/campus-resource-platform.git
cd campus-resource-platform

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 导入数据
python manage.py loaddata backup_data.json
```

### 方案二：直接复制数据库文件（适合一次性迁移）

#### 在 macOS 上

```bash
# 找到数据库文件位置
# 通常在 campus_platform/settings.py 中配置

# 复制数据库文件
cp db.sqlite3 db_backup.sqlite3

# 压缩
zip db_backup.zip db_backup.sqlite3
```

#### 传输到 Windows

可以通过以下方式传输：
- 使用 Git（临时添加）
- 使用云盘（百度网盘、iCloud 等）
- 使用 U 盘
- 使用网络传输工具

#### 在 Windows 上

```bash
# 解压并复制数据库文件到项目根目录
# 确保文件名为 db.sqlite3

# 运行迁移
python manage.py migrate
```

### 方案三：使用远程数据库（生产环境推荐）

配置使用 MySQL 或 PostgreSQL 等远程数据库服务：

#### 1. 安装 MySQL 客户端

```bash
pip install mysqlclient
```

#### 2. 修改 settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campus_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_database_host',
        'PORT': '3306',
    }
}
```

#### 3. 导出导入数据库

```bash
# macOS 上导出
mysqldump -u username -p campus_db > backup.sql

# Windows 上导入
mysql -u username -p campus_db < backup.sql
```

## 📝 推荐工作流程

### 日常开发同步

```bash
# 在 macOS 上
# 1. 导出数据库
python3 manage.py dumpdata --format json --indent 2 \
  --exclude auth.permission \
  --exclude contenttypes \
  > data_backup.json

# 2. 提交到 Git
git add data_backup.json
git commit -m "Update database backup"
git push

# 在 Windows 上
# 1. 拉取最新代码
git pull

# 2. 导入数据
python manage.py loaddata data_backup.json
```

### 创建数据库备份脚本

创建 `backup_db.sh`（macOS/Linux）：

```bash
#!/bin/bash
echo "正在备份数据库..."
python3 manage.py dumpdata --format json --indent 2 \
  --exclude auth.permission \
  --exclude contenttypes \
  > backup_$(date +%Y%m%d_%H%M%S).json
echo "备份完成！"
```

创建 `backup_db.bat`（Windows）：

```batch
@echo off
echo 正在备份数据库...
python manage.py dumpdata --format json --indent 2 --exclude auth.permission --exclude contenttypes > backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.json
echo 备份完成！
```

## ⚠️ 注意事项

### 1. 敏感数据处理

导出时排除敏感数据：

```bash
python3 manage.py dumpdata \
  --exclude auth.User \
  --exclude authtoken \
  > public_data.json
```

### 2. 数据冲突解决

如果导入时出现冲突：

```bash
# 清空现有数据
python3 manage.py flush

# 重新导入
python3 manage.py loaddata backup_data.json
```

### 3. 只导出特定应用

```bash
# 只导出 users 应用的数据
python3 manage.py dumpdata users --format json --indent 2 > users_backup.json

# 只导出 courses 应用的数据
python3 manage.py dumpdata courses --format json --indent 2 > courses_backup.json
```

## 🔧 自动化脚本

### 完整同步脚本（macOS）

创建 `sync_to_git.sh`：

```bash
#!/bin/bash

echo "=== 开始同步数据库 ==="

# 备份数据库
BACKUP_FILE="backup_$(date +%Y%m%d).json"
python3 manage.py dumpdata --format json --indent 2 \
  --exclude auth.permission \
  --exclude contenttypes \
  --exclude sessions \
  > $BACKUP_FILE

echo "数据库已备份到 $BACKUP_FILE"

# 添加到 Git
git add $BACKUP_FILE
git commit -m "Database backup: $(date +%Y-%m-%d)"
git push

echo "=== 同步完成 ==="
```

使用：
```bash
chmod +x sync_to_git.sh
./sync_to_git.sh
```

### Windows 导入脚本

创建 `import_data.bat`：

```batch
@echo off
echo === 开始导入数据库 ===

REM 运行迁移
python manage.py migrate

REM 导入数据
python manage.py loaddata backup_data.json

echo === 导入完成 ===
pause
```

## 📊 各方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 数据导出导入 | 安全、灵活、可版本控制 | 需要手动操作 | 日常开发同步 |
| 直接复制文件 | 简单快速 | 文件大、易冲突 | 一次性迁移 |
| 远程数据库 | 实时同步、无需手动操作 | 需要配置、有成本 | 生产环境 |

## 💡 最佳实践

1. **定期备份**：每天或每次重要更新后备份
2. **版本控制**：使用带日期的文件名，如 `backup_20260319.json`
3. **排除敏感数据**：不要导出用户密码、token 等
4. **测试导入**：定期测试备份文件是否可以正常导入
5. **多份备份**：本地、云端、Git 多份备份

---

**推荐**：使用方案一（数据导出导入），这是最安全和可靠的方式！
