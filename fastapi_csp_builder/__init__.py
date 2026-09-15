import secrets
from typing import List, Optional
from dataclasses import dataclass, field
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.datastructures import MutableHeaders

@dataclass
class CSPConfig:
    default_src: List[str] = field(default_factory=lambda: ["'self'"])
    script_src: List[str] = field(default_factory=lambda: ["'self'"])
    style_src: List[str] = field(default_factory=lambda: ["'self'"])
    img_src: List[str] = field(default_factory=lambda: ["'self'", "data:", "https:"])
    font_src: List[str] = field(default_factory=lambda: ["'self'"])
    connect_src: List[str] = field(default_factory=lambda: ["'self'"])
    add_nonce: bool = True

    def build_header(self, nonce: Optional[str] = None) -> str:
        directives = []
        if self.default_src:
            directives.append(f"default-src {' '.join(self.default_src)}")
        
        script_sources = list(self.script_src)
        if self.add_nonce and nonce:
            script_sources.append(f"'nonce-{nonce}'")
        if script_sources:
            directives.append(f"script-src {' '.join(script_sources)}")

        if self.style_src:
            directives.append(f"style-src {' '.join(self.style_src)}")
        if self.img_src:
            directives.append(f"img-src {' '.join(self.img_src)}")
        if self.font_src:
            directives.append(f"font-src {' '.join(self.font_src)}")
        if self.connect_src:
            directives.append(f"connect-src {' '.join(self.connect_src)}")

        return "; ".join(directives)

class CSPMiddleware:
    def __init__(self, app: ASGIApp, config: Optional[CSPConfig] = None):
        self.app = app
        self.config = config or CSPConfig()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        nonce = secrets.token_urlsafe(16)
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["csp_nonce"] = nonce

        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                header_val = self.config.build_header(nonce)
                res_headers = MutableHeaders(raw=list(message.get("headers", [])))
                res_headers["Content-Security-Policy"] = header_val
                message["headers"] = res_headers.raw
            await send(message)

        await self.app(scope, receive, send_wrapper)
