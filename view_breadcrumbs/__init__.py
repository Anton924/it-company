"""Top-level package for view_breadcrumbs."""

__author__ = """Tonye Jack"""
__email__ = "jtonye@ymail.com"
__version__ = "2.5.1"

from .generic import (
    BaseBreadcrumbMixin,
    CreateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
    UpdateWithNoDetailBreadcrumbMixin
)

__all__ = [
    "BaseBreadcrumbMixin",
    "CreateBreadcrumbMixin",
    "DetailBreadcrumbMixin",
    "ListBreadcrumbMixin",
    "UpdateBreadcrumbMixin",
    "DeleteBreadcrumbMixin",
    "UpdateWithNoDetailBreadcrumbMixin"
]
