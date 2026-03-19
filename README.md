# E2E 自动化测试指南

## 核心说明

**本指南用于本地开发环境中，使用 AI Agent（Claude Code、Open Code 等）进行 E2E 测试。**

### 为什么是本地测试？

| 场景 | 说明 |
|------|------|
| ✅ **本地开发** | 前后端都在本地运行，可直接调试 |
| ✅ **功能验证** | 开发完成后快速验证功能是否正常 |
| ✅ **BUG 修复** | 修复后立即验证，无需等待部署 |
| ✅ **快速反馈** | 发现问题立即定位和修复 |
| ❌ **生产环境** | 环境不同，不适用本指南 |
| ❌ **CI/CD** | 需要额外配置，参考专门的 CI/CD 文档 |

### AI Agent 的三大作用

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 📝 AI 生成测试用例                                            │
│     → 告诉 AI 功能需求，自动生成测试用例文档                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. ▶️ AI 执行测试                                                 │
│     → AI 解析测试用例，自动调用 playwright-cli 执行                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. 🔧 AI 自动修复 BUG                                             │
│     → 测试失败时，AI 自动定位问题并修复代码                        │
└─────────────────────────────────────────────────────────────────┘
```

### 核心优势

| 优势 | 说明 |
|------|------|
| **无需写代码** | 用自然语言描述测试步骤 |
| **AI 自动生成** | 告诉功能需求，AI 自动生成测试用例 |
| **AI 自动执行** | AI 解析测试用例，自动执行测试 |
| **AI 自动修复** | 测试失败时 AI 自动定位并修复问题 |
| **断点续传** | 支持保存进度，中断后可继续执行 |

---

## 目录

- [1. 环境准备](#1-环境准备)
- [2. AI 生成测试用例](#2-ai-生成测试用例)
- [3. AI 执行测试](#3-ai-执行测试)
- [4. AI 自动修复 BUG](#4-ai-自动修复-bug)
- [5. 进度管理](#5-进度管理)
- [6. 完整工作流程](#6-完整工作流程)
- [7. 常见问题](#7-常见问题)

---

## 1. 环境准备

### 1.1 安装 Playwright CLI

```bash
# 全局安装（只需一次）
npm install -g @playwright/cli@latest

# 验证安装
playwright-cli --help

# 安装 AI 技能（供 AI Agent 使用）
playwright-cli install --skills
```

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318104705186.png" alt="image-20260318104705186" style="zoom:50%;" />

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318104924819.png" alt="image-20260318104924819" style="zoom: 25%;" />

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318105006755.png" alt="image-20260318105006755" style="zoom:50%;" />

### 1.2 确认服务运行

```bash
# 确认前后端服务在本地运行
# 前端：http://localhost:3000
# 后端：http://localhost:8080

# 健康检查
curl http://localhost:8080/health
```

### 1.3 创建测试目录

```bash
# 在项目根目录创建测试目录
mkdir -p e2e/test-cases/auth
mkdir -p e2e/test-cases/user
mkdir -p e2e/progress
mkdir -p e2e/reports
mkdir -p e2e/screenshots/success
mkdir -p e2e/screenshots/failure
```

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318105744198.png" alt="image-20260318105744198" style="zoom:50%;" />



### 1.4 配置运行环境

复制并修改运行环境配置：

```bash
# 复制样例到项目
cp docs/autotest/samples/running-environment.md ./

# 根据项目修改服务地址、端口、测试账号等
```

---

## 2. AI 生成测试用例

### 2.1 生成方式

**方式1：根据功能描述生成**

项目终端启动claude，模板如下，需求也可以给agent文件路径让它自己整理

```
请根据以下功能需求生成 E2E 测试用例：

功能：用户登录
需求：
1. 正常登录成功
2. 密码错误提示
3. 空用户名验证
4. 账号锁定处理

要求：
- 按照 E2E测试标准.md 的格式编写
- 包含测试编号
- 每个用例包含步骤、验证、清理
- 保存到 E:\E2E-Autotest\samples\e2e\test-cases\auth\login.md
```

这里我给的是AuthController文件路径让agent自己整理

![image-20260318114018152](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318114018152.png)

这就是claude基于我输入的自然语言提示词生成的测试md，可以发现它还读取了running-environment的信息

![image-20260318115022850](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318115022850.png)

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318115254375.png" alt="image-20260318115254375" style="zoom:50%;" />

再来一个UserController的

![image-20260318115704318](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318115704318.png)

![image-20260318121027715](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318121027715.png)

![image-20260318121048753](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318121048753.png)

**方式2：根据现有页面生成**

```
请访问 http://localhost:3000/login，分析登录页面后生成测试用例：
- 覆盖正常和异常场景
- 包含字段验证测试
- 添加截图步骤
```

### 2.2 测试用例模板

生成的测试用例应遵循以下格式：

```markdown
# {功能}测试

**优先级**: P0
**模块**: {模块名}

## 用例1: {用例名称}
**编号**: {模块}_{操作}_{场景}_{类型}_{序号}

### 步骤
1. 打开页面
2. 点击元素
3. 输入内容

### 验证
- 验证点1
- 验证点2

### 清理
- 清理操作
```

### 2.3 参考样例

详细样例参考 `samples/e2e/test-cases/`：
- `samples/e2e/test-cases/auth/login.md`
- `samples/e2e/test-cases/user/user-test.md`

---

## 3. AI 执行测试

### 3.1 单个测试文件

告诉claude：

```
使用 playwright-cli 执行 e2e/test-cases/auth/login.md：
- 有头模式（--headed），可以看到浏览器操作
- 每个用例执行后截图
- 失败时停止执行
- 生成测试报告到 e2e/reports/
```

测试过程会自动打开登录页面，去模拟真实的测试流程

![image-20260318121958874](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318121958874.png)

![image-20260318122005963](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318122005963.png)

![image-20260318131046024](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318131046024.png)

打开执行测试报告可以看到用例执行详情

![image-20260318131336712](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318131336712.png)

截图情况

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318131452282.png" alt="image-20260318131452282" style="zoom:50%;" />

### 3.2 批量执行

先给剩下模块生成测试用例md

![image-20260318142451932](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318142451932.png)

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318143321405.png" alt="image-20260318143321405" style="zoom:50%;" />

创建 `e2e/run-all-tests.md`：

```markdown
# 批量执行

## 执行顺序
E:\E2E-Autotest\samples\e2e\test-cases\alarm\alarm-test.md                                                                                                            
E:\E2E-Autotest\samples\e2e\test-cases\artwork\artwork-test.md                                                                                                        
E:\E2E-Autotest\samples\e2e\test-cases\monitor\monitor-test.md                                                                                                        
E:\E2E-Autotest\samples\e2e\test-cases\trade\trade-test.md   

## 配置
- 会话名：test-session
- 进度文件：e2e/progress/test-progress.txt
```

![image-20260318143937566](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318143937566.png)

然后执行：

```
执行 e2e/run-all-tests.md 中指定的所有测试用例
```

这里全部执行要耗时较久，claude5分钟执行结束，挑了p0的执行。平时测试时可以尽量单职责测试，避免消耗过多token

![image-20260318151403391](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318151403391.png)

+ 这里也可以使用subAgent来进行测试，相当于你有5个测试工程师，claude分配测试任务给这5个子代理

```
E:\E2E-Autotest\samples\running-environment.md E:\E2E-Autotest\E2E测试标准.md,参考这些文档,使用5个SubAgent手动执行使用 playwright-cli 执行 E:\E2E-Autotest\samples\e2e\run-all-tests.md 中指定的所有测试用例
- 有头模式（--headed），可以看到浏览器操作
- 每个用例执行后截图
- 失败时停止执行
- 生成测试报告到 e2e/reports/
注意, 主Agent只管分配任务, 每次给子代理分配一个未测试md的任务, 你要给子代理强调使用CLI, 使用 playwright cli 根据md文件中的说明, 一步一步操作完成测试, 先完成功能测试, 再测试性能 限流等其它非功能测试用例
```

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318160151878.png" alt="image-20260318160151878" style="zoom:50%;" />

这里开了四个浏览器,说明四个子代理是并行测试的

![image-20260318160220284](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318160220284.png)

注意:这里项目可能会出现API速率限制,导致某个子代理执行失败,建议排查前端请求数显示、反向代理的limit_req、redis连接数、浏览器同域名并发连接数限制等等。建议平时还是单个测试模块为单元串行执行

### 3.3 断点续传

假如突然断开了测试，可以根据test-progress.txt文件直接跳到断开点开测

```
执行 e2e/test-cases/ 目录下的所有测试：
1. 读取 e2e/progress/test-progress.txt
2. 跳过状态为 PASS 的测试
3. 从第一个空状态的测试开始执行
4. 每个测试执行后更新进度
5. 失败时保存 FAIL 状态，可选择是否继续
```

### 3.4 执行流程图

```
启动 → 读取进度 → 跳过已通过 → 执行新测试 → 更新进度
                                              ↓
                                          失败？
                                            ↓     ↓
                                          是    否
                                          ↓     ↓
                                  收集日志 → 继续执行
```

最后看看测试报告

---

## 4. AI 自动修复 BUG

### 4.1 修复流程

前置条件：

这里新生成几个功能接口模拟实际需求，然后在接口内部出点逻辑bug

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318172557798.png" alt="image-20260318172557798" style="zoom:50%;" />

![image-20260318171524462](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318171524462.png)

然后生成了测试用例

![image-20260318171604915](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318171604915.png)

当测试失败时，AI Agent 自动执行以下流程：

```
1. 收集信息
   - playwright-cli console error    # 浏览器错误
   - playwright-cli network         # 网络请求
   - tail -50 logs/api.log           # 后端日志
   - docker compose logs mysql       # 数据库日志

2. 分析问题
   - 确定问题类型（前端/后端/数据）
   - 定位问题代码位置
   - 分析根本原因

3. 自动修复
   - 前端问题：修改组件代码
   - 后端问题：修改 handler/service
   - 数据问题：更新测试数据

4. 验证修复
   - 重新执行失败的测试
   - 确认通过后继续
```

### 4.2 给 AI 的修复提示

测试失败时，使用以下提示：

```
E2E 测试失败，请按以下流程自动修复：

1. 查看测试报告：cat e2e/reports/TEST-REPORT-*.md
2. 收集失败信息：
   - playwright-cli console error
   - playwright-cli network
   - tail -50 logs/api.log
3. 分析并修复问题
4. 重新执行失败的测试用例
5. 确认通过后继续执行其他测试
```

![image-20260318172343110](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318172343110.png)

ok,它发现了上面截图的那个bug

![image-20260318174001592](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318174001592.png)

哈哈，它的修复是将获取排序按降序，这样就是第一个元素是最高价了

![image-20260318174515897](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318174515897.png)

![image-20260318174524881](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318174524881.png)

![image-20260318174458324](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318174458324.png)

重启一下项目，claude会重新执行失败的用例，测试成功！

![image-20260318175516951](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318175516951.png)

测试报告也生成了，由于这里的bug是随机生成，没有相应页面的，所以没有截图

![image-20260318175722430](C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318175722430.png)

### 4.3 参考环境信息

日志查询参考 `samples/running-environment.md`：

| 信息 | 来源 |
|------|------|
| 服务地址 | running-environment.md |
| 测试账号 | running-environment.md |
| 日志位置 | running-environment.md |

---

## 5. 进度管理

### 5.1 进度文件

**e2e/progress/test-progress.txt**:

```
# 格式：{编号} {状态} {时间}
auth_login_normal_1 PASS 2026-03-16_14:30:15
auth_login_err_pwd_1
user_edit_basic_1
```

**状态说明**：
- `PASS` - 已通过
- `FAIL` - 失败
- 空 - 未执行

<img src="C:\Users\redteamobile\AppData\Roaming\Typora\typora-user-images\image-20260318151305950.png" alt="image-20260318151305950" style="zoom:50%;" />

### 5.2 进度命令

```bash
# 查看进度
cat e2e/progress/test-progress.txt

# 查看失败的测试
grep FAIL e2e/progress/test-progress.txt

# 查看未执行的测试
grep -E '^[^_]+_[^_]+_[^_]+_[^_]+_\d+ *$' e2e/progress/test-progress.txt

# 统计进度
echo "通过: $(grep -c PASS e2e/progress/test-progress.txt)"
echo "失败: $(grep -c FAIL e2e/progress/test-progress.txt)"

# 重试失败的测试
sed -i 's/FAIL.*$/ /' e2e/progress/test-progress.txt

# 完全重置
rm e2e/progress/test-progress.txt
```

### 5.3 AI 自动生成进度

```
首次执行时，如果进度文件不存在：
1. AI 扫描所有测试用例文件
2. 提取每个用例的编号
3. 生成初始进度文件（所有状态为空）
4. 开始执行测试
```

---

## 6. 完整工作流程

### 6.1 首次测试

```
1. 启动前后端服务
2. 告诉 AI："请根据用户登录功能生成测试用例"
3. AI 生成 e2e/test-cases/auth/login.md
4. 告诉 AI："执行这个测试文件"
5. AI 执行测试，生成报告
```

### 6.2 日常测试

```
1. 修改代码后
2. 告诉 AI："执行 e2e/test-cases/user/ 的测试，验证修改"
3. AI 执行测试
4. 如果失败，AI 自动修复
5. 验证通过后继续
```

### 6.3 回归测试

```
1. 告诉 AI："执行所有测试用例，生成测试报告"
2. AI 按顺序执行所有测试
3. 生成完整测试报告
4. 标注失败的测试
```

---

## 7. 常见问题

### Q1: playwright-cli 命令不生效？

**A**: AI 不了解命令用法，提示 AI：
```
请参考 Playwright CLI 官方文档：
https://github.com/microsoft/playwright-cli
或查看本地帮助：playwright-cli --help
```

### Q2: 测试失败后如何继续？

**A**: 方式1 - 修复后重试：
```bash
sed -i 's/FAIL.*$/ /' e2e/progress/test-progress.txt
```

方式2 - 跳过失败的测试：
```
跳过状态为 FAIL 的测试，继续执行剩余测试
```

### Q3: 如何只测试特定模块？

**A**: 告诉 AI：
```
只执行 e2e/test-cases/user/ 目录下的测试
```

### Q4: 如何查看测试报告？

**A**:
```bash
cat e2e/reports/TEST-REPORT-*.md
```

### Q5: 测试用例编号怎么定？

**A**: 格式为 `{模块}_{操作}_{场景}_{类型}_{序号}`，例如：
- `auth_login_normal_1` - 认证-登录-正常流程-第1个
- `user_edit_err_notfound_1` - 用户-编辑-不存在错误-第1个

---

## 8. 参考文档

| 文档 | 说明 |
|------|------|
| `E2E测试标准.md` | 完整的测试标准规范 |
| `samples/README.md` | 样例文件说明 |
| `samples/running-environment.md` | 运行环境配置 |
| `samples/e2e/test-cases/` | 测试用例样例 |
| [Playwright CLI GitHub](https://github.com/microsoft/playwright-cli) | 官方文档 |

---

## 9. AI Agent 提示词模板

### 9.1 生成测试用例提示词

**使用场景**：首次生成测试用例，或新增功能模块时使用。

**使用方法**：在 Claude Code 中使用 `/loop 1m` 循环执行

```
docs/design/*.md running-environment.md e2e/E2E测试标准.md, e2e/progress/(测试进度目录), 参考这些文档, 以及测试用例标准以及目录结构, 生成每个模块的详细测试用例, 注意已经存在的测试用例(test-progress.txt)不要重复生成, 需要覆盖基本功能路径, 以及其它有可能的操作路径. 并生成所有测试用户到 progress/test-progress.txt 文件中.
```

**说明**：
- AI 会自动扫描项目，分析功能模块
- 参考 E2E测试标准.md 生成测试用例
- 检查现有进度，避免重复生成
- 覆盖正常路径 + 异常路径 + 边界条件
- 自动生成初始进度文件

### 9.2 执行测试用例提示词

**使用场景**：代码修改后验证功能，或执行完整测试时使用。

**使用方法**：在 Claude Code 中使用 `/loop 1m` 循环执行

```
docs/design/*.md running-environment.md e2e/E2E测试标准.md, e2e/progress/(测试进度目录), 参考这些文档, 使用5个SubAgent手动执行已经生成好的e2e测试用例, 不要输出报告, 有bug的, 务必定位问题并修复bug, 测试通过的测试用例, 简单记录到一个文档中就行了(e2e/progress/目录下), 注意, 使用的是 playwright cli, 不是playwright mcp. 主Agent只管分配任务, 每次给子代理分配一个未测试的任务, 你要给子代理强调使用CLI, 不是MCP, 所有测试用例在 e2e/test-cases 目录下, 每个文件一个测试用例, 你直接读取文件就行, 不要读取文件内容, 免得占上下文, 且禁止切换到MCP模式, 禁止创建ts格式的测试用例, 读取 e2e/test-cases/**/*.md  使用 playwright cli 根据md文件中的说明, 一步一步操作完成测试, 先完成功能测试, 再测试性能 限流等其它非功能测试用例
```

**说明**：
- 使用 5 个 SubAgent 并行执行测试
- 每个测试用例独立分配给一个子代理
- 主 Agent 只负责任务分配，不执行测试
- 子代理使用 **playwright-cli**（不是 MCP）
- 自动定位并修复 BUG
- 通过的测试简单记录到进度目录
- 不输出冗长的测试报告

### 9.3 提示词使用示例

**示例1：生成登录模块测试用例**

```
docs/design/*.md running-environment.md e2e/E2E测试标准.md, 参考这些文档, 为认证模块生成详细的 E2E 测试用例：
- 正常登录
- 密码错误
- 空用户名
- 账号锁定
- 退出登录

生成到 e2e/test-cases/auth/login.md
并更新进度文件 e2e/progress/test-progress.txt
```

**示例2：执行所有测试**

```
docs/design/*.md running-environment.md e2e/E2E测试标准.md, 使用5个SubAgent执行e2e/test-cases目录下的所有测试用例
```

**示例3：只执行失败的测试**

```
查看 e2e/progress/test-progress.txt 中状态为空的测试, 使用5个SubAgent执行这些测试
```

---

## 10. 快速参考
