"""Prompt 路由"""

from app.domain.grade_weights import get_grade_band


def get_assessment_prompts(grade: int) -> tuple[str, str]:
    """根据年级返回 (system_prompt, user_prompt_template)"""
    band = get_grade_band(grade)
    if band == "1_2":
        from app.prompts.assessment_1_2 import SYSTEM_PROMPT, USER_PROMPT
    elif band == "3_4":
        from app.prompts.assessment_3_4 import SYSTEM_PROMPT, USER_PROMPT
    else:
        from app.prompts.assessment_5_7 import SYSTEM_PROMPT, USER_PROMPT
    return SYSTEM_PROMPT, USER_PROMPT


def render_assessment_prompt(
    grade: int,
    topic: str,
    text: str,
    teacher_context: str | None = None,
) -> list[dict[str, str]]:
    """渲染完整的 messages 列表"""
    system_tpl, user_tpl = get_assessment_prompts(grade)

    system = system_tpl.format(grade=grade)

    # 教师上下文部分
    if teacher_context:
        from app.prompts.assessment_3_4 import TEACHER_CONTEXT_TEMPLATE
        ctx_section = TEACHER_CONTEXT_TEMPLATE.format(context=teacher_context)
    else:
        ctx_section = ""

    user = user_tpl.format(
        topic=topic,
        text=text,
        teacher_context_section=ctx_section,
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
