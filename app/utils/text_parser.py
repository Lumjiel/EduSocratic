"""解析老师输入的文字指令"""

import re
from app.domain.schemas import ParsedCommand


def parse_teacher_message(text: str) -> ParsedCommand:
    """
    解析老师 @机器人 后的文字。

    支持格式：
    "评估 学生:小明 年级:3 主题:动物穿衣服 发言:我觉得..."
    "小明 3年级 动物穿衣服\\n我觉得..."
    "帮助"
    "查询 小明"
    "生成周报"
    """
    text = text.strip()

    # 去除 @机器人 的部分（飞书会带 @mention）
    text = re.sub(r'@[\w]+\s*', '', text).strip()

    # 帮助
    if text in ("帮助", "help", "?", "？"):
        return ParsedCommand(action="help", raw_message=text)

    # 查询
    if text.startswith("查询"):
        name = text.replace("查询", "").strip()
        return ParsedCommand(action="query", student_name=name or None, raw_message=text)

    # 周报
    if "周报" in text:
        return ParsedCommand(action="weekly_report", raw_message=text)

    # 取消
    if text in ("取消", "cancel"):
        return ParsedCommand(action="cancel", raw_message=text)

    # 评估（默认）
    return _parse_assessment(text)


def _parse_assessment(text: str) -> ParsedCommand:
    """解析评估请求"""
    student_name = None
    grade = None
    topic = None
    speech_text = None

    # 尝试提取 "学生:XXX" 或 "学生：XXX"
    m = re.search(r'学生[:：]\s*(\S+)', text)
    if m:
        student_name = m.group(1)

    # 尝试提取 "年级:N" 或 "N年级"
    m = re.search(r'年级[:：]?\s*(\d)', text)
    if m:
        grade = int(m.group(1))
    else:
        m = re.search(r'(\d)\s*年级', text)
        if m:
            grade = int(m.group(1))

    # 尝试提取 "主题:XXX" 或 "主题：XXX"
    m = re.search(r'主题[:：]\s*(.+?)(?:\s+(?:学生|年级|发言)|$)', text)
    if m:
        topic = m.group(1).strip()

    # 尝试提取 "发言:XXX" 或引号内的文字
    m = re.search(r'发言[:：]\s*(.+)', text, re.DOTALL)
    if m:
        speech_text = m.group(1).strip()
    else:
        # 尝试引号（中英文引号、「」）
        m = re.search(r'["“「](.+?)["”」]', text, re.DOTALL)
        if m:
            speech_text = m.group(1).strip()

    # 如果以上都没提取到发言文字，尝试取最后一行非元信息文字
    if not speech_text:
        lines = text.split('\n')
        # 过滤掉包含元信息关键词的行
        content_lines = [
            l for l in lines
            if not re.search(r'(学生|年级|主题|评估|发言)[:：]', l)
            and not re.search(r'^\d+\s*年级', l)
            and l.strip()
        ]
        if content_lines:
            speech_text = '\n'.join(content_lines).strip()

    return ParsedCommand(
        action="assess",
        student_name=student_name,
        grade=grade,
        topic=topic,
        text=speech_text,
        raw_message=text,
    )
