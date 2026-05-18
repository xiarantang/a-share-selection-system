# 🛠️ 常见问题排障指南

> 遇到问题不要慌，这里列出了小白最常见的 10 个问题。按顺序排查即可。
>
> 数据层说明：系统按 **akshare → baostock（~570 条日 K）→ skill_fallback（数据量可能较少）** 三级降级拉取数据。baostock 已内置在安装依赖中，skill_fallback 为可选的第三级兜底。

---

## 1. 双击 `start_ui.command` 没反应 / 闪退

**可能原因**：脚本没有执行权限，或被 macOS 安全策略拦截。

**解决办法**：
1. 右键点击 `start_ui.command` → 选择「打开方式」→「终端」
2. 如果弹出「无法打开，因为无法验证开发者」，去「系统设置 → 隐私与安全性」页面，最底下会有「仍要打开」按钮，点击它
3. 还不行？打开「终端」App，把 `start_ui.command` 文件**拖入终端窗口**，按回车

---

## 2. 提示「未找到 Python3」

**可能原因**：Mac 没有安装 Python，或安装了但系统找不到。

**解决办法**：
1. 打开「终端」App（启动台 → 搜索 Terminal）
2. 输入以下命令，按回车：
   ```
   xcode-select --install
   ```
3. 弹出窗口点击「安装」，等几分钟
4. 安装完成后，去 https://www.python.org/downloads/ 下载 Python 3.9+（下载 macOS 安装包）
5. 双击安装包，一路「继续」安装
6. 重新双击 `start_ui.command`

**如果启动脚本报「pip 安装失败」或「虚拟环境创建失败」**：

- 先确认 Python 版本：打开终端，输入 `python3 --version`，确认显示 3.9 或更高版本
- 如果版本正确但仍失败，打开终端，输入以下命令手动安装依赖：
  ```
  python3 -m pip install --upgrade pip
  cd （把项目文件夹拖入终端）按回车
  python3 -m pip install -r requirements-ui.txt
  ```
- 安装完成后重新双击 `start_ui.command`
- 如果手动安装也失败（比如提示「编译错误」或「架构不匹配」），请截图终端报错发到项目 Issues

---

## 3. 双击 `install_fallback.command` 提示「未找到 Git」（可选的第三级兜底）

**可能原因**：Git 没有安装。

**解决办法**：
- **方法一（推荐）**：打开「终端」，输入 `xcode-select --install`，按提示安装
- **方法二**：打开 https://git-scm.com/download/mac，下载安装
- 安装完成后重新双击 `install_fallback.command`

---

## 4. `install_fallback.command` 下载失败（GitHub 连不上）（可选的第三级兜底）

**可能原因**：网络问题，GitHub 被屏蔽或连接超时。

**解决办法**：
1. 打开浏览器，访问 https://github.com/shouldnotappearcalm/a-share-skill
2. 如果能打开，说明不是 GitHub 问题 → 重试安装脚本
3. 如果打不开，可能是网络限制：
   - 试试换个网络（比如手机热点）
   - 在公司/学校可能需要联系网管
4. **手动安装方法**：在能打开 GitHub 的电脑上，下载 ZIP 解压后，把 `a-share-data`、`a-share-paper-trading` 等文件夹复制到 Mac 的 `~/.agents/skills/` 目录

---

## 5. 浏览器打不开 `http://localhost:8501`

**可能原因**：Streamlit 没有启动成功，或端口不对。

**解决办法**：
1. 确认启动脚本的终端窗口没有关闭（关闭窗口 = 系统停止）
2. 看终端窗口最后一行有没有显示 URL。如果端口不是 8501（比如显示 `localhost:8502`），用对应的端口
3. 如果终端显示「端口被占用」→ 按脚本提示的端口号访问（通常是 8502 或 8503）
4. 如果终端显示「Streamlit 启动失败」→ 看终端里的错误信息，按提示操作
5. **端口被占用？** 试试以下方法（从简单到复杂）：
   - 关闭之前打开的终端窗口，再重新双击启动脚本
   - 重启电脑，然后重新双击启动脚本
   - 如果还不行，打开「终端」，输入 `lsof -ti :8501 | xargs kill -9`（这条命令的作用：关掉占用 8501 端口的旧进程），然后重新双击启动脚本

---

## 6. 点了「开始选股」一直转圈，等了好几分钟

**可能原因**：数据拉取慢，或网络不通。

**解决办法**：
1. 首次选股扫 10 只需要 30-60 秒，这是正常的
2. 如果超过 2 分钟 → 刷新页面（按 F5 或 Cmd+R），重新点击「开始选股」
3. 系统会自动按 **akshare → baostock → skill_fallback** 顺序尝试可用来源。个别数据源慢会让等待变长，但系统会继续尝试下一个来源
4. 如果 baostock 和 akshare 都连不上，系统会降级到第三级兜底（skill_fallback，数据量可能较少），结果仍可参考
5. 如需安装 skill_fallback 兜底通道 → 双击 `scripts/install_fallback.command`

---

## 7. 选股完后结果是空的，或者全部失败

**可能原因**：数据源全部不可用（akshare、baostock 和 skill_fallback 都连不上）。

**解决办法**：
1. 确认电脑能上网（打开浏览器看看能不能打开网页）
2. 重新启动系统（双击 `start_ui.command`），再试一次
3. 如未安装 skill_fallback 兜底通道 → 双击 `scripts/install_fallback.command`（安装后可提供第三级兜底）
4. 如果安装 fallback 也失败了，参考本文第 4 条

---

## 8. 所有股票都标了「覆盖不全」，是不是有问题？

**不是系统坏了。** 正常情况下，系统通过 baostock 拉取约 **570 条**日 K 线，不会出现覆盖不全。

如果看到「覆盖不全」，说明 baostock 和 akshare 都没能连上，系统降级到了第三级兜底（skill_fallback，数据量可能较少）。这不影响你正常使用——系统已经自动降低了评分和置信度，结果仍然可以参考。

**建议**：检查网络连接后重新选股，通常 baostock 会恢复 570 条数据。

---

## 9. 看不懂「决策」「风险等级」「置信度」这些词

| 词 | 白话解释 |
|----|---------|
| **强观察 (strong_watch)** | 评分较高，值得多看几眼 |
| **观察 (watch)** | 有一定亮点，但不够突出 |
| **中性 (neutral)** | 表现平平，没有特别信号 |
| **回避 (avoid)** | 风险较高，建议谨慎 |
| **风险 low / medium / high** | 低 / 中 / 高风险 |
| **置信度** | 评分可不可靠——越高越可靠 |
| **覆盖不全 ⚠️** | 数据量可能较少（降级到了第三级兜底 skill_fallback），评分可能偏高或偏低 |

---

## 10. 不知道怎么开始操作

**操作流程**：

1. **启动**：双击 `start_ui.command` → 浏览器自动打开页面
2. **环境自检**：页面会自动检查 Python、缓存、兜底通道是否就绪（不是报错，只是状态提示）
3. **选参数**：左侧保持默认即可（static 55 只精选 / 扫描 10 只）
4. **选股**：点击页面左侧「🚀 开始选股」→ 等 30-60 秒
5. **看结果**：页面显示排名、评分、风险提示

> **可选**：双击 `scripts/install_fallback.command` 可安装第三级兜底数据通道（skill_fallback），在网络不稳定时多一层保障。系统已内置 baostock（约 570 条日 K），不装 fallback 也能正常使用。

详细图文教程 → [📖 小白使用指南](./USER_GUIDE.md)

---

> 以上问题都解决不了？把终端窗口里的**报错截图**发到项目 Issues：
> https://github.com/xiarantang/a-share-selection-system/issues
