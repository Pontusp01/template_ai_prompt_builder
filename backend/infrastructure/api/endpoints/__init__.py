# infrastructure/api/endpoints/__init__.py
"""Endpoints package for API routes organization."""

# Ändra dessa importer för att matcha din faktiska filstruktur
# Om filerna ligger direkt i endpoints-katalogen:
from infrastructure.api.endpoints.departments import register_department_routes
from infrastructure.api.endpoints.templates import register_template_routes
from infrastructure.api.endpoints.colors import register_color_routes
from infrastructure.api.endpoints.completion_types import register_completion_type_routes
from infrastructure.api.endpoints.text_managemen import register_text_management_routes
from infrastructure.api.endpoints.debug import register_debug_routes

__all__ = [
    'register_department_routes',
    'register_template_routes',
    'register_color_routes',
    'register_completion_type_routes',
    'register_text_management_routes',
    'register_debug_routes'
]