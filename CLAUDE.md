# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

EduSocratic —— 面向圆桌星球 1-7 年级线上小班思辨课程的 AI 评估系统（2026 AI 先锋未来人才大赛参赛作品）。核心能力：用 LLM 从六个维度量化评估学生思辨能力，通过飞书机器人/卡片打通学生→老师→家长闭环。

**项目仓库根 = 代码根**（仓库根目录 `E:\project\EduSocratic\` 就是 Python 包所在位置，没有额外嵌套）。以下路径均相对于仓库根目录。

## 迭代模式（重要）

项目正按 [`docs/迭代文档.md`](docs/迭代文档.md) 从零分级重建，Level 0-3 已完成（2026-07-24），后续 Level 4-7 待实现。

- 约定：**每次对话只做一个 Level**，用「请实现 Level N」触发；流程 = 列文件 → 完整代码 → 测试代码 → 验收命令，跑完验收再进下一个
- ⚠️ 迭代文档的代码块有 **markdown 渲染损坏**：正则反斜杠丢失（`\s` `\d` `\S` → `s` `d` `S`）、代码围栏标记被吞、`__name__` → `name`、字符类方括号丢失。实现时必须先还原原义，不能照抄
- 已应用的偏差（相对文档）：pyproject dev 依赖用 `[dependency-groups]`（非 optional-dependencies，否则 `uv sync` 装不上 pytest）、`[tool.uv] package = false`（应用非库）、pytest `pythonpath = ["."]`；`llm_service.py` 模块级 `AsyncOpenAI` 包了 try/except（openai SDK 2.x 拒绝空字符串 api_key，否则模块导入即崩，无 key 时应落兜底分支）
- 遗留代码：旧架构模块（`app/infrastructure/`、`app/api/v1/`、`app/middleware/`、`app/domain/grading|report|feedback/`、`app/tasks/`、`app/models/`）还在磁盘上但**不再被任何代码引用**，清理待用户确认；旧测试 `tests/unit/test_dimensions.py` 测旧模块，保持绿色

## 常用命令

```bash
# 依赖（uv 管理，dev 组默认安装）
uv sync

# 启动应用（开发模式，带热重载）
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 健康检查: curl http://localhost:8000/health
# API 文档:  http://localhost:8000/docs

# 测试
uv run pytest                                # 全量
uv run pytest tests/test_domain.py           # 单文件
uv run pytest -k "grade_3"                   # 按名过滤
```

> Level 6/7 才需要 PostgreSQL/Redis（docker-compose.yml 已备好），Level 0-3 不依赖任何外部服务。

## 架构概览（当前 = 新 MVP 管道 + 遗留模块）

新管道（迭代文档架构）：

```
app/
├── main.py               # FastAPI 入口 + /health，挂载 webhook 路由
├── config.py             # pydantic-settings（lowercase 字段，读 .env）
├── domain/               # 纯数据层，无 IO
│   ├── constants.py      #   六维元组、分数/年级范围、状态枚举
│   ├── grade_weights.py  #   年级段权重 + 加权总分
│   └── schemas.py        #   全部 Pydantic 模型
├── prompts/              # Prompt 模板（Python 模块，年级段 1_2/3_4/5_7 + repair）
│   └── __init__.py       #   按年级路由渲染 render_assessment_prompt()
├── services/
│   └── llm_service.py    # LLM 调用 → 三段式校验 → 修复重试 → 兜底
├── api/
│   └── webhook.py        # 飞书事件回调（challenge/token 校验、消息路由）
└── utils/
    └── text_parser.py    # 老师指令解析（评估/查询/帮助/周报/取消）
```

遗留（不再被引用，待清理）：`app/infrastructure/`（LLM/ASR/飞书/缓存/OSS 适配器）、`app/api/v1/`、`app/middleware/`、`app/domain/grading|report|feedback/`、`app/models/`、`app/tasks/`、根目录 `prompts/v1.0/`（旧版 md 模板）、`config/base.yaml`、`requirements.txt`。

### 核心数据流（当前实现）

```
飞书消息 → POST /webhook
  → challenge 验证 → token 校验 → 非消息事件忽略
    → text：判断 @机器人 → parse_teacher_message() → ParsedCommand
        （当前返回解析结果供调试；Level 4 接 call_llm_assessment + 发卡片）
    → image/audio：回复"开发中"占位

评估管道（llm_service.call_llm_assessment，Level 4 接入 webhook）
  ① render_assessment_prompt()  # 按年级段选模板（1-2/3-4/5-7）
  ② AsyncOpenAI.chat(temperature=0)
  ③ _validate_output()          # 剥离代码围栏 → json.loads → Pydantic 校验
  ④ 校验失败 → REPAIR_PROMPT 修复重试（≤llm_max_retries 次）
  ⑤ 非校验异常/全失败 → 全 3 分兜底 + needs_review=True（系统永不崩）
  ⑥ compute_weighted_score()    # 0 权重维度自动不计入总分
```

### 六维评估 + 年级权重（domain/grade_weights.py）

六个维度固定：观点清晰度 / 逻辑连贯性 / 证据支撑 / 多角度思考 / 回应与质疑 / 表达完整性。`GRADE_WEIGHTS` 分三档（1_2 重表达、逻辑与多角度为 0 不计分；3_4 重逻辑；5_7 重思辨、六维均衡）。`get_active_dimensions(grade)` 返回权重>0 的维度；`compute_weighted_score(scores, grade)` 算加权总分。改权重只动 `GRADE_WEIGHTS` 字典。

### LLM 可靠性三段式（services/llm_service.py）

1. **Pydantic 强校验**（`LLMAssessmentOutput`）：字段齐全 + 1-5 整数 + 字符串最小长度
2. **格式修复重试**：原始输出（前 500 字）+ 错误信息 + `REPAIR_PROMPT` 让 LLM 自修，最多 `settings.llm_max_retries` 次
3. **中性分兜底**：全失败 → 六维全 3 分 + `needs_review=True` 待人工复核

## 开发注意事项

- **配置**：`app/config.py` lowercase 字段读 `.env`（pydantic-settings，环境变量名大小写不敏感），字段参考 `.env.example`。旧 `config/base.yaml` 不再被加载。
- **无依赖注入框架**：新代码用模块级单例（`llm_service.client`、`settings`），测试直接 `unittest.mock.patch` 模块属性。不要引入 Depends 或另搞 DI。
- **Prompt 扩展**：新增年级段/题型在 `app/prompts/` 加模块 + 在 `get_assessment_prompts()` 加分支；`USER_PROMPT` 模板占位符为 `{topic}/{text}/{teacher_context_section}`，JSON 示例里的字面花括号必须双写。
- **测试默认 asyncio**：`pyproject.toml` 已配 `asyncio_mode = "auto"`，异步测试不需要 marker 声明。
- **DB/Redis 未接入**：Level 6（PostgreSQL 持久化）、Level 7（Redis 缓存/熔断）未实现，不要提前引入外部服务依赖。

## 待办（迭代文档 Level 4-7）

Level 4 飞书卡片 + 评估串联 → Level 5 卡片按钮回调 + 审核迭代 → Level 6 PostgreSQL 持久化 → Level 7 Redis 缓存 + 配额熔断
