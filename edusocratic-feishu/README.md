# EduSocratic - 维学思辨AI评估系统

> 2026 AI先锋未来人才大赛参赛作品 | EduSocratic团队

面向圆桌星球1-7年级线上小班思辨课程的AI评估系统。通过大语言模型从六个维度（观点清晰度、逻辑连贯性、证据支撑、多角度思考、回应与质疑、表达完整性）对学生思辨能力进行量化评估，解决思辨课堂"反馈效率低、个性化指导欠缺、学情无法量化"三大教学难题。

## 目录

- [核心特性](#核心特性)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [核心模块](#核心模块)
- [评估维度设计](#评估维度设计)
- [成本分析](#成本分析)
- [开发路线图](#开发路线图)
- [配置说明](#配置说明)

## 核心特性

### 六维思辨评估模型
融合Carnegie/ETS持久技能框架、Paul-Elder批判性思维模型和皮亚杰认知发展理论，将抽象的思辨能力拆解为**六个可量化维度**：

| 维度 | 1-2年级权重 | 3-4年级权重 | 5-7年级权重 |
|------|------------|------------|------------|
| 观点清晰度 | 40% | 30% | 15% |
| 表达完整性 | 30% | — | — |
| 逻辑连贯性 | — | 25% | 25% |
| 证据支撑 | 15% | 25% | 20% |
| 多角度思考 | — | 10% | 20% |
| 回应与质疑 | 15% | 10% | 20% |

权重随年级动态调整，尊重认知发展规律。

### LLM可靠性保障
- **JSON Schema严格校验**：确保输出格式正确、字段完整、分数在1-5范围内
- **格式修复重试**：LLM返回格式错误时自动发送修复Prompt，80%可自动修复
- **中性分兜底**：3次重试仍失败则返回3分+标记待人工复核，系统永不崩溃
- **SimHash相似缓存**：相似回答直接返回缓存结果，节省API调用成本

### 成本熔断机制
- 单学生每天限20次评估
- 单班每月$50硬预算上限
- 超限自动熔断，防止API滥用

### 教师反馈闭环
- 评估卡片"评分不准确"按钮收集教师修正数据
- 自动统计各维度偏差，检测Prompt漂移
- 累计偏差超阈值自动触发优化提醒

### 飞书原生集成
- **学生端**：机器人接收文字/语音回答，实时互动
- **老师端**：消息卡片推送评估结果，一键确认/修改/反馈
- **家长端**：云文档自动生成个性化学习报告
- **管理端**：多维表格仪表盘可视化班级数据

## 系统架构

```
┌────────────────────────────────────────────────────────────────────┐
│                       API Gateway / BFF 层                         │
│            (身份认证、请求限流、路由分发、请求ID链路追踪)            │
├────────────────────────────────────────────────────────────────────┤
│                      Service 层（业务编排）                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 评估服务  │ │ 报告服务  │ │ 用户服务  │ │ 通知服务  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├────────────────────────────────────────────────────────────────────┤
│                      Domain 层（核心领域逻辑）                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 评分引擎  │ │ Prompt   │ │ 权重     │ │ 报告     │            │
│  │          │ │ 管理器   │ │ 计算器   │ │ 生成器   │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├────────────────────────────────────────────────────────────────────┤
│                   Infrastructure 层（外部服务适配）                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ LLM      │ │ ASR      │ │ 飞书     │ │ 缓存     │            │
│  │ Provider │ │ Provider │ │ Adapter  │ │ Provider │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├────────────────────────────────────────────────────────────────────┤
│                       数据持久层                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ PostgreSQL│ │  Redis   │ │ 多维表格  │ │  OSS     │            │
│  │ (主数据) │ │ (缓存)   │ │ (展示)   │ │ (文件)   │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├────────────────────────────────────────────────────────────────────┤
│                    Cross-cutting（横切关注点）                      │
│    日志链路(ELK) │ 监控告警(Prometheus) │ 配置中心 │ 成本熔断    │
└────────────────────────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose（可选）

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/Lumjiel/EduSocratic.git
cd EduSocratic/edusocratic-feishu

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的API Keys

# 5. 启动数据库和Redis
docker-compose up -d db redis

# 6. 运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker一键启动

```bash
docker-compose up -d
```

### 验证

```bash
# 健康检查
curl http://localhost:8000/health

# API文档
open http://localhost:8000/docs
```

## 项目结构

```
edusocratic-feishu/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 入口 + 依赖注入
│   ├── config.py                  # 配置加载（pydantic-settings）
│   │
│   ├── api/                       # API Gateway 层
│   │   ├── deps.py                # 依赖注入
│   │   └── v1/
│   │       ├── router.py          # 路由聚合
│   │       ├── webhooks.py        # 飞书事件回调
│   │       ├── assessment.py      # 评估接口 + 用量查询
│   │       └── reports.py         # 报告接口
│   │
│   ├── services/                  # Service 层（业务编排）
│   │   ├── assessment_service.py  # 评估主流程编排
│   │   ├── report_service.py      # 报告生成编排
│   │   ├── feedback_service.py    # 教师反馈收集
│   │   └── notification_service.py # 通知编排
│   │
│   ├── domain/                    # Domain 层（核心逻辑）
│   │   ├── grading/
│   │   │   ├── engine.py          # 评分引擎（缓存→熔断→LLM→校验→缓存）
│   │   │   ├── dimensions.py      # 六维定义 + 年级权重 + 加权计算
│   │   │   ├── prompt_manager.py  # Prompt模板管理（版本化）
│   │   │   └── validator.py       # LLM输出校验 + 格式修复 + 兜底
│   │   ├── report/
│   │   │   ├── generator.py       # 报告生成器
│   │   │   └── templates.py       # 报告模板管理
│   │   └── feedback/
│   │       ├── collector.py       # 反馈收集 + Prompt漂移检测
│   │       └── analyzer.py         # 反馈分析
│   │
│   ├── infrastructure/            # Infrastructure 层（外部适配）
│   │   ├── llm/
│   │   │   ├── base.py            # LLM Provider接口 + OpenAI + 智谱
│   │   │   └── circuit_breaker.py # 成本熔断器
│   │   ├── asr/
│   │   │   └── base.py            # ASR接口 + 讯飞适配
│   │   ├── feishu/
│   │   │   ├── client.py          # 飞书API封装
│   │   │   ├── card_builder.py    # 卡片构建（老师端/家长端/学生端）
│   │   │   └── event_handler.py   # 消息事件处理
│   │   ├── cache/
│   │   │   └── similarity.py      # SimHash相似回答缓存
│   │   └── storage/
│   │       ├── postgres.py        # SQLAlchemy异步引擎
│   │       └── oss.py             # 文件存储
│   │
│   ├── models/                    # 数据模型（SQLAlchemy ORM）
│   │   └── __init__.py            # User/Classroom/Assessment/Feedback/Report
│   │
│   ├── tasks/                     # Celery 异步任务
│   │   ├── __init__.py            # Celery配置
│   │   ├── assessment.py          # 评估异步任务
│   │   └── report.py              # 报告异步任务
│   │
│   └── middleware/                # 中间件
│       ├── logging.py             # 请求日志 + 链路追踪 + 限频
│       └── error_handler.py       # 全局异常处理
│
├── prompts/                       # Prompt 模板（外部化、版本化）
│   ├── v1.0/
│   │   ├── assessment_1_2.md      # 1-2年级评估Prompt
│   │   ├── assessment_3_4.md      # 3-4年级评估Prompt
│   │   ├── assessment_5_7.md      # 5-7年级评估Prompt
│   │   └── format_repair.md       # 格式修复Prompt
│   └── v1.1/                      # 后续版本Prompt
│
├── config/                        # 配置文件
│   ├── base.yaml                  # 基础配置
│   ├── production.yaml            # 生产环境覆盖
│   └── secret.env.example         # 环境变量模板
│
├── tests/                         # 测试
│   ├── conftest.py               # pytest fixtures
│   ├── unit/                      # 单元测试
│   │   └── test_dimensions.py     # 维度计算测试
│   ├── integration/               # 集成测试
│   └── fixtures/                  # 测试数据
│
├── migrations/                    # 数据库迁移（Alembic）
├── docker-compose.yml             # 服务编排
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 技术栈

| 层级 | 技术 | 选型理由 |
|------|------|----------|
| 语言 | Python 3.11+ | AI生态成熟，async/await原生支持 |
| Web框架 | FastAPI | 异步、自动文档、类型安全 |
| 任务队列 | Celery + Redis | 评估任务异步化，解耦接收和处理 |
| 缓存 | Redis | 相似回答缓存 + 限频计数器 |
| 主数据库 | PostgreSQL + SQLAlchemy 2.0 | 结构化数据持久化（异步ORM） |
| LLM | GPT-4 Turbo / 智谱 GLM-4 | 评估主模型（可切换Provider） |
| ASR | 讯飞语音转写 | 高准确率中文少儿语音 |
| 飞书SDK | lark-oapi | 官方Python SDK |
| 监控 | Prometheus + Grafana | 延迟/成本/成功率监控 |
| 日志 | ELK Stack | 分布式日志链路追踪 |
| 配置 | YAML + 环境变量 | Prompt/权重/API Key外部化 |
| 部署 | Docker Compose | 标准化部署 |

## 核心模块

### 评分引擎（GradingEngine）

评估流程：**缓存检查 → 成本熔断 → LLM调用 → 输出校验 → 结果缓存**

```python
# 评估流程伪代码
async def assess(student_id, class_id, grade, topic, response):
    # 1. 成本熔断检查
    budget = await breaker.check_and_consume(student_id, class_id)
    if not budget["allowed"]: return budget_exceeded_result()

    # 2. 相似缓存检查
    cached = await cache.get_cached_result(grade, topic, response)
    if cached: return cached

    # 3. 调用LLM
    raw_output = await llm.chat(messages, temperature=0)

    # 4. 校验 + 修复
    result = await validator.validate_and_fix(raw_output)

    # 5. 缓存结果
    await cache.cache_result(grade, topic, response, result)
    return result
```

### LLM输出校验器（OutputValidator）

三层防护确保LLM输出可靠：
1. **JSON Schema校验**：Pydantic模型严格校验字段完整性、类型、范围
2. **格式修复重试**：发送修复Prompt让LLM自行修正格式（最多2次）
3. **中性分兜底**：全部失败返回3分+标记待人工复核

### 成本熔断器（CostCircuitBreaker）

基于Redis的滑动窗口限频：
- 每生每天最多20次评估
- 每班每月$50硬预算上限
- 超限自动熔断，返回友好提示

### 飞书卡片构建器（CardBuilder）

三种卡片模板：
- **老师端评估卡片**：六维评分 + 亮点/建议 + 确认/修改/反馈按钮
- **家长端报告卡片**：学习报告 + 成长曲线 + 家庭建议
- **学生端激励卡片**：正向反馈 + 鼓励话语

## 评估维度设计

### 学术基础

本方案融合三大理论框架：

1. **Carnegie/ETS 持久技能框架（2026）**：定义协作、沟通、批判性思维三大持久技能
2. **Paul-Elder 批判性思维模型**：认知维度 + 元认知维度 + 情感态度维度
3. **皮亚杰认知发展理论**：1-7年级跨越前运算→具体运算→形式运算阶段

### 评分准确性验证

| 指标 | 目标值 | 说明 |
|------|--------|------|
| Cohen's Kappa | ≥ 0.65 | AI与人工评分"实质性一致" |
| 维度级Pearson r | ≥ 0.7 | 各维度评分与人工相关系数 |
| 极端差异率 | < 5% | AI与人工评分相差≥2分的比例 |

验证方法：90条采样 → 3位老师独立评分 → AI评分 → 计算Kappa系数 → 迭代优化

## 成本分析

| 项目 | 单价 | 月用量（50班） | 月成本 |
|------|------|----------------|--------|
| GPT-4 Turbo | $0.02/次评估 | 50班×7人×8次=2800次 | ~$56 |
| ASR服务 | ¥0.006/秒 | 2800次×15秒=42000秒 | ~¥252 |
| 飞书商业版 | ¥10/人/月 | 50老师 | ¥500 |
| 云服务器(2核4G) | ¥100/月 | 1台 | ¥100 |
| Redis云服务 | ¥50/月 | 1实例 | ¥50 |
| **合计** | | | **~$130/月** |

> 熔断机制确保不会超支。单班$50/月硬上限，全部50班约$2500/月封顶。

## 开发路线图

### 第一阶段：MVP验证（1-2个月）

- [x] 评估维度设计与专家评审
- [x] Prompt工程 + 输出校验
- [x] 飞书基础集成（收消息→评估→卡片）
- [x] 缓存 + 限流 + 成本熔断
- [ ] 2个班级试点运行

### 第二阶段：规模化（3-4个月）

- [ ] 语音识别集成 + 说话人分离策略
- [ ] 家长端云文档报告 + 权限控制
- [ ] 教师反馈闭环 + Prompt漂移检测
- [ ] 监控面板 + 成本看板
- [ ] 全部班级推广 + 老师培训

### 第三阶段：持续优化（长期）

- [ ] 基于教师反馈数据的Prompt自动优化
- [ ] 多模态扩展（白板绘图分析）
- [ ] 课堂实时AI教练（流式ASR + 轻量模型）
- [ ] 说话人分离能力上线（需APP配合）

## 配置说明

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `OPENAI_API_KEY` | 是 | OpenAI API Key |
| `ZHIPU_API_KEY` | 否 | 智谱GLM-4 API Key（备选LLM） |
| `FEISHU_APP_ID` | 是 | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | 是 | 飞书应用 App Secret |
| `FEISHU_VERIFICATION_TOKEN` | 是 | 飞书事件验证Token |
| `XUNFEI_APP_ID` | 否 | 讯飞ASR App ID |
| `XUNFEI_API_KEY` | 否 | 讯飞ASR API Key |
| `DATABASE_URL` | 是 | PostgreSQL连接URL |
| `REDIS_URL` | 是 | Redis连接URL |

### 飞书应用配置

1. 在[飞书开放平台](https://open.feishu.cn)创建企业自建应用
2. 配置事件订阅：`im.message.receive_v1`
3. 配置机器人能力
4. 获取 App ID / App Secret / Verification Token
5. 填入 `.env` 文件

## License

MIT

---

*本项目为2026 AI先锋未来人才大赛参赛作品*
