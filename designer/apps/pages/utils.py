""" Page utils """


def is_valid_child_page(cls, parent_child_pages):
    """
    When adding a child page (e.g., ProgramPage, EnterprisePage), we want to ensure
    only child pages of the same type can exist under their parent page.

    For example:
    - if the parent page has no children, the page would be a valid sibling.
    - if the parent page already has a child page `ProgramPage`, then only
      a new `ProgramPage` is valid under the parent page.

    .. no_pii:
    """
    for child_page in parent_child_pages:
        if not isinstance(child_page.specific, cls):
            return False
    return True
