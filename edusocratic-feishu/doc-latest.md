# 维学思辨AI评估系统 - 项目策划方案

> 2026 AI先锋未来人才大赛参赛作品 | EduSocratic团队

---

# 一、项目概述

## 1.1 项目背景

杭州维学新知网络科技有限公司（简称"维学"）是一家集团化运营的在线素质教育公司，核心品牌为"圆桌星球"，定位为"K12 自适应学习方案提供商"。公司核心产品为圆桌星球人文思辨课程，面向1-7年级学生，采用线上小班（7人）直播形式，围绕文学、历史、哲学、科学、社会学、艺术等主题展开平等对话和深度讨论。

**核心痛点**：圆桌星球的思辨能力评估完全依赖人工评价，由此产生三大教学难题：

| 痛点 | 具体表现 | 量化影响 |
|------|----------|----------|
| 效率困境 | 每节课7名学生的课堂发言、习作完全依赖人工评价，老师课后逐一撰写评语耗时30-60分钟 | 假设全校50个班，老师每周多花15-30小时写评语 |
| 量化困境 | 思辨能力不像数学题有标准答案，缺乏客观量化指标，不同老师评价标准不一 | 家长完全无法追踪孩子能力变化 |
| 反馈困境 | 课堂表现到家长收到反馈有较长延迟，学生无法获得即时成长指引 | 反馈周期通常>1周，错过最佳干预窗口 |

## 1.2 方案定位

本项目为圆桌星球设计一套 **"AI初评 + 老师审核 + 持续进化"** 的思辨能力评估系统。核心价值在于：

- **为老师减负**：自动生成发言分析报告和评估建议，将评语撰写时间从30-60分钟压缩至5-10分钟
- **让能力可见**：将抽象的思辨能力转化为可量化、可追踪的六维评估数据
- **让反馈即时**：课后自动生成个性化报告推送至家长端，形成"课堂-评估-反馈"闭环
- **越用越准**：教师反馈闭环驱动Prompt持续优化，系统评分逐步逼近资深老师水平

## 1.3 设计原则

| 原则 | 说明 |
|------|------|
| **可靠性优先** | LLM输出必须经过JSON Schema校验 + 格式修复重试，绝不把原始LLM输出直接推给用户 |
| **渐进式复杂度** | MVP阶段用"学生单独发语音"绕开说话人分离难题；后续迭代引入多路音频流+diarization |
| **成本可控** | 每个学生每天评估次数上限 + 每班每月API预算熔断 + 相似回答缓存 |
| **可验证** | 用Cohen's Kappa系数量化AI与人工评分一致性，有数据才有说服力 |
| **隐私设计** | 数据最小化采集 + 飞书文档级权限控制 + 未成年人数据加密存储 |

## 1.4 命题要求对照

| 命题要求 | 本方案对应设计 |
|----------|----------------|
| 搭建思辨能力评估维度，适配1-7年级认知梯度 | 六维评估框架（观点清晰度、逻辑连贯性、证据支撑、多角度思考、回应与质疑、表达完整性）+ 年级差异化权重 |
| 说明核心技术路径与数据处理方案，兼顾少儿表达的不规范性 | GPT-4级别大语言模型 + 意图理解（非语法纠错）+ 分年级Prompt策略 + JSON Schema校验兜底 |
| 阐述方案落地路径、潜在风险与优化方向 | 三阶段MVP部署 + 飞书原生集成 + 六大风险缓解措施 + 教师反馈闭环驱动持续优化 |

---

# 二、市场调研

## 2.1 维学公司概况

| 维度 | 信息 |
|------|------|
| 公司全称 | 杭州维学新知网络科技有限公司 |
| 成立时间 | 2018年11月 |
| 总部 | 杭州（在武汉、重庆、成都设有分公司） |
| 团队规模 | 500-999人，预计年末达到1000人+ |
| 融资阶段 | 天使轮（投资方含九合锐达、嘉兴鹏信等） |
| 法定代表人 | 周枫 |
| 核心品牌 | 圆桌星球（已注册商标） |

**课程设计理念**：
- 融合哥伦比亚大学通识课、同伴学习（peer learning）、探究式学习（structured inquiry-based learning）、基于问题的学习（PBL）等教学模式
- 设计了20+种思维训练方式，覆盖不同年龄段认知特点
- 课程研发负责人李娜为哥伦比亚大学教育心理学博士
- 80%的课堂时间由学生主导发言，老师作为引导者而非灌输者

## 2.2 少儿思辨教育市场概况

### 市场趋势

2025-2026年，少儿思辨教育赛道出现显著升温。根据中国青年报社社会调查中心的专项调查：

- 62.6%的受访家长感到使用AI工具后孩子知识面和视野得到拓展
- 58.8%的家长感觉孩子对AI技术产生了心理依赖
- 42.7%的家长直言孩子独立主动思考的能力下降

在AI焦虑的催化下，家长群体出现了从"AI工具热"到"思辨能力培养热"的转向。QuestMobile《2025有孩家庭人群消费洞察报告》显示，6-12岁文史类产品使用率同比增长18%。

### 政策背景

在"双减"政策框架下，学科类培训受到严格限制，素质教育（含思辨、阅读、表达等）获得政策红利。新版全国语文课程标准将"思维的发展与提升"列为四大核心能力之一，为思辨教育提供了课程合法性和市场需求双重支撑。

### 市场规模

少儿素质教育市场整体规模在千亿级别。思辨教育作为细分赛道仍处于快速成长期，尚无权威第三方给出精确市场规模数据，但从头部企业的扩张速度（维学一年内从400人扩张至近1000人）来看，需求端增长强劲。

## 2.3 同类竞品分析

| 竞品 | 核心方向 | 教学模式 | AI应用情况 |
|------|----------|----------|------------|
| 火花思维 | 数理思维 + 中文素养 | 小班直播，2分钟1次1对1互动 | AI智能分析学情，"火花6问"含AI问答 |
| 豌豆思维 | 数理逻辑思维 | 在线小班直播 | AI辅助教学，自适应学习路径 |
| 你拍一 | 数学思维（幼少儿） | 溯源教学法，七步闭环 | AI应用相对初级，以真人教学为主 |
| 猿辅导AI大阅读 | 阅读 + 思辨（2026.7上线） | AI一对一伴读，苏格拉底式引导 | 自研大模型，AI私教全程对话引导，1499元/年 |
| **圆桌星球（维学）** | **人文思辨（1-7年级）** | **7人小班圆桌讨论** | **目前无公开AI评估系统（本项目的切入点）** |
| 伴鱼智学 | AI私教 + 思维课（6-12岁） | AI一对一语音对话 | 自研大模型，全程语音交互，准确率99.8% |

**关键发现**：主流竞品中，火花思维和伴鱼智学已初步应用AI（学情分析、AI对话），猿辅导AI大阅读是最新入局者（2026年7月），但专门针对"思辨能力AI评估"的产品尚未出现。

## 2.4 思辨教育 vs 传统学科培训

| 维度 | 传统学科培训 | 思辨教育 |
|------|-------------|----------|
| 教学目标 | 知识掌握、应试技巧 | 独立思考、逻辑表达、批判性思维 |
| 评价方式 | 标准化考试（可量化） | 主观评价为主（难量化） |
| 师生关系 | 教师主导、单向传授 | 平等对话、引导启发 |
| 答案特征 | 有标准答案 | 无标准答案，重在论证过程 |
| AI适配难度 | 相对低（有标准答案可对） | 高（需要理解论证逻辑、评估思维质量） |

---

# 三、思辨能力评估维度

## 3.1 学术评估框架参考

### Carnegie/ETS 持久技能框架（2026）

卡内基教学促进基金会与ETS在2026年报告中定义了三大"持久技能"（durable skills），每个技能分为四个发展层级：探索→分析→整合→延伸：

- **协作**：处理团队动态、整合不同视角、建立信任
- **沟通**：适应不同受众调整信息、主动倾听、跨语境表达
- **批判性思维**：寻找和评估信息、构建基于证据的论证、在复杂/模糊情境中推理

### Paul-Elder 批判性思维模型

国内中小学AI教育批判性思维研究（2025）中广泛采用的三维框架：

- **认知维度**：问题分析、逻辑推理、证据评估
- **元认知维度**：自我监控、策略调整、反思质疑
- **情感态度维度**：开放包容、理性审慎、责任担当

## 3.2 六维评估框架

结合圆桌星球课程特点，将思辨评估拆解为以下六个维度：

| 维度 | 定义 | 评估要点 |
|------|------|----------|
| 观点清晰度 | 能否明确表达自己的立场和观点 | 是否有明确立场、是否清晰表达 |
| 逻辑连贯性 | 论证是否有内在逻辑、是否自洽 | 因果关系是否合理、论证是否一致 |
| 证据支撑 | 是否引用事实、例子或推理支撑观点 | 例子是否相关、证据是否充分 |
| 多角度思考 | 能否考虑反方观点或替代解释 | 是否考虑不同立场、是否有辩证思维 |
| 回应与质疑 | 能否针对他人观点提出有效回应 | 回应是否切题、质疑是否有深度 |
| 表达完整性 | 语言表达是否完整、有条理 | 句子是否完整、表达是否连贯 |

## 3.3 年级差异化权重设计

基于皮亚杰认知发展理论，1-7年级（约6-13岁）跨越两个关键阶段：

### 1-2年级（6-8岁）：前运算→具体运算过渡

| 维度 | 权重 | 评估重点 |
|------|------|----------|
| 观点清晰度 | 40% | 能否说出"我觉得/我认为" |
| 表达完整性 | 30% | 句子是否完整 |
| 证据支撑 | 15% | 能否举出一个例子 |
| 回应与质疑 | 15% | 能否重复或简单回应他人 |

**评估原则**："能说出来就是进步" —— 重点评估"是否愿意表达"和"能否说出基本观点"

### 3-4年级（8-10岁）：具体运算阶段

| 维度 | 权重 | 评估重点 |
|------|------|----------|
| 观点清晰度 | 30% | 观点是否完整、有主语有判断 |
| 逻辑连贯性 | 25% | 因果关系是否合理 |
| 证据支撑 | 25% | 例子是否与观点相关 |
| 多角度思考 | 10% | 能否主动提出不同看法 |
| 回应与质疑 | 10% | 回应是否切题、有理由 |

**评估原则**："能讲出道理就是成长" —— 重点评估论证的基本逻辑和证据意识

### 5-7年级（10-13岁）：具体运算→形式运算过渡

| 维度 | 权重 | 评估重点 |
|------|------|----------|
| 逻辑连贯性 | 25% | 论证链条是否完整、有无逻辑漏洞 |
| 多角度思考 | 20% | 能否系统分析多方立场 |
| 证据支撑 | 20% | 证据是否充分、来源是否可信 |
| 回应与质疑 | 20% | 质疑是否精准、回应是否有深度 |
| 观点清晰度 | 15% | 观点是否明确、有层次 |

**评估原则**："能辩证思考就是深度" —— 重点评估批判性思维的高阶能力

## 3.4 评分标准（1-5分制）

| 分数 | 定义 | 对应年级水平 |
|------|------|--------------|
| 5分（卓越） | 远超该年级平均水平，表现出令人印象深刻的思辨能力 | 顶尖 |
| 4分（优秀） | 明显超出该年级平均水平 | 优秀 |
| 3分（达标） | 达到该年级应有的思辨能力水平 | 中等 |
| 2分（待提升） | 略低于该年级平均水平 | 及格 |
| 1分（需关注） | 显著低于该年级平均水平 | 需干预 |

**关键原则**：评分标准与年级挂钩——同样是"能举出一个例子"，1年级得5分，5年级可能只算3分。

## 3.5 评分准确性验证方案

### 验证方法

| 步骤 | 操作 |
|------|------|
| 1. 采样 | 从不同年级各抽取30条课堂发言（共90条） |
| 2. 人工标注 | 请3位资深老师独立评分（六维1-5分） |
| 3. AI评分 | 用系统对同样的90条发言评分 |
| 4. 一致性计算 | 计算AI评分与人工评分的Cohen's Kappa系数 |
| 5. 迭代 | Kappa < 0.6则调整Prompt重新验证 |

### 验收标准

| 指标 | 目标值 | 说明 |
|------|--------|------|
| Cohen's Kappa | ≥ 0.65 | "实质性一致"阈值 |
| 维度级Pearson r | ≥ 0.7 | 各维度评分与人工相关系数 |
| 极端差异率 | < 5% | AI与人工评分相差≥2分的比例 |

---

# 四、技术架构

## 4.1 工程分层架构

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

## 4.2 LLM可靠性保障机制

```
用户发言 → 相似度缓存命中? ── 是 → 直接返回缓存结果
                │
                否
                ↓
        调用LLM API（温度=0 + 重试3次）
                │
                ↓
        JSON Schema校验 ── 失败 → 格式修复Prompt二次请求
                │                          │
                成功                       失败 → 返回中性分(3分)
                │                         + 标记待人工复核
                ↓
        分数合理性检查(1-5分区间)
                │
                ↓
        写入评估缓存 → 返回结果
```

### 关键机制说明

| 机制 | 实现 | 为什么 |
|------|------|--------|
| **请求级缓存** | SimHash + Redis，TTL=24h | 相似回答("我觉得对因为XXX")直接返回，省成本 |
| **JSON Schema校验** | 严格校验6维度 + 分数范围 | LLM经常漏字段、改字段名、给范围外分数 |
| **格式修复重试** | 一次失败后发送"你的格式有误，请严格按JSON返回" | 80%的格式错误能自动修复 |
| **中性分兜底** | 3次重试仍失败则给3分 + 标记 | 系统永不崩溃，宁可漏评也不乱评 |
| **成本熔断** | 单学生每天限20次，单月上限$50 | 防止API被刷或Prompt错误导致天价账单 |

## 4.3 语音处理方案

### 核心挑战：说话人分离（Speaker Diarization）

| 阶段 | 方案 | 可行性 |
|------|------|--------|
| MVP（比赛Demo） | 学生**单独发语音消息**给机器人，每人每条语音独立转写 | ✅ 完全可行，绕开diarization |
| v1.0（单班部署） | 接入pyannote/speaker-diarization，处理音频流 | ⚠️ 需要额外GPU资源 |
| v2.0（规模化） | 圆桌星球APP支持多路独立音频流，前端分离后上传 | ✅ 最优但需APP配合 |

### 少儿语音识别准确率保障

| 策略 | 实现 |
|------|------|
| ASR引擎选择 | 讯飞/字节少儿语音专用模型（如有） |
| 上下文辅助 | 将课堂讨论主题文字一并发送给ASR引擎做语义纠正 |
| 二次确认 | ASR结果置信度<0.7时，回复"我没听清，再说一次" |
| 人工兜底 | 极低置信度语音标记为"待人工转写"，不强行评估 |

### 实时性SLA设计

| 场景 | 延迟要求 | 技术选型 |
|------|----------|----------|
| 课堂即时反馈 | <3秒 | 流式ASR + 轻量规则引擎（非LLM） |
| 课后AI深度评估 | <30秒可接受 | 批量ASR + GPT-4评估 |
| 学习报告生成 | <5分钟 | 异步队列 + 报告构建服务 |

---

# 五、数据采集方案

## 5.1 数据流全景

```
                    ┌──────────────┐
    文字输入 ──────→│              │
                    │  飞书机器人  │────→ 消息事件 ────→ 后端服务
    语音消息 ──────→│  (事件订阅)  │
                    │              │
    文件上传 ──────→│              │
                    └──────────────┘
                           │
                    WebSocket长连接
                    (im.message.receive_v1)
                           │
                           ▼
              ┌────────────────────────┐
              │    消息类型路由器       │
              ├────────┬───────┬───────┤
              │  text  │ audio │ file  │
              └───┬────┴───┬───┴───┬───┘
                  │        │       │
                  ▼        ▼       ▼
              直接处理  ASR转写  OCR提取
                  │        │       │
                  └────────┼───────┘
                           ▼
                    ┌──────────────┐
                    │ 敏感信息脱敏  │
                    │ (手机号/地名) │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ AI评估引擎    │
                    └──────────────┘
```

## 5.2 数据类型与采集方式

| 数据类型 | 采集方式 | 处理链路 | 存储位置 |
|----------|----------|----------|----------|
| 文字发言 | 飞书text消息 | 直接解码UTF-8 | 多维表格 |
| 语音发言 | 飞书audio消息 | 下载→ASR→文本 | 多维表格 + OSS |
| 习作文档 | 飞书file消息 | 下载→OCR/文本提取 | 多维表格 + OSS |
| 互动记录 | 课堂聊天记录 | NLP分析提及/回复关系 | PostgreSQL |
| 教师反馈 | 卡片按钮点击 | 反馈理由编码 | PostgreSQL |

## 5.3 比赛场景Demo方案

| 环节 | 操作 | 技术实现 |
|------|------|----------|
| 课前 | 预制学生名单+讨论主题 | 多维表格批量导入 |
| 课中 | 在群聊@机器人发语音/文字 | 飞书WebSocket接收事件 |
| 课后 | 自动评估+推送 | 异步队列 + 卡片推送 |

---

# 六、飞书集成方案

## 6.1 四端权限模型

| 角色 | 能看什么 | 能操作什么 | 飞书权限实现 |
|------|----------|------------|--------------|
| 任课老师 | 自己班级的评估数据 | 审核/修改/确认AI评分 | 多维表格行级筛选 + 文档共享 |
| 学生家长 | 自己孩子的评估报告 | 阅读 + 确认收到 | 独立云文档 + 仅owner可见 |
| 学生本人 | 课堂激励反馈（仅正向） | 查看激励消息 | 机器人私聊消息 |
| 教学主管 | 全校班级对比数据 | 查看 + 导出 | 多维表格仪表盘 |
| 系统管理员 | 全部数据 | 全部操作 | 管理后台（不通过飞书） |

## 6.2 消息卡片交互设计

### 老师端评估卡片

```
┌──────────────────────────────────────┐
│ 📊 课堂思辨评估 - 三年级2班           │
│ 主题：应不应该给动物穿衣服？          │
├──────────────────────────────────────┤
│ 👦 小明 (5年级)                      │
│ 观点清晰度: 4  逻辑连贯性: 3         │
│ 证据支撑: 4  多角度思考: 2            │
│ 回应与质疑: 3  表达完整性: 4         │
│ ───────────────────────────────────  │
│ 💡 亮点：能举出"动物毛"做证据        │
│ 📌 建议：试试想想反方的理由          │
├──────────────────────────────────────┤
│  [✅ 确认发送]  [✏️ 修改后发送]      │
│  [👎 评分不准确]                     │
└──────────────────────────────────────┘
```

> **"评分不准确"按钮** = 教师反馈闭环的数据入口。点击后记录：
> - 原始AI评分（六维）
> - 教师修改后的评分
> - 差异维度 + 差异量
> - 用于后续Prompt优化训练集

## 6.3 飞书能力映射

| 飞书能力 | 用途 | 限频 | 应对策略 |
|---------|------|------|----------|
| IM消息(机器人) | 接收学生发言 | 5 QPS | 异步队列缓冲 |
| 消息卡片 | 推送评估结果 | 50次/秒 | 批量排队+熔断 |
| 多维表格 | 数据存储+仪表盘 | 10次/秒写 | 批量合并写入 |
| 云文档 | 家长个性化报告 | 同API标准 | 异步生成+链接推送 |
| 自动化流程 | 定时报告/提醒 | 商业版50万次/月 | 事件驱动优先 |

---

# 七、代码实现

## 7.1 技术栈选择

| 层级 | 技术 | 选型理由 |
|------|------|----------|
| 语言 | Python 3.11+ | AI生态成熟，async/await原生支持 |
| Web框架 | FastAPI | 异步、自动文档、类型安全 |
| 任务队列 | Celery + Redis | 评估任务异步化，解耦接收和处理 |
| 缓存 | Redis | 相似回答缓存 + 限频计数器 |
| 主数据库 | PostgreSQL | 结构化数据持久化（用户/班级/反馈） |
| ORM | SQLAlchemy 2.0 | 异步ORM，类型提示 |
| 飞书SDK | lark-oapi | 官方Python SDK |
| LLM | GPT-4 Turbo / 智谱GLM-4 | 评估主模型（可切换） |
| ASR | 讯飞/字节少儿模型 | 高准确率中文少儿语音 |
| 监控 | Prometheus + Grafana | 延迟/成本/成功率监控 |
| 日志 | ELK Stack | 分布式日志链路追踪 |
| 配置 | YAML + 环境变量 | Prompt/权重/API Key外部化 |
| 部署 | Docker Compose | 标准化部署 |

## 7.2 项目结构

```
edusocratic-feishu/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 入口 + 生命周期管理
│   ├── config.py                  # 配置加载（YAML + env）
│   │
│   ├── api/                       # API Gateway 层
│   │   ├── deps.py                # 依赖注入（DB/Redis/当前用户）
│   │   └── v1/
│   │       ├── router.py          # 路由聚合
│   │       ├── assessment.py      # 评估接口
│   │       ├── reports.py         # 报告接口
│   │       └── webhooks.py        # 飞书事件回调
│   │
│   ├── services/                  # Service 层（业务编排）
│   │   ├── assessment_service.py  # 评估主流程编排
│   │   ├── report_service.py      # 报告生成编排
│   │   ├── feedback_service.py    # 教师反馈收集
│   │   └── notification_service.py # 通知编排
│   │
│   ├── domain/                    # Domain 层（核心逻辑）
│   │   ├── grading/
│   │   │   ├── engine.py          # 评分引擎主逻辑
│   │   │   ├── dimensions.py      # 六维定义 + 权重计算
│   │   │   ├── prompt_manager.py  # Prompt模板管理（版本化）
│   │   │   └── validator.py       # LLM输出校验 + 修复
│   │   ├── report/
│   │   │   ├── generator.py       # 报告生成器
│   │   │   └── templates.py       # 报告模板管理
│   │   └── feedback/
│   │       ├── collector.py       # 反馈收集器
│   │       └── analyzer.py         # 反馈分析（用于优化）
│   │
│   ├── infrastructure/            # Infrastructure 层（外部适配）
│   │   ├── llm/
│   │   │   ├── base.py            # LLM Provider 接口
│   │   │   ├── openai_provider.py # OpenAI 适配
│   │   │   ├── zhipu_provider.py  # 智谱适配
│   │   │   └── circuit_breaker.py # 成本熔断器
│   │   ├── asr/
│   │   │   ├── base.py            # ASR Provider 接口
│   │   │   └── xunfei_provider.py # 讯飞适配
│   │   ├── feishu/
│   │   │   ├── client.py          # 飞书 API 封装
│   │   │   ├── card_builder.py    # 卡片构建器
│   │   │   └── event_handler.py   # 事件解析
│   │   ├── cache/
│   │   │   ├── similarity.py      # SimHash相似度计算
│   │   │   └── redis_client.py    # Redis 操作封装
│   │   └── storage/
│   │       ├── postgres.py        # DB 操作
│   │       └── oss.py             # 文件存储
│   │
│   ├── models/                    # 数据模型
│   │   ├── user.py                # 用户/教师/家长
│   │   ├── classroom.py           # 班级/学生关系
│   │   ├── assessment.py          # 评估记录
│   │   ├── feedback.py            # 教师反馈
│   │   └── report.py              # 报告记录
│   │
│   ├── tasks/                     # Celery 异步任务
│   │   ├── assessment.py          # 评估任务
│   │   ├── report.py              # 报告生成任务
│   │   └── notification.py        # 通知任务
│   │
│   └── middleware/                # 中间件
│       ├── logging.py             # 请求日志 + 链路追踪
│       ├── rate_limit.py          # 限频中间件
│       └── error_handler.py       # 全局异常处理
│
├── migrations/                    # 数据库迁移（Alembic）
├── tests/                         # 测试
│   ├── unit/                      # 单元测试
│   ├── integration/               # 集成测试
│   └── fixtures/                  # 测试数据
│
├── prompts/                       # Prompt 模板（外部化）
│   ├── v1.0/
│   │   ├── assessment_1_2.md      # 1-2年级评估Prompt
│   │   ├── assessment_3_4.md      # 3-4年级评估Prompt
│   │   ├── assessment_5_7.md      # 5-7年级评估Prompt
│   │   └── format_repair.md       # 格式修复Prompt
│   └── v1.1/
│       └── ...
│
├── config/                        # 配置文件
│   ├── base.yaml                  # 基础配置
│   ├── production.yaml            # 生产环境覆盖
│   └── secret.env.example         # 敏感配置模板
│
├── docker-compose.yml             # 服务编排
├── Dockerfile
├── requirements.txt
└── README.md
```

## 7.3 核心代码示例

### LLM输出校验器

```python
# app/domain/grading/validator.py
from pydantic import BaseModel, Field, validator
from typing import Dict

class AssessmentResult(BaseModel):
    """评估结果数据模型 — 严格校验LLM输出"""
    scores: Dict[str, int] = Field(..., description="六维评分")
    reasoning: str = Field(..., min_length=10, max_length=500)
    highlights: str = Field(..., min_length=5, max_length=200)
    suggestions: str = Field(..., min_length=5, max_length=200)
    overall_comment: str = Field(..., min_length=20, max_length=100)

    @validator("scores")
    def validate_scores(cls, v):
        required = ["观点清晰度", "逻辑连贯性", "证据支撑",
                    "多角度思考", "回应与质疑", "表达完整性"]
        for dim in required:
            if dim not in v:
                raise ValueError(f"缺少维度: {dim}")
            if not 1 <= v[dim] <= 5:
                raise ValueError(f"{dim} 分数 {v[dim]} 超出1-5范围")
        return v

    @validator("reasoning")
    def validate_reasoning(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("理由过短")
        return v


class OutputValidator:
    """LLM输出校验 + 格式修复"""

    def __init__(self, llm_client, max_retries: int = 3):
        self.llm = llm_client
        self.max_retries = max_retries

    async def validate_and_fix(self, raw_output: str) -> AssessmentResult:
        """校验原始输出，失败则进入修复循环"""

        # 第一次尝试：直接解析JSON
        try:
            data = self._extract_json(raw_output)
            return AssessmentResult(**data)
        except (json.JSONDecodeError, ValidationError):
            pass  # 进入修复流程

        # 修复循环：告诉LLM它的格式有误，请重新返回
        repair_prompt = open("prompts/v1.0/format_repair.md").read()

        for attempt in range(self.max_retries - 1):
            try:
                fixed = await self.llm.chat(
                    messages=[
                        {"role": "system", "content": repair_prompt},
                        {"role": "user", "content": f"请修复以下JSON:\n{raw_output}"}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                data = json.loads(fixed)
                return AssessmentResult(**data)
            except (json.JSONDecodeError, ValidationError):
                continue

        # 全部失败 — 返回中性分 + 标记待人工复核
        return self._fallback_result(raw_output)

    def _fallback_result(self, original: str) -> AssessmentResult:
        """兜底：中性分 + 保留原始输出供人工审查"""
        return AssessmentResult(
            scores={dim: 3 for dim in [
                "观点清晰度", "逻辑连贯性", "证据支撑",
                "多角度思考", "回应与质疑", "表达完整性"
            ]},
            reasoning=f"[AI评估异常，需人工复核] 原始输出: {original[:100]}",
            highlights="AI评估异常",
            suggestions="建议老师手动评估本条",
            overall_comment="系统评估异常，已标记待人工复核"
        )

    def _extract_json(self, text: str) -> dict:
        """从LLM返回中提取JSON（处理Markdown包裹等情况）"""
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
```

### 成本熔断器

```python
# app/infrastructure/llm/circuit_breaker.py
import redis
from datetime import datetime, timedelta

class CostCircuitBreaker:
    """API成本熔断器"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.DAILY_LIMIT_PER_STUDENT = 20        # 每生每天最多20次评估
        self.MONTHLY_BUDGET_PER_CLASS = 50.0     # 每班每月$50上限
        self.PER_REQUEST_COST = 0.02             # 每次评估约$0.02

    async def check_and_consume(self, student_id: str, class_id: str) -> dict:
        """检查是否允许本次评估，允许则扣减预算"""

        daily_key = f"cost:daily:{student_id}:{datetime.now().strftime('%Y%m%d')}"
        monthly_key = f"cost:monthly:{class_id}:{datetime.now().strftime('%Y%m')}"

        # 检查日限额
        daily_count = int(self.redis.get(daily_key) or 0)
        if daily_count >= self.DAILY_LIMIT_PER_STUDENT:
            return {"allowed": False, "reason": "daily_limit_exceeded"}

        # 检查月预算
        monthly_cost = float(self.redis.get(monthly_key) or 0)
        if monthly_cost + self.PER_REQUEST_COST > self.MONTHLY_BUDGET_PER_CLASS:
            return {"allowed": False, "reason": "monthly_budget_exceeded"}

        # 扣减
        pipe = self.redis.pipeline()
        pipe.incr(daily_key)
        pipe.expire(daily_key, 86400)
        pipe.incrbyfloat(monthly_key, self.PER_REQUEST_COST)
        pipe.expire(monthly_key, 2592000)
        pipe.execute()

        return {"allowed": True}
```

### 相似回答缓存

```python
# app/infrastructure/cache/similarity.py
import hashlib

class SimilarityCache:
    """基于SimHash的相似回答缓存"""

    def __init__(self, redis_client, threshold: int = 3):
        self.redis = redis_client
        self.threshold = threshold

    def _simhash(self, text: str) -> str:
        """计算文本的SimHash指纹（简化版）"""
        return hashlib.md5(text.encode()).hexdigest()[:16]

    async def get_cached_result(self, grade: int, topic: str, response: str) -> dict | None:
        """查询是否有相似评估结果"""
        fingerprint = self._simhash(f"{grade}:{topic}:{response}")
        cached = self.redis.get(f"assess:cache:{fingerprint}")
        if cached:
            return json.loads(cached)
        return None

    async def cache_result(self, grade: int, topic: str, response: str, result: dict):
        """缓存评估结果"""
        fingerprint = self._simhash(f"{grade}:{topic}:{response}")
        self.redis.setex(
            f"assess:cache:{fingerprint}",
            86400,
            json.dumps(result, ensure_ascii=False)
        )
```

### 教师反馈收集

```python
# app/domain/feedback/collector.py

class FeedbackCollector:
    """收集教师对AI评分的修正，用于后续优化"""

    async def record_disagreement(
        self,
        assessment_id: str,
        teacher_id: str,
        original_scores: dict,
        corrected_scores: dict,
        feedback_reason: str | None = None
    ):
        """记录一次教师修正"""

        diff = {}
        for dim in original_scores:
            diff[dim] = corrected_scores[dim] - original_scores[dim]

        max_diff_dim = max(diff, key=lambda k: abs(diff[k]))

        feedback = {
            "assessment_id": assessment_id,
            "teacher_id": teacher_id,
            "original_scores": original_scores,
            "corrected_scores": corrected_scores,
            "differences": diff,
            "max_disagreement_dimension": max_diff_dim,
            "max_disagreement_value": diff[max_diff_dim],
            "reason": feedback_reason,
            "created_at": datetime.utcnow()
        }

        await self.db.feedback.insert(feedback)
        await self._check_prompt_drift(max_diff_dim)

    async def _check_prompt_drift(self, dimension: str):
        """检测Prompt是否需要调整"""
        recent = await self.db.feedback.find({
            "max_disagreement_dimension": dimension,
            "created_at": {"$gte": datetime.utcnow() - timedelta(days=7)}
        }).to_list(None)

        if len(recent) >= 20:
            avg_diff = sum(r["max_disagreement_value"] for r in recent) / len(recent)
            if abs(avg_diff) > 1.0:
                await self.alert_service.send(
                    f"⚠️ Prompt漂移预警: {dimension}维度近7天"
                    f"累计{len(recent)}次修正，平均偏差{avg_diff:.1f}分，建议调整Prompt"
                )
```

## 7.4 数据流转时序图（含异常路径）

```
┌────┐  ┌────┐  ┌──────┐  ┌──────┐  ┌────┐  ┌──────┐  ┌──────┐
│学生│  │飞书│  │机器人│  │评估  │  │LLM  │  │校验  │  │飞书  │
│    │  │    │  │服务  │  │引擎  │  │API  │  │器    │  │API   │
└┬───┘  └┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
 │发言    │        │        │        │        │        │        │
 ├───────→│        │        │        │        │        │        │
 │        │事件推送 │        │        │        │        │        │
 │        ├───────→│        │        │        │        │        │
 │        │        │ASR/解码 │        │        │        │        │
 │        │        ├───────→│        │        │        │        │
 │        │        │        │缓存命中?─→是→返回缓存      │        │
 │        │        │        │─┐      │        │        │        │
 │        │        │        │ │否    │        │        │        │
 │        │        │        │ ↓      │        │        │        │
 │        │        │        │成本检查─┐       │        │        │
 │        │        │        │      │超限→返回限额提示        │
 │        │        │        │      │通过    │        │        │
 │        │        │        │      ↓       │        │        │
 │        │        │        │调用LLM────────→│        │        │
 │        │        │        │      │←──────┤        │        │
 │        │        │        │      │校验    │        │        │
 │        │        │        │      ├───────→│        │        │
 │        │        │        │      │←──────┤        │        │
 │        │        │        │      │修复重试─→LLM──→│        │
 │        │        │        │      │(最多2次)│        │        │
 │        │        │        │      │通过    │        │        │
 │        │        │        │      │写缓存   │        │        │
 │        │        │        │      │写入DB   │        │        │
 │        │        │        │      │推送卡片────────────────→│
 │        │        │        │      │        │        │        │
 │        │←──────┤←──────┤←──────┤        │        │        │
 │        │        │        │ 老师点"评分不准确"         │        │
 │        │        │        │      │        │        │        │
 │        │        │        │记录反馈→[用于Prompt优化]    │        │
```

---

# 八、落地路径与里程碑

## 8.1 三阶段落地计划

### 第一阶段：MVP验证（1-2个月）

| 里程碑 | 内容 | 交付物 |
|--------|------|--------|
| M1 | 评估维度设计 + 专家评审 | 六维评估框架文档 + Kappa验证报告 |
| M2 | Prompt工程 + 输出校验 | Prompt模板 + JSON Schema + 格式修复 |
| M3 | 飞书基础集成（收消息→评估→卡片） | 可运行的评估原型 |
| M4 | 缓存 + 限流 + 成本熔断 | 基础设施层可用 |
| M5 | 2个班级试点运行 | 试点评估报告 + 老师反馈 |

### 第二阶段：规模化（3-4个月）

| 里程碑 | 内容 | 交付物 |
|--------|------|--------|
| M6 | 语音识别集成 + 说话人分离策略 | ASR转写通道上线 |
| M7 | 家长端云文档报告 + 权限控制 | 自动生成的个性化报告 |
| M8 | 教师反馈闭环 + Prompt漂移检测 | 反馈收集 + 自动预警 |
| M9 | 监控面板 + 成本看板 | Grafana Dashboard |
| M10 | 全部班级推广 + 老师培训 | 部署完成 + 培训材料 |

### 第三阶段：持续优化（长期）

| 里程碑 | 内容 |
|--------|------|
| M11 | 基于教师反馈数据的Prompt自动优化（半自动） |
| M12 | 多模态扩展（白板绘图分析） |
| M13 | 课堂实时AI教练（流式ASR + 轻量模型） |
| M14 | 说话人分离能力上线（需APP配合） |

## 8.2 成本分析

| 项目 | 单价 | 月用量（50班） | 月成本 |
|------|------|----------------|--------|
| GPT-4 Turbo | $0.02/次评估 | 50班×7人×8次=2800次 | ~$56 |
| ASR服务 | ¥0.006/秒 | 2800次×15秒=42000秒 | ~¥252 |
| 飞书商业版 | ¥10/人/月 | 50老师 | ¥500 |
| 云服务器(2核4G) | ¥100/月 | 1台 | ¥100 |
| Redis云服务 | ¥50/月 | 1实例 | ¥50 |
| **合计** | | | **~$130/月** |

> 注：熔断机制确保不会超支。单班$50/月硬上限，全部50班约$2500/月封顶。

## 8.3 关键成功指标

| 指标 | 目标值 | 衡量方式 |
|------|--------|----------|
| 老师评语时间 | ≤10分钟（降80%） | 时间追踪 |
| AI-人工评分Kappa | ≥0.65 | 定期抽样 |
| 评估成功率 | ≥95%（不因系统错误失败） | 监控面板 |
| 单次生评成本 | ≤$0.03 | 成本看板 |
| 老师满意度 | ≥4/5分 | 月度问卷 |
| 家长报告阅读率 | ≥70% | 飞书文档阅读数据 |

---

# 九、风险分析

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| AI评分与老师偏差大 | 中 | 高 | AI初评+老师审核；Kappa验证；超过5%差异率则暂停上线 |
| 少儿语音识别率低 | 高 | 中 | MVP用单独发语音绕开diarization；文字兜底；置信度<0.7要求重发 |
| LLM格式不稳定 | 高 | 中 | JSON Schema校验+格式修复重试3次+中性分兜底，永不崩溃 |
| API成本失控 | 低 | 高 | 单生日限+班级月预算熔断+缓存降重复调用 |
| 数据合规风险 | 低 | 高 | 隐私设计从Day1；监护人同意前置；数据最小化 |
| 老师抵触 | 中 | 中 | "助手"定位；反馈按钮增强掌控感；充分培训 |

---

# 十、附录

## 10.1 飞书OpenAPI核心能力矩阵

| 能力域 | 可做什么 | 频率限制 | 本项目结合点 |
|--------|----------|----------|--------------|
| IM消息 | 发送文本/富文本/卡片/图片/文件/音频消息 | 1000次/分钟，50次/秒 | 学生端：机器人接收思辨回答 |
| 消息卡片 | 交互式卡片（按钮、图表、表单） | 同消息发送 | 老师端：评估结果卡片 |
| 多维表格 | 数据表、仪表盘、图表、自动化流程 | 10次/秒（写操作） | 老师端：学生评估仪表盘 |
| 云文档 | 创建/读取/更新文档 | 同API标准 | 家长端：自动生成个性化学习报告 |
| 机器人 | 接收消息事件、回复、群聊互动 | 5 QPS（群内） | 学生端：课堂群聊内AI教练互动 |
| 日历 | 创建日程、查询忙闲 | 同API标准 | 课程提醒、评估日程自动创建 |

## 10.2 参考文献

1. Carnegie/ETS 持久技能框架（2026）
2. Paul-Elder 批判性思维模型
3. 皮亚杰认知发展理论
4. Google Vantage - 生成式AI未来技能评估实验（2026）
5. 福建师范大学 - GenAI+协作问题解决对小学生批判性思维影响（2025）
6. Cohen's Kappa: 评分者间一致性度量方法

## 10.3 MVP开发工作量估算

| 模块 | 工作量 | 说明 |
|------|--------|------|
| 评估引擎 + Prompt + 输出校验 | 1.5天 | 评分逻辑 + JSON Schema + 格式修复 |
| 缓存层(Redis) | 0.5天 | SimHash相似度 + 评估结果缓存 |
| 成本熔断器 | 0.5天 | 日限 + 月预算 + 熔断 |
| 教师反馈收集 | 1天 | 反馈按钮 + 漂移检测 + 预警 |
| 飞书集成 | 1天 | 消息接收 + 卡片推送 + 多维表格 |
| 监控面板 | 0.5天 | Grafana + Prometheus |
| 测试 + Kappa验证 | 1天 | 单元测试 + 一致性验证 |
| **合计** | **约7天** | 一个人可完成 |

---

*本方案为2026 AI先锋未来人才大赛参赛作品，由EduSocratic团队设计*

