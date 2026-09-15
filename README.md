# fastapi-csp-builder

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/fastapi-csp-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Type-safe Content Security Policy (CSP) builder and middleware with automatic per-request cryptographic nonce generation for FastAPI.

---

## 🚀 Features

- 🛡️ **XSS Protection**: Secure your modern web application with production-grade CSP headers.
- 🎲 **Cryptographic Nonce**: Generates unique `request.state.csp_nonce` for inline scripts and styles.
- ⚡ **Type-Safe Builder**: Fluent builder pattern for defining directives (`default-src`, `script-src`, `style-src`).

---

## 📦 Installation

```bash
pip install fastapi-csp-builder
```

---

## 🛠️ Quickstart

```python
from fastapi import FastAPI
from fastapi_csp_builder import CSPMiddleware, CSPConfig

app = FastAPI()

csp = CSPConfig(
    default_src=["'self'"],
    script_src=["'self'", "https://cdn.jsdelivr.net"],
    style_src=["'self'", "'unsafe-inline'"],
    add_nonce=True
)

app.add_middleware(CSPMiddleware, config=csp)
```

---

## ☕ Support My Studies / Buy Me a Coffee

I am an independent developer and student building open-source developer productivity tools. If this CSP builder secured your web applications, please consider supporting my studies:

- ☕ **Buy Me a Coffee:** [ko-fi.com/me1121118](https://ko-fi.com/)
- ⭐ **Star this repository** on GitHub!

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
