# E2E 测试运行环境配置

**更新时间**: 2026-03-16
**测试环境**: 本地开发环境

## 1. 服务地址

| 服务 | 地址 | 端口 | 说明 |
|------|------|------|------|
| 前端应用 | http://localhost | 3000 | Vite 开发服务器 |
| 后端 API | http://localhost | 8080 | Java/Go 后端服务 |
| 健康检查 | http://localhost:8080 | - | GET /health |

## 2. 中间件配置

| 中间件 | 地址 | 端口 | 用户名 | 密码 | 数据库 |
|--------|------|------|--------|------|--------|
| MySQL | localhost | 3306 | root | 123456 | crocodile_security |
| Redis | localhost | 6379 | root | 123456 | - |

## 3. 测试账号

| 用户名 | 密码 | 角色 | 用途 |
|--------|------|------|------|
| admin | 123456 | 系统管理员 | 完整权限测试 |
| ecurity001 | 123456 | 安保人员 | 基础功能测试 |
| buyer001 | 123456 | 买家 | 基础功能测试 |
| seller001 | 123456 | 卖家 | 基础功能测试 |
| buyer001 | 123456 | 普通用户 | 并发测试 |

## 4. 健康检查端点

```bash
# 检查后端服务
curl http://localhost:8080/health

# 检查依赖状态
curl http://localhost:8080/ready

# 查看指标
curl http://localhost:8080/metrics
```

## 5. 日志位置

| 服务 | 日志位置 | 查看命令 |
|------|---------|---------|
| 后端 API | 终端输出 | 查看后端运行终端 |
| MySQL | Docker 日志 | `D:\mysql-8.0.44-winx64\data\redtea.log` |
| Redis | Docker 日志 | `docker logs redis-rr -f` |
| 前端 | 终端输出 | 查看前端运行终端 |

## 6. Docker 服务状态

```bash
# 查看所有服务状态
docker compose ps

# 查看服务日志
docker compose logs

# 启动服务
docker compose up -d

# 停止服务
docker compose down
```

## 7. 浏览器控制台日志查询

使用 playwright-cli 查询：

```bash
# 查看控制台消息
playwright-cli console

# 查看网络请求
playwright-cli network

# 查看错误日志
playwright-cli console error
```

## 8. 测试前检查清单

- [ ] 后端服务正常运行（http://localhost:8080/health）
- [ ] 前端服务正常运行（http://localhost:5173）
- [ ] MySQL 可连接
- [ ] Redis 可连接
- [ ] 测试数据已准备
- [ ] playwright-cli 已安装可用

## 9. 故障排查

| 问题 | 排查方法 |
|------|---------|
| 后端无法启动 | 查看后端运行终端 |
| MySQL 连接失败 | 检查D:\mysql-8.0.44-winx64\data\redtea.log日志 |
| 前端无法访问后端 | 检查 CORS 配置，查看后端日志 |
| 测试失败 | 查看 playwright-cli console 和网络日志 |

## 10. 环境变量

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=  -- 换位自己的数据库

# Redis
REDIS_ADDR=localhost:6379
REDIS_PASSWORD=123456

# 后端
API_PORT=8080
API_MODE=debug

# JWT
JWT_SECRET=
```
