"""
Rich Text Area

Rich Text Area inherits DraftailRichTextArea
& format value before calling to_database_format
"""
from wagtail.admin.rich_text.editors.draftail import (
    DraftailRichTextArea, DraftailRichTextAreaAdapter)
from wagtail.telepath import register


class RichTextArea(DraftailRichTextArea):
    """ Custom rich text area widget"""
    def value_from_datadict(self, data, files, name):
        original_value = data.get(name)
        if original_value is None:
            return None

        if isinstance(original_value, str):
            original_value = self.format_value(original_value)

        return self.converter.to_database_format(original_value)


register(DraftailRichTextAreaAdapter(), RichTextArea)
