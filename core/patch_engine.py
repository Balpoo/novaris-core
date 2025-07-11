# core/patch_engine.py

# ❌ Remove this:
# from agents.auto_debug_agent import auto_debug_wrap


# ✅ Replace it with a lazy import inside the function
def patch_all_methods(obj):
    from agents.auto_debug_agent import auto_debug_wrap  # Lazy import

    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if callable(attr) and not attr_name.startswith("__"):
            try:
                setattr(obj, attr_name, auto_debug_wrap(attr))
            except Exception:
                pass
    return obj
