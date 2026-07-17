from typing import Optional


class ReportTemplateManager:
    """报告模板管理"""

    TEMPLATES = {
        "weekly": "templates/weekly_report.md",
        "monthly": "templates/monthly_report.md",
    }

    def get_template(self, template_type: str) -> str:
        return self.TEMPLATES.get(template_type, self.TEMPLATES["weekly"])
