# query_mysql.py 使用指南

## 安装依赖

```bash
pip install pymysql requests
```

## 数据库操作

### 查询数据 (SELECT)
```bash
python scripts/py/query_mysql.py \
  --host localhost \
  --port 3306 \
  --user root \
  --password your_password \
  --database your_db \
  --format table \
  query "SELECT * FROM users LIMIT 10"
```

### 执行语句 (INSERT/UPDATE/DELETE/DDL)
```bash
# INSERT
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "INSERT INTO users (name, email) VALUES ('test', 'test@example.com')"

# UPDATE
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "UPDATE users SET name='newname' WHERE id=1"

# DELETE
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "DELETE FROM users WHERE id=1"

# DDL - CREATE TABLE
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "CREATE TABLE test (id INT PRIMARY KEY, name VARCHAR(100))"

# DDL - ALTER TABLE
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "ALTER TABLE users ADD COLUMN age INT"

# DDL - DROP TABLE
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  execute "DROP TABLE IF EXISTS test"
```

### 显示所有表
```bash
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  --format table \
  tables
```

### 显示表结构
```bash
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  --format table \
  describe users
```

### 显示建表语句
```bash
python scripts/py/query_mysql.py \
  --host localhost --user root --password pwd --database db \
  show-create users
```

## HTTP 请求 (curl)

### GET 请求
```bash
python scripts/py/query_mysql.py curl "https://api.example.com/users"
```

### POST 请求 (JSON)
```bash
python scripts/py/query_mysql.py curl "https://api.example.com/users" \
  -X POST \
  -H "Content-Type: application/json" \
  --json '{"name": "test", "email": "test@example.com"}'
```

### 添加请求头
```bash
python scripts/py/query_mysql.py curl "https://api.example.com/users" \
  -H "Authorization: Bearer your_token" \
  -H "X-Custom-Header: value"
```

## 输出格式

- `--format json` (默认): JSON 格式输出
- `--format table`: 表格格式输出（仅查询）

## 返回格式

### 成功响应
```json
{
  "success": true,
  "data": [...],
  "rowcount": 10,
  "fields": ["id", "name", "email"]
}
```

### 错误响应
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 命令列表

| 命令 | 说明 |
|-----|------|
| `query <sql>` | 执行 SELECT 查询 |
| `execute <sql>` | 执行 INSERT/UPDATE/DELETE/DDL |
| `tables` | 显示所有表 |
| `describe <table>` | 显示表结构 |
| `show-create <table>` | 显示建表语句 |
| `curl <url>` | 执行 HTTP 请求 |

## 使用示例

```bash
# 从环境变量读取密码
export DB_PASSWORD=your_password

python scripts/py/query_mysql.py \
  --host $DB_HOST \
  --user $DB_USER \
  --password $DB_PASSWORD \
  --database $DB_NAME \
  --format table \
  query "SELECT id, username, created_at FROM users WHERE status='active' ORDER BY created_at DESC LIMIT 20"
```
