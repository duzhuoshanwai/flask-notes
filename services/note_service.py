from utils import get_db_connection
from sqlite3 import Error
import os
from markupsafe import escape
import bleach
from mistune import create_markdown

class NoteService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.timezone = os.environ.get("TIMEZONE", "+8")
        self.markdown = create_markdown(escape=True)
        self.custom_allowed_tags = [
            "address",
            "article",
            "aside",
            "footer",
            "header",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "hgroup",
            "main",
            "nav",
            "section",
            "blockquote",
            "dd",
            "div",
            "dl",
            "dt",
            "figcaption",
            "figure",
            "hr",
            "li",
            "main",
            "ol",
            "p",
            "pre",
            "ul",
            "a",
            "abbr",
            "b",
            "bdi",
            "bdo",
            "br",
            "cite",
            "code",
            "data",
            "dfn",
            "em",
            "i",
            "kbd",
            "mark",
            "q",
            "rb",
            "rp",
            "rt",
            "rtc",
            "ruby",
            "s",
            "samp",
            "small",
            "span",
            "strong",
            "sub",
            "sup",
            "time",
            "u",
            "var",
            "wbr",
            "caption",
            "col",
            "colgroup",
            "table",
            "tbody",
            "td",
            "tfoot",
            "th",
            "thead",
            "tr",
            "img",
            "a",
        ]
        self.custom_allowed_attributes = {
            "a": ["href", "name", "target"],
            "img": ["src", "srcset", "alt", "title", "width", "height", "loading"],
        }

    def html_clean(self, dirty_html):
        return bleach.clean(
            dirty_html,
            tags=self.custom_allowed_tags,
            attributes=self.custom_allowed_attributes,
            protocols=["http", "https", "ftp", "mailto", "tel"],
            strip=True,
        )

    def get_notes(self, page: int = 1, limit: int = 10) -> list:
        """获取分页笔记列表（渲染时清理）"""
        offset = (page - 1) * limit
        with get_db_connection(self.db_path) as conn:
            db_notes = conn.execute(
                "SELECT * FROM notes ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()

        return [
            {
                "id": note["id"],
                "created_at": note["created_at"],
                "edited_at": note["edited_at"],
                "title": escape(note["title"]),
                "content": self.html_clean(self.markdown(note["content"])),
            }
            for note in db_notes
        ]

    def get_note_by_id(self, id: int, md_type: bool) -> dict:
        """
        根据ID获取单条note
        md_type true返回markdown格式，false返回html格式
        """
        with get_db_connection(self.db_path) as conn:
            note = conn.execute(
                f"""
                SELECT 
                    id,
                    title,
                    content,
                    datetime(created_at, '{self.timezone} hours') as created_at,
                    datetime(edited_at, '{self.timezone} hours') as edited_at
                FROM notes 
                WHERE id = ?""",
                (id,),
            ).fetchone()

        if note:
            return {
                "id": note["id"],
                "title": escape(note["title"]),  # TODO: 重新实现渲染逻辑
                "content": note["content"] if md_type else self.html_clean(self.markdown(note["content"])),
                "created_at": note["created_at"],
                "edited_at": note["edited_at"],
            }
        return None

    def create_note(self, title: str, md_content: str) -> bool:
        """创建笔记（存储前清理）"""
        # TODO: 重新实现消毒逻辑
        sanitized_title = title
        sanitized_content = md_content

        with get_db_connection(self.db_path) as conn:
            try:
                conn.execute(
                    "INSERT INTO notes (title, content) VALUES (?, ?)",
                    (sanitized_title, sanitized_content),
                )
                conn.commit()
                return True
            except Error as e:
                print(f"数据库错误: {e}")
                return False

    def update_note(self, id: int, title: str, md_content: str) -> bool:
        """更新笔记（存储前清理）"""
        # TODO: 重新实现消毒逻辑
        sanitized_title = title
        sanitized_content = md_content

        with get_db_connection(self.db_path) as conn:
            try:
                conn.execute(
                    "UPDATE notes SET title = ?, content = ?, edited_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (sanitized_title, sanitized_content, id),
                )
                conn.commit()
                return True
            except Error as e:
                print(f"数据库更新错误: {e}")
                return False

    def get_total_notes(self) -> int:
        """获取总note数"""
        with get_db_connection(self.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        return count
