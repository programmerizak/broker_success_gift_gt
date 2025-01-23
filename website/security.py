def get_security(debug, env):
    # if not debug and not test:
    if not debug :
        return {
            "SESSION_COOKIE_HTTPONLY": True,
            "CSRF_COOKIE_HTTPONLY": False,
            "SECURE_BROWSER_XSS_FILTER": True,
            "X_FRAME_OPTIONS": "DENY",
            "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
            "SESSION_COOKIE_SECURE": True,
            "CSRF_COOKIE_SECURE": True,
            "SECURE_SSL_REDIRECT": True,
            "SECURE_HSTS_SECONDS": env("SECURE_HSTS_SECONDS"),
            "SECURE_HSTS_INCLUDE_SUBDOMAINS": env.bool(
                "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
            ),
            "SECURE_HSTS_PRELOAD": env.bool("SECURE_HSTS_PRELOAD", default=True),
            "SECURE_CONTENT_TYPE_NOSNIFF": env.bool(
                "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
            ),
        }
    return {}
