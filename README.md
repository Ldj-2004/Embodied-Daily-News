# 具身智能日报

每天自动收集国内外具身智能新闻，筛选并生成恰好五条中文日报，自动截取原网页并生成实验室大屏轮播页面。

项目刻意不为每个网站维护爬虫，而是使用 RSS、Google News RSS 查询和 arXiv 作为候选来源。模型只负责从候选中选择、去重和编辑；最终链接、来源和发布时间均由程序从原始候选回填。

## 最终输出

日报只列出五条新闻，不显示“重点”“模型”“产品”等分类标题。每条包含：

1. 中文标题与原文链接；
2. 简短事实摘要；
3. 为什么重要；
4. 原始来源。

运行后会生成：

- `output/YYYY-MM-DD.md`：当天 Markdown 日报；
- `output/YYYY-MM-DD.json`：当天结构化数据；
- `output/latest.md` 与 `output/latest.json`：最新日报；
- `data/state.json`：跨天去重状态。

## 工作流程

```text
RSS / Google News RSS / arXiv
              ↓
 当天新闻 / 最近 arXiv 更新日论文
              ↓
        URL 与相似标题去重
              ↓
   模型选出并编辑恰好五条
              ↓
 Markdown / JSON / 网页截图 / 大屏页面
```

单个信源无法访问时会被记录并跳过，不会中断其他信源。抓取状态保存在本地的 `output/source-health.json`，该诊断文件默认不提交到 Git。

## 本地安装

需要 Python 3.11 或更高版本。

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
```

## 配置模型 API

打开本地 `.env`，填写：

```dotenv
OPENAI_API_KEY=在这里填写你的sk密钥
OPENAI_BASE_URL=http://35.220.164.252:3888/v1/
OPENAI_MODEL=gpt-4o-mini
```

如果服务商提供的模型名不是 `gpt-4o-mini`，请修改 `OPENAI_MODEL`。项目使用 OpenAI 兼容的 `chat/completions` 接口。

如果改用 DeepSeek，代码无需修改，只需把本地 `.env` 改成：

```dotenv
OPENAI_API_KEY=你的DeepSeek密钥
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-flash
```

这里沿用 `OPENAI_` 环境变量名，是因为项目调用的是 OpenAI 兼容接口；密钥本身仍然是 DeepSeek 密钥。不要把真实密钥写入源码或 `.env.example`。

如果改用中国区 Kimi/Moonshot API：

```dotenv
OPENAI_API_KEY=你的Kimi密钥
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=kimi-k3.1-pro-highspeed
```

不同账号可用模型可能不同，可运行 `python scripts/check_api_models.py --probe` 查看模型列表并做一次最小调用测试。本项目本次实测账号使用 `kimi-k3.1-pro-highspeed` 可以完成生成。

### HTTP 安全警告

指定地址使用 `http://` 而不是 `https://`。这意味着 API 密钥和请求内容可能在传输过程中被窃听或篡改。强烈建议先向服务提供方索取 HTTPS 地址。

项目默认拒绝把密钥发送到 HTTP 地址。如果你确认信任该网络和服务商并明确接受风险，才在 `.env` 中设置：

```dotenv
ALLOW_INSECURE_API_BASE=true
```

`.env` 已被 `.gitignore` 排除，不能把真实密钥写入 `.env.example`、源码或提交记录。

## 先运行无密钥演示

以下命令不联网、不调用模型，也不发送飞书，用于检查最终五条 UI：

```bash
python -m embodied_daily --demo --skip-feishu
```

查看 `output/latest.md`。确认格式后再运行真实流程：

```bash
python -m embodied_daily --skip-feishu
```

## 生成当前测试版大屏

安装 Chromium（只需执行一次）：

```bash
python -m playwright install chromium
```

生成五条已核实测试新闻、网页截图和静态站点：

```bash
python scripts/generate_test_showcase.py
```

启动本地预览：

```bash
python -m http.server 8000 --directory dist
```

浏览器打开 `http://127.0.0.1:8000`。页面以 35:65 的统一布局展示中文概述和原网页首屏，自动每 18 秒切换，支持左右方向键与空格暂停。

测试版日期固定为 `2026-10-30`；正式日报由每日任务写入当天日期。网页截图失败时会自动生成本地占位图，不会阻断站点构建。

如果只想检查 RSS 和搜索源，不调用模型也不发送飞书：

```bash
python -m embodied_daily --check-sources
```

详细结果会写入 `output/source-health.json`。

调试时如需忽略历史去重：

```bash
python -m embodied_daily --skip-feishu --ignore-state
```

## 接入飞书

1. 新建一个飞书测试群；
2. 进入群设置，添加“自定义机器人”；
3. 复制 Webhook 地址；
4. 建议开启签名校验，并复制签名密钥；
5. 在本地 `.env` 中填写：

```dotenv
FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/你的地址
FEISHU_SECRET=你的签名密钥
```

随后运行：

```bash
python -m embodied_daily
```

没有配置 `FEISHU_WEBHOOK` 时，程序仍会正常生成本地日报，只是不发送消息。

## 日期与论文规则

- 普通新闻按 `Asia/Shanghai` 时区允许日报当天或前一天发布，以覆盖中美时差；
- 五条中固定包含两篇 arXiv 论文和三条产业、产品或机构新闻；
- 当天有 arXiv 更新时只使用当天论文；当天没有更新时，使用抓取结果中最近一次更新日的论文；
- arXiv 通常在美东时间周日至周四 20:00 发布，周五、周六不发布，因此任务统一安排在北京时间 09:30 之后运行。

如果两日内普通新闻不足三条，或最近更新日的论文不足两篇，任务会明确失败并保留诊断信息，而不是悄悄违反日期规则。

## 上传 GitHub 后自动运行

仓库内的 `.github/workflows/daily.yml` 会：

- 每天北京时间 09:30 自动执行，确保位于 arXiv 当次发布之后；
- 支持在 GitHub Actions 页面手动触发；
- 生成日报并截取五个原网页首屏；
- 某条新闻无法生成有效网页截图时，自动淘汰该候选并换成截图可用的同类新闻；
- 普通新闻优先企业产品、模型、量产交付和真实部署，降低政策、宏观投资、赛事论坛及纯融资消息的权重；
- 对最终五条内容进行第二次 API 精读总结，使大屏文字信息更完整；
- 模型选稿只发送最高分的精简候选；API 超时或限流时自动使用确定性排序，避免整次日报失败；
- 论文不再展示 arXiv 摘要页，而是优先截取论文 HTML 正文中尺寸合适的代表性图表；
- 构建并发布 GitHub Pages 大屏站点；
- 飞书配置为可选项，未配置时不会影响大屏；
- 将日报和去重状态提交回仓库。

当前工作流已经固定使用 Kimi 中国区接口和 `kimi-k3.1-pro-highspeed`，因此只需要在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加密钥：

### Secrets

| 名称 | 内容 |
|---|---|
| `OPENAI_API_KEY` | 你的 `sk-...` 密钥 |
| `FEISHU_WEBHOOK` | 飞书自定义机器人 Webhook |
| `FEISHU_SECRET` | 飞书机器人签名密钥；未启用签名时可不填 |

首次配置后，在 **Actions → Daily embodied intelligence digest → Run workflow** 手动运行一次。确认日报和飞书消息都正确，再等待定时任务。

首次发布大屏前，还需要在 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。

如果仓库设置禁止 GitHub Actions 写入，请在 **Settings → Actions → General → Workflow permissions** 中允许 Read and write permissions。

## 调整信源与筛选范围

- `config/sources.yaml`：RSS、arXiv 和 Google News 查询；
- `config/settings.yaml`：关键词、时间范围、候选数量和并发设置；
- `src/embodied_daily/llm.py`：编辑标准与 JSON 输出约束。

建议先连续运行七天，再根据漏报和误报调整词表。只有长期漏掉某个关键来源时，才增加新的专用接入方式。

## 测试

```bash
pytest
ruff check .
```

测试不会调用外部 API，也不会向飞书发送消息。

## 数据与版权

本项目默认只保存标题、短摘要、时间和原文链接，不复制整篇新闻。自动摘要可能存在错误，正式引用和重要决策请回到原始来源核实。

## 腾讯云 CloudBase 国内大屏部署

工作流会在生成 `dist/` 后自动发布到 CloudBase 静态网站托管。只有下列三个
GitHub Actions Secrets 全部存在时才执行，未配置时会自动跳过且不影响 GitHub Pages：

- `TCB_SECRET_ID`：专用腾讯云 CAM 子用户的 SecretId
- `TCB_SECRET_KEY`：该子用户的 SecretKey
- `TCB_ENV_ID`：CloudBase 环境 ID

账号侧需要先创建 CloudBase 环境并开通静态网站托管，再为专用 CAM 子用户授予
云开发部署权限。不要把密钥写入仓库、日志、Issue 或聊天。部署使用
`--safe --verify --prune`：发布失败时回滚、上传后校验，并清理上一版遗留文件。

