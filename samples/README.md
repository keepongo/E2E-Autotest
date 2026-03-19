# 测试用例样例

本目录包含 E2E 测试用例的样例文件，供参考使用。

## 目录结构

```
samples/
├── README.md                  # 样例说明文档
├── running-environment.md     # 运行环境配置（服务地址、中间件、测试账号）
├── run-all-tests.md           # 批量执行配置样例
└── e2e/
    ├── test-cases/            # 测试用例目录
    │   ├── auth/              # 认证模块样例
    │   │   └── login.md
    │   └── user/              # 用户模块样例
    │       ├── user-list.md
    │       ├── user-create.md
    │       └── user-edit.md
    ├── progress/              # 进度文件样例
    │   ├── test-progress.txt          # 当前进度
    │   ├── test-progress-failed.txt   # 包含失败的进度
    │   └── test-progress-initial.txt  # 初始进度（全部未执行）
    ├── reports/               # 测试报告样例
    │   └── TEST-REPORT-20260316-143000.md
    └── screenshots/           # 截图目录
        ├── success/
        └── failure/
```

## 样例文件说明

| 文件 | 说明 |
|------|------|
| `running-environment.md` | **运行环境配置**（服务地址、中间件、测试账号、日志位置） |
| `test-progress.txt` | 正常执行进度（部分通过、部分未执行） |
| `test-progress-failed.txt` | 包含失败记录的进度 |
| `test-progress-initial.txt` | 初始进度（AI 自动生成） |
| `login.md` | 登录功能测试用例 |
| `user-edit.md` | 用户编辑测试用例（单文件多测试用例示例） |
| `TEST-REPORT-*.md` | 测试报告模板 |
| `run-all-tests.md` | 批量执行配置 |

## 使用方法

1. 复制 `running-environment.md` 到项目根目录或 `docs/` 目录
2. 根据项目实际情况修改服务地址、端口、测试账号等
3. 复制测试用例样例到项目 `e2e/test-cases/` 目录
4. 根据项目实际情况修改测试用例内容
5. 执行测试时让 AI Agent 参考运行环境配置

## AI Agent 使用提示

执行测试时，让 AI Agent 读取运行环境配置：

```
执行 e2e/test-cases/auth/login.md 中的测试用例：
1. 参考 docs/autotest/samples/running-environment.md 获取服务地址和测试账号
2. 使用 playwright-cli 连接到 http://localhost:5173
3. 使用测试账号 admin/admin123 登录
4. 按测试用例步骤执行操作
5. 失败时查询后端日志 logs/api.log
```
