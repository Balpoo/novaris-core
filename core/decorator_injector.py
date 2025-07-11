# core/decorator_injector.py

import types
from core.patch_engine import patch_all_methods


def patch_all_methods(target_class):
    """
    Automatically wraps all public instance methods of a class
    with auto_debug_wrap to log errors and enable self-healing.
    """
    for attr_name in dir(target_class):
        if attr_name.startswith("__"):
            continue  # Skip dunder methods

        attr = getattr(target_class, attr_name)
        if isinstance(attr, (types.FunctionType, types.MethodType)) and callable(attr):
            wrapped = auto_debug_wrap(attr)
            setattr(target_class, attr_name, wrapped)

    return target_class
