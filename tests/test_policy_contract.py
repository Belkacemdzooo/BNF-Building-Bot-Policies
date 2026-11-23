from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocumentLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.html_attrs: dict[str, str | None] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_attrs = values
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")


class PolicyContractTests(unittest.TestCase):
    def read_page(self, name: str) -> str:
        path = ROOT / name
        self.assertTrue(path.is_file(), f"Missing legal page: {name}")
        return path.read_text(encoding="utf-8")

    def test_privacy_page_preserves_arabic_rtl_and_retention_contract(self) -> None:
        html = self.read_page("privacy-policy.html")
        parser = DocumentLinks()
        parser.feed(html)

        self.assertEqual(parser.html_attrs.get("lang"), "ar")
        self.assertEqual(parser.html_attrs.get("dir"), "rtl")
        self.assertIn("bnf.building@gmail.com", html)
        self.assertIn("إلى أن نتلقى طلباً صالحاً لحذفها", html)
        self.assertIn("until we receive a valid deletion request", html)
        self.assertIn("نسخ تقنية احتياطية", html)
        self.assertIn("Technical backups", html)

    def test_data_deletion_page_has_a_real_request_path_and_safety_notice(self) -> None:
        html = self.read_page("data-deletion.html")
        parser = DocumentLinks()
        parser.feed(html)

        self.assertIn("mailto:bnf.building@gmail.com", html)
        self.assertIn("+213", html)
        self.assertIn("طلب حذف بيانات WhatsApp", html)
        self.assertIn("Data Deletion Request", html)
        self.assertIn("لا ترسل كلمة مرور أو رمز تحقق", html)
        self.assertIn("Do not send passwords or verification codes", html)

    def test_terms_disclose_automated_reply_limitations(self) -> None:
        html = self.read_page("terms-of-service.html")
        self.assertIn("غير دقيقة أو غير محدثة", html)
        self.assertIn("not a binding offer", html)
        self.assertIn("اطلب تأكيداً", html)

    def test_all_local_navigation_targets_exist(self) -> None:
        pages = (
            "index.html",
            "privacy-policy.html",
            "terms-of-service.html",
            "data-deletion.html",
        )
        for page in pages:
            html = self.read_page(page)
            parser = DocumentLinks()
            parser.feed(html)
            for href in parser.links:
                if href.startswith(("mailto:", "https://", "http://", "#", "tel:")):
                    continue
                target = href.split("#", 1)[0].split("?", 1)[0]
                if target:
                    self.assertTrue(
                        (ROOT / target).is_file(),
                        f"{page} links to missing local target {href}",
                    )


if __name__ == "__main__":
    unittest.main()
