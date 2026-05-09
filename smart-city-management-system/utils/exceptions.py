# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class SmartCityException(Exception):
    """Base exception for Smart City application"""
    pass


class DatabaseException(SmartCityException):
    """Database operation exception"""
    pass


class AuthenticationException(SmartCityException):
    """Authentication failure exception"""
    pass


class AuthorizationException(SmartCityException):
    """Authorization failure exception"""
    pass


class ValidationException(SmartCityException):
    """Data validation exception"""
    pass


class ResourceNotFoundException(SmartCityException):
    """Resource not found exception"""
    pass


class DuplicateResourceException(SmartCityException):
    """Duplicate resource exception"""
    pass


class ConfigurationException(SmartCityException):
    """Configuration error exception"""
    pass


class NotImplementedException(SmartCityException):
    """Feature not implemented exception"""
    pass
