import json
from typing import Optional


class CardBuilder:
    """飞书消息卡片构建器"""

    @staticmethod
    def build_assessment_card(
        student_name: str,
        grade: int,
        topic: str,
        scores: dict,
        weighted_score: float,
        highlights: str,
        suggestions: str,
        overall_comment: str,
        assessment_id: str = ""
    ) -> str:
        """构建老师端评估结果卡片"""

        scores_rows = "\n".join([
            f"| {dim} | {score}分 |"
            for dim, score in scores.items()
        ])

        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"content": f"📊 课堂思辨评估 - {grade}年级", "tag": "plain_text"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": f"**{student_name}** | 主题：{topic}",
                        "tag": "lark_md"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": f"**六维评分：**\n| 维度 | 分数 |\n|---|---|\n{scores_rows}\n\n**加权总分：{weighted_score}分**"
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {"content": f"💡 **亮点：**{highlights}", "tag": "lark_md"}
                },
                {
                    "tag": "div",
                    "text": {"content": f"📌 **建议：**{suggestions}", "tag": "lark_md"}
                },
                {
                    "tag": "div",
                    "text": {"content": f"📝 **总评：**{overall_comment}", "tag": "lark_md"}
                },
                {"tag": "hr"},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"content": "✅ 确认发送", "tag": "plain_text"},
                            "type": "primary",
                            "value": {"action": "confirm", "id": assessment_id}
                        },
                        {
                            "tag": "button",
                            "text": {"content": "✏️ 修改后发送", "tag": "plain_text"},
                            "type": "default",
                            "value": {"action": "edit", "id": assessment_id}
                        },
                        {
                            "tag": "button",
                            "text": {"content": "👎 评分不准确", "tag": "plain_text"},
                            "type": "danger",
                            "value": {"action": "disagree", "id": assessment_id}
                        }
                    ]
                }
            ]
        }

        return json.dumps(card, ensure_ascii=False)

    @staticmethod
    def build_parent_report_card(
        student_name: str,
        grade: int,
        topic: str,
        scores: dict,
        weighted_score: float,
        highlights: str,
        suggestions: str,
        overall_comment: str
    ) -> str:
        """构建家长端学习报告卡片"""

        scores_text = "\n".join([
            f"- {dim}：{'⭐' * score} ({score}/5)"
            for dim, score in scores.items()
        ])

        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"content": f"📚 思辨课堂学习报告", "tag": "plain_text"},
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"content": f"**{student_name}** | {grade}年级 | 主题：{topic}", "tag": "lark_md"}
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": f"**六维评分：**\n{scores_text}\n\n**综合得分：{weighted_score}分**"
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {"content": f"💡 **课堂亮点：**{highlights}", "tag": "lark_md"}
                },
                {
                    "tag": "div",
                    "text": {"content": f"📌 **提升建议：**{suggestions}", "tag": "lark_md"}
                },
                {
                    "tag": "div",
                    "text": {"content": f"📝 **老师寄语：**{overall_comment}", "tag": "lark_md"}
                },
                {"tag": "hr"},
                {
                    "tag": "note",
                    "elements": [{"content": "本报告由AI辅助生成，仅供参考。如有疑问请联系任课老师。", "tag": "plain_text"}]
                }
            ]
        }

        return json.dumps(card, ensure_ascii=False)

    @staticmethod
    def build_encouragement_card(message: str) -> str:
        """构建学生端正向激励卡片"""
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"content": "🌟 你的发言很棒！", "tag": "plain_text"},
                "template": "orange"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"content": message, "tag": "lark_md"}
                }
            ]
        }
        return json.dumps(card, ensure_ascii=False)
