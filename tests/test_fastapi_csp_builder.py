import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi_csp_builder import CSPMiddleware, CSPConfig

def test_csp_middleware():
    app = FastAPI()
    app.add_middleware(CSPMiddleware, config=CSPConfig(add_nonce=True))

    @app.get("/page")
    def page(req: Request):
        return {"nonce": req.state.csp_nonce}

    client = TestClient(app)
    res = client.get("/page")
    assert res.status_code == 200
    assert "Content-Security-Policy" in res.headers
    csp_header = res.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp_header
    assert "'nonce-" in csp_header
