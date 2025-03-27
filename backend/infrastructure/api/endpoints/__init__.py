"""Endpoints package for API routes organization."""

from .departments import register_department_routes
from .templates import register_template_routes
from .colors import register_color_routes
from .completion_types import register_completion_type_routes
from .text_managemen import text_management_routes
from .debug import register_debug_routes

__all__ = [
    'register_department_routes',
    'register_template_routes',
    'register_color_routes',
    'register_completion_type_routes',
    'register_debug_routes',
    'text_management_routes'
]