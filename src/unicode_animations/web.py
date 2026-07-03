"""Browser demo server for unicode_animations."""

from __future__ import annotations

import argparse
import json
import webbrowser
from collections.abc import Sequence
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TypedDict
from urllib.parse import urlparse

from .braille import BRAILLE_SPINNER_NAMES, spinners


class SpinnerPayload(TypedDict):
    frames: list[str]
    interval: int


def build_spinner_payload() -> dict[str, SpinnerPayload]:
    """Return JSON-friendly spinner data for the web preview."""
    return {
        name: {
            "frames": list(spinners[name].frames),
            "interval": spinners[name].interval,
        }
        for name in BRAILLE_SPINNER_NAMES
    }


def build_demo_html() -> str:
    """Return demo HTML that loads spinner data from /spinners.json."""
    return """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>unicode-animatio</title>
  <style>
    :root {
      --bg: #14171a;
      --panel: #1b2128;
      --border: #2f3945;
      --text: #ecf2f8;
      --muted: #a7b4c2;
      --soft: #8191a3;
      --accent: #2ec4b6;
      --mono: 'Cascadia Mono', 'SF Mono', 'Menlo', monospace;
      --sans: 'Avenir Next', 'Segoe UI', sans-serif;
    }

    [data-theme="light"] {
      --bg: #f2f6f9;
      --panel: #ffffff;
      --border: #d8e1ea;
      --text: #1d2935;
      --muted: #516276;
      --soft: #76879a;
      --accent: #0b8f83;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: var(--sans);
      color: var(--text);
      background:
        radial-gradient(circle at 0% 0%, rgba(46, 196, 182, 0.16), transparent 42%),
        radial-gradient(circle at 100% 100%, rgba(11, 143, 131, 0.14), transparent 45%),
        var(--bg);
    }

    .wrap {
      max-width: 860px;
      margin: 0 auto;
      padding: 2.2rem 1.2rem 3rem;
    }

    .top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.25rem;
    }

    h1 {
      margin: 0;
      font-size: 1.75rem;
      letter-spacing: -0.02em;
    }

    .sub {
      margin-top: 0.45rem;
      color: var(--soft);
      font-size: 0.94rem;
    }

    .toggle {
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--muted);
      border-radius: 10px;
      padding: 0.45rem 0.7rem;
      font-size: 0.78rem;
      cursor: pointer;
    }

    .panel {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: color-mix(in srgb, var(--panel) 93%, transparent);
      overflow: hidden;
    }

    .row {
      display: flex;
      align-items: center;
      gap: 0.9rem;
      padding: 0.64rem 0.95rem;
      border-bottom: 1px solid var(--border);
    }

    .row:last-child { border-bottom: none; }

    .frame {
      width: 6.2rem;
      text-align: center;
      color: var(--accent);
      font-family: var(--mono);
      white-space: nowrap;
      font-size: 1rem;
      font-weight: 700;
    }

    .name {
      font-weight: 600;
      font-size: 0.9rem;
      min-width: 8rem;
    }

    .meta {
      margin-left: auto;
      color: var(--soft);
      font-size: 0.78rem;
      font-family: var(--mono);
    }

    .foot {
      margin-top: 1rem;
      color: var(--soft);
      font-size: 0.78rem;
      font-family: var(--mono);
    }

    @media (max-width: 640px) {
      .row {
        flex-wrap: wrap;
        gap: 0.45rem 0.8rem;
      }

      .meta {
        margin-left: 0;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div>
        <h1>unicode-animatio</h1>
        <div class="sub">18 braille spinner animations served from local Python data</div>
      </div>
      <button class="toggle" id="themeToggle" type="button">Theme</button>
    </div>

    <div class="panel" id="spinnerPanel"></div>

    <div class="foot">
      CLI: <code>unicode-animatio --list</code> | <code>unicode-animatio helix</code>
    </div>
  </div>

  <script>
    const panel = document.getElementById('spinnerPanel');
    const els = {};

    function buildRows(spinners) {
      Object.entries(spinners).forEach(([name, s]) => {
        const row = document.createElement('div');
        row.className = 'row';

        const frame = document.createElement('span');
        frame.className = 'frame';
        frame.textContent = s.frames[0];

        const label = document.createElement('span');
        label.className = 'name';
        label.textContent = name;

        const meta = document.createElement('span');
        meta.className = 'meta';
        meta.textContent = `${s.frames.length}f / ${s.interval}ms`;

        row.append(frame, label, meta);
        panel.appendChild(row);
        els[name] = frame;
      });
    }

    function startAnimation(spinners) {
      const byInterval = {};
      Object.entries(spinners).forEach(([name, s]) => {
        if (!byInterval[s.interval]) byInterval[s.interval] = [];
        byInterval[s.interval].push({ name, frames: s.frames, i: 0 });
      });

      Object.entries(byInterval).forEach(([interval, group]) => {
        window.setInterval(() => {
          group.forEach((entry) => {
            entry.i = (entry.i + 1) % entry.frames.length;
            els[entry.name].textContent = entry.frames[entry.i];
          });
        }, Number(interval));
      });
    }

    async function init() {
      const response = await fetch('/spinners.json');
      const spinnerData = await response.json();
      buildRows(spinnerData);
      startAnimation(spinnerData);
    }

    init();

    const toggle = document.getElementById('themeToggle');
    toggle.addEventListener('click', () => {
      const dark = document.documentElement.dataset.theme === 'dark';
      document.documentElement.dataset.theme = dark ? 'light' : 'dark';
    });
  </script>
</body>
</html>
"""


def create_demo_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    """Create an HTTP server exposing the demo page and spinner JSON data."""
    payload = build_spinner_payload()
    payload_json = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    html = build_demo_html().encode("utf-8")

    def _write_response(
        handler: BaseHTTPRequestHandler,
        *,
        content_type: str,
        body: bytes,
        status: int = 200,
        cache_control: str | None = None,
    ) -> None:
        handler.send_response(status)
        handler.send_header("Content-Type", content_type)
        if cache_control is not None:
            handler.send_header("Cache-Control", cache_control)
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)

    class DemoHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            route = urlparse(self.path).path

            if route in ("/", "/index.html"):
                _write_response(self, content_type="text/html; charset=utf-8", body=html)
                return

            if route == "/spinners.json":
                _write_response(
                    self,
                    content_type="application/json; charset=utf-8",
                    body=payload_json,
                    cache_control="no-store",
                )
                return

            _write_response(
                self,
                status=404,
                content_type="text/plain; charset=utf-8",
                body=b"Not Found",
            )

        def log_message(self, format: str, *args: object) -> None:  # noqa: A003
            # Keep CLI output clean for demo usage.
            return

    return ThreadingHTTPServer((host, port), DemoHandler)


def serve_demo(host: str = "127.0.0.1", port: int = 0, open_browser: bool = True) -> int:
    """Serve the web demo until interrupted."""
    server = create_demo_server(host=host, port=port)
    bound_host, bound_port = server.server_address
    url = f"http://{bound_host}:{bound_port}/"

    print(f"Serving unicode-animatio web demo at {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping demo server...")
    finally:
        server.server_close()

    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unicode-animatio-web",
        description="Run a local browser demo for unicode_animations.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=0, help="Port to bind (default: auto)")
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not auto-open the browser",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return serve_demo(host=args.host, port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    raise SystemExit(main())
