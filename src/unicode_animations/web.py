"""Browser demo server for unicode_animations."""

from __future__ import annotations

import argparse
import json
import webbrowser
from collections.abc import Sequence
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TypedDict, cast
from urllib.parse import urlparse

from . import __version__
from .catalog import (
    CATEGORY_NAMES,
    SPINNER_NAMES,
    metadata_for_spinner,
    spinners,
)


class SpinnerPayload(TypedDict):
    frames: list[str]
    interval: int
    interval_ms: int
    category: str
    tags: list[str]
    frame_count: int
    frame_width: int
    preview_frame: str
    motion: str
    description: str


DEMO_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>unicode-animatio gallery</title>
  <style>
    :root {
      --bg: #101316;
      --band: #161b20;
      --panel: #1f252b;
      --panel-strong: #252c33;
      --border: #38434e;
      --text: #f0f5f8;
      --muted: #aab6c2;
      --soft: #7d8b98;
      --accent: #31d4bd;
      --accent-2: #f3c969;
      --danger: #f27a7a;
      --shadow: rgba(0, 0, 0, 0.24);
      --mono: 'Cascadia Mono', 'SF Mono', 'Menlo', monospace;
      --sans: 'Inter', 'Avenir Next', 'Segoe UI', sans-serif;
    }

    [data-theme="light"] {
      --bg: #f5f8fb;
      --band: #eaf0f6;
      --panel: #ffffff;
      --panel-strong: #f2f6fa;
      --border: #d5e0ea;
      --text: #18222d;
      --muted: #526274;
      --soft: #718295;
      --accent: #0b8f83;
      --accent-2: #926b12;
      --danger: #b34242;
      --shadow: rgba(29, 41, 53, 0.1);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: var(--sans);
      color: var(--text);
      background: linear-gradient(180deg, var(--band), var(--bg) 22rem);
    }

    button, input {
      font: inherit;
    }

    button:focus-visible,
    input:focus-visible {
      outline: 3px solid color-mix(in srgb, var(--accent) 72%, transparent);
      outline-offset: 2px;
    }

    button:disabled {
      cursor: not-allowed;
      opacity: 0.55;
    }

    .wrap {
      max-width: 1160px;
      margin: 0 auto;
      padding: 2rem 1.1rem 3rem;
    }

    .top {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 1rem;
      align-items: start;
      margin-bottom: 1.2rem;
    }

    h1 {
      margin: 0;
      font-size: 2rem;
      line-height: 1.08;
    }

    .sub {
      max-width: 46rem;
      margin-top: 0.55rem;
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1.5;
    }

    .toolbar {
      display: grid;
      grid-template-columns: minmax(12rem, 1fr) auto;
      gap: 0.7rem;
      align-items: center;
      margin-bottom: 0.8rem;
    }

    .search {
      width: 100%;
      min-height: 2.6rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0 0.8rem;
      color: var(--text);
      background: var(--panel);
      outline: none;
    }

    .button {
      min-height: 2.6rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0 0.8rem;
      color: var(--text);
      background: var(--panel);
      cursor: pointer;
    }

    .button[aria-pressed="true"] {
      border-color: color-mix(in srgb, var(--accent) 72%, var(--border));
      color: var(--accent);
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-bottom: 0.65rem;
    }

    .chip {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 0.42rem 0.7rem;
      color: var(--muted);
      background: var(--panel);
      cursor: pointer;
    }

    .chip[aria-pressed="true"] {
      border-color: var(--accent);
      color: var(--text);
      background: color-mix(in srgb, var(--accent) 18%, var(--panel));
    }

    .results-status {
      margin-bottom: 0.9rem;
      color: var(--muted);
      font-family: var(--mono);
      font-size: 0.78rem;
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(17rem, 21rem);
      gap: 1rem;
      align-items: start;
    }

    .gallery {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
      gap: 0.75rem;
    }

    .card {
      min-height: 10.6rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.85rem;
      color: var(--text);
      background: var(--panel);
      box-shadow: 0 12px 28px var(--shadow);
      cursor: pointer;
      text-align: left;
    }

    .card[aria-selected="true"] {
      border-color: var(--accent);
      outline: 2px solid color-mix(in srgb, var(--accent) 28%, transparent);
    }

    .frame {
      display: grid;
      min-height: 3.5rem;
      place-items: center;
      border-radius: 6px;
      color: var(--accent);
      background: var(--panel-strong);
      font-family: var(--mono);
      font-size: 1.35rem;
      font-weight: 700;
      white-space: pre;
    }

    .card[data-motion="high"] .frame {
      color: var(--danger);
    }

    .card[data-category="graph"] .frame,
    .card[data-category="data"] .frame {
      color: var(--accent-2);
    }

    .card-title {
      display: flex;
      justify-content: space-between;
      gap: 0.7rem;
      margin-top: 0.7rem;
      font-weight: 700;
    }

    .category {
      color: var(--soft);
      font-family: var(--mono);
      font-size: 0.72rem;
      font-weight: 500;
    }

    .meta {
      margin-top: 0.55rem;
      color: var(--muted);
      font-family: var(--mono);
      font-size: 0.74rem;
      line-height: 1.45;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
      margin-top: 0.55rem;
    }

    .tag {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 0.2rem 0.42rem;
      color: var(--soft);
      font-size: 0.7rem;
    }

    .details {
      position: sticky;
      top: 1rem;
      scroll-margin-top: 1rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem;
      background: var(--panel);
      box-shadow: 0 12px 28px var(--shadow);
    }

    .detail-frame {
      display: grid;
      min-height: 6rem;
      place-items: center;
      border-radius: 8px;
      color: var(--accent);
      background: var(--panel-strong);
      font-family: var(--mono);
      font-size: 2rem;
      font-weight: 800;
      white-space: pre;
    }

    .details h2 {
      margin: 0.9rem 0 0.35rem;
      font-size: 1.25rem;
    }

    .detail-list {
      display: grid;
      gap: 0.45rem;
      margin: 0.75rem 0 0;
      color: var(--muted);
      font-family: var(--mono);
      font-size: 0.78rem;
    }

    .snippet {
      margin-top: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.7rem;
      overflow-x: auto;
      color: var(--text);
      background: var(--bg);
      font-family: var(--mono);
      font-size: 0.75rem;
      white-space: pre-wrap;
    }

    .detail-copy {
      width: 100%;
      margin-top: 0.75rem;
    }

    .empty {
      border: 1px dashed var(--border);
      border-radius: 8px;
      padding: 1rem;
      color: var(--muted);
      background: var(--panel);
    }

    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    @media (max-width: 840px) {
      .top,
      .layout {
        grid-template-columns: 1fr;
      }

      .toolbar {
        grid-template-columns: 1fr;
      }

      .details {
        order: -1;
        position: static;
      }
    }
  </style>
</head>
<body>
  <main class="wrap">
    <header class="top">
      <div>
        <h1>unicode-animatio</h1>
        <div class="sub">
          __CATALOG_COUNT__ deterministic Unicode and ASCII terminal animations,
          with category metadata for host-owned renderers.
        </div>
      </div>
      <button class="button" id="themeToggle" type="button">Light theme</button>
    </header>

    <section class="toolbar" aria-label="Gallery controls">
      <input
        class="search"
        id="searchInput"
        type="search"
        aria-label="Search animations"
        placeholder="Search names, categories, tags..."
        autocomplete="off"
      />
      <button class="button" id="motionToggle" type="button" aria-pressed="false">
        Reduced motion
      </button>
    </section>

    <div class="visually-hidden" id="copyStatus" role="status"></div>

    <nav class="chips" id="categoryChips" aria-label="Category filters"></nav>
    <div class="results-status" id="resultsStatus" role="status"></div>

    <section class="layout">
      <div>
        <div
          class="gallery"
          id="spinnerGallery"
          role="listbox"
          aria-label="Animation presets"
          aria-describedby="resultsStatus"
        ></div>
        <div class="empty" id="emptyState" hidden></div>
      </div>
      <aside class="details" id="detailsPanel">
        <div id="detailsContent" aria-live="polite"></div>
        <button class="button detail-copy" id="copyCurrent" type="button" disabled>
          Copy snippet
        </button>
      </aside>
    </section>
  </main>

  <script>
    const gallery = document.getElementById('spinnerGallery');
    const emptyState = document.getElementById('emptyState');
    const detailsPanel = document.getElementById('detailsPanel');
    const detailsContent = document.getElementById('detailsContent');
    const searchInput = document.getElementById('searchInput');
    const categoryChips = document.getElementById('categoryChips');
    const resultsStatus = document.getElementById('resultsStatus');
    const motionToggle = document.getElementById('motionToggle');
    const copyCurrent = document.getElementById('copyCurrent');
    const copyStatus = document.getElementById('copyStatus');
    const themeToggle = document.getElementById('themeToggle');
    const themePreferenceKey = 'unicode-animatio:theme';
    const motionPreferenceKey = 'unicode-animatio:motion';
    const categoryNames = __CATEGORY_NAMES__;
    const frameEls = {};
    const cardEls = {};
    let spinners = {};
    let activeCategory = 'all';
    let selectedName = '';
    let reducedMotion = false;

    function setTheme(theme) {
      document.documentElement.dataset.theme = theme;
      const nextTheme = theme === 'dark' ? 'light' : 'dark';
      themeToggle.textContent = `${nextTheme[0].toUpperCase()}${nextTheme.slice(1)} theme`;
    }

    function setReducedMotion(value) {
      reducedMotion = value;
      motionToggle.setAttribute('aria-pressed', String(reducedMotion));
      if (!reducedMotion) return;
      Object.entries(spinners).forEach(([name, spinner]) => {
        if (frameEls[name]) frameEls[name].textContent = spinner.preview_frame;
      });
      if (frameEls.__detail && spinners[selectedName]) {
        frameEls.__detail.textContent = spinners[selectedName].preview_frame;
      }
    }

    function initializePreferences() {
      const savedTheme = window.localStorage.getItem(themePreferenceKey);
      const savedMotion = window.localStorage.getItem(motionPreferenceKey);
      const systemTheme = window.matchMedia('(prefers-color-scheme: light)').matches;
      const systemMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      setTheme(savedTheme || (systemTheme ? 'light' : 'dark'));
      setReducedMotion(savedMotion ? savedMotion === 'reduce' : systemMotion);
    }

    function spinnerSnippet(name) {
      return [
        'from unicode_animations import get_provider',
        '',
        'provider = get_provider()',
        `animation = provider.get('${name}')`,
      ].join('\\n');
    }

    async function copyText(text) {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
        return;
      }
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      textArea.remove();
    }

    function renderChips() {
      const categories = ['all', ...categoryNames];
      categoryChips.replaceChildren();
      categories.forEach((category) => {
        const button = document.createElement('button');
        button.className = 'chip';
        button.type = 'button';
        button.textContent = category;
        button.setAttribute('aria-pressed', String(category === activeCategory));
        button.addEventListener('click', () => {
          activeCategory = category;
          categoryChips.querySelectorAll('.chip').forEach((chip) => {
            chip.setAttribute('aria-pressed', String(chip.textContent === activeCategory));
          });
          renderGallery();
        });
        categoryChips.appendChild(button);
      });
    }

    function selectSpinner(name) {
      selectedName = name;
      Object.entries(cardEls).forEach(([cardName, card]) => {
        const selected = cardName === selectedName;
        card.setAttribute('aria-selected', String(selected));
        card.tabIndex = selected ? 0 : -1;
      });
      renderDetails();
      cardEls[name].focus();
    }

    function moveCardSelection(name, event) {
      const names = Object.keys(cardEls);
      const current = names.indexOf(name);
      const offsets = { ArrowLeft: -1, ArrowUp: -1, ArrowRight: 1, ArrowDown: 1 };
      let next = current;
      if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = names.length - 1;
      else if (event.key in offsets) {
        next = (current + offsets[event.key] + names.length) % names.length;
      } else {
        return;
      }
      event.preventDefault();
      selectSpinner(names[next]);
    }

    function buildCard(name, spinner) {
      const card = document.createElement('button');
      card.className = 'card';
      card.type = 'button';
      card.setAttribute('role', 'option');
      card.dataset.category = spinner.category;
      card.dataset.motion = spinner.motion;
      card.setAttribute('aria-selected', String(name === selectedName));
      card.tabIndex = name === selectedName ? 0 : -1;
      card.addEventListener('click', () => {
        selectSpinner(name);
        if (window.matchMedia('(max-width: 840px)').matches) detailsPanel.scrollIntoView();
      });
      card.addEventListener('keydown', (event) => moveCardSelection(name, event));
      cardEls[name] = card;

      const frame = document.createElement('div');
      frame.className = 'frame';
      frame.setAttribute('aria-hidden', 'true');
      frame.textContent = spinner.preview_frame;
      frameEls[name] = frame;

      const title = document.createElement('div');
      title.className = 'card-title';
      title.innerHTML = `<span>${name}</span><span class="category">${spinner.category}</span>`;

      const meta = document.createElement('div');
      meta.className = 'meta';
      meta.textContent = `${spinner.frame_count} frames / ${spinner.interval_ms}ms`;

      const tags = document.createElement('div');
      tags.className = 'tags';
      spinner.tags.forEach((tag) => {
        const tagEl = document.createElement('span');
        tagEl.className = 'tag';
        tagEl.textContent = tag;
        tags.appendChild(tagEl);
      });

      card.append(frame, title, meta, tags);
      return card;
    }

    function renderGallery() {
      gallery.replaceChildren();
      Object.keys(frameEls).forEach((key) => delete frameEls[key]);
      Object.keys(cardEls).forEach((key) => delete cardEls[key]);
      const query = searchInput.value.trim();
      const normalizedQuery = query.toLowerCase();
      const visible = Object.entries(spinners).filter(([name, spinner]) => {
        const categoryMatch = activeCategory === 'all' || spinner.category === activeCategory;
        const text = [name, spinner.category, ...spinner.tags].join(' ').toLowerCase();
        return categoryMatch && (!normalizedQuery || text.includes(normalizedQuery));
      });

      if (!visible.some(([name]) => name === selectedName) && visible.length > 0) {
        selectedName = visible[0][0];
      }
      if (visible.length === 0) selectedName = '';
      visible.forEach(([name, spinner]) => gallery.appendChild(buildCard(name, spinner)));
      const noun = visible.length === 1 ? 'animation' : 'animations';
      const category = activeCategory === 'all' ? '' : `${activeCategory} `;
      const match = query ? ` matching “${query}”` : '';
      resultsStatus.textContent = `${visible.length} ${category}${noun}${match}`;
      emptyState.hidden = visible.length > 0;
      emptyState.textContent = visible.length > 0 ? '' : 'No matching animations.';
      renderDetails();
    }

    function renderDetails() {
      const spinner = spinners[selectedName];
      if (!spinner) {
        detailsContent.replaceChildren();
        detailsPanel.hidden = true;
        copyCurrent.disabled = true;
        return;
      }

      detailsPanel.hidden = false;
      copyCurrent.disabled = false;
      const tagMarkup = spinner.tags.map((tag) => {
        return `<span class="tag">${tag}</span>`;
      }).join('');
      detailsContent.innerHTML = `
        <div class="detail-frame" id="detailFrame" aria-hidden="true">${spinner.preview_frame}</div>
        <h2>${selectedName}</h2>
        <div class="tags">${tagMarkup}</div>
        <div class="detail-list">
          <div>category: ${spinner.category}</div>
          <div>use: ${spinner.description}</div>
          <div>frames: ${spinner.frame_count}</div>
          <div>interval: ${spinner.interval_ms}ms</div>
          <div>width: ${spinner.frame_width}</div>
          <div>motion: ${spinner.motion}</div>
        </div>
        <pre class="snippet"><code>${spinnerSnippet(selectedName)}</code></pre>
      `;
      frameEls.__detail = document.getElementById('detailFrame');
    }

    function startAnimation() {
      const byInterval = {};
      Object.entries(spinners).forEach(([name, spinner]) => {
        if (!byInterval[spinner.interval_ms]) byInterval[spinner.interval_ms] = [];
        byInterval[spinner.interval_ms].push({ name, frames: spinner.frames, i: 0 });
      });

      Object.entries(byInterval).forEach(([interval, group]) => {
        window.setInterval(() => {
          if (reducedMotion) return;
          group.forEach((entry) => {
            entry.i = (entry.i + 1) % entry.frames.length;
            if (frameEls[entry.name]) frameEls[entry.name].textContent = entry.frames[entry.i];
            if (entry.name === selectedName && frameEls.__detail) {
              frameEls.__detail.textContent = entry.frames[entry.i];
            }
          });
        }, Number(interval));
      });
    }

    async function init() {
      initializePreferences();
      const response = await fetch('/spinners.json');
      spinners = await response.json();
      selectedName = Object.keys(spinners)[0] || '';
      renderChips();
      renderGallery();
      startAnimation();
    }

    searchInput.addEventListener('input', renderGallery);
    motionToggle.addEventListener('click', () => {
      const nextValue = !reducedMotion;
      setReducedMotion(nextValue);
      window.localStorage.setItem(motionPreferenceKey, nextValue ? 'reduce' : 'full');
    });
    copyCurrent.addEventListener('click', async () => {
      copyStatus.textContent = '';
      await copyText(spinnerSnippet(selectedName));
      copyCurrent.textContent = 'Copied';
      copyStatus.textContent = `${selectedName} snippet copied.`;
      window.setTimeout(() => { copyCurrent.textContent = 'Copy snippet'; }, 1000);
    });

    themeToggle.addEventListener('click', () => {
      const dark = document.documentElement.dataset.theme === 'dark';
      const nextTheme = dark ? 'light' : 'dark';
      setTheme(nextTheme);
      window.localStorage.setItem(themePreferenceKey, nextTheme);
    });

    init();
  </script>
</body>
</html>
"""


def build_spinner_payload() -> dict[str, SpinnerPayload]:
    """Return JSON-friendly spinner data for the web preview."""
    payload: dict[str, SpinnerPayload] = {}
    for name in SPINNER_NAMES:
        metadata = metadata_for_spinner(name)
        payload[name] = {
            "frames": list(spinners[name].frames),
            "interval": metadata.interval_ms,
            "interval_ms": metadata.interval_ms,
            "category": metadata.category,
            "tags": list(metadata.tags),
            "frame_count": metadata.frame_count,
            "frame_width": metadata.frame_width,
            "preview_frame": metadata.preview_frame,
            "motion": metadata.motion,
            "description": metadata.description,
        }
    return payload


def build_demo_html() -> str:
    """Return demo HTML that loads spinner data from /spinners.json."""
    return DEMO_HTML_TEMPLATE.replace("__CATALOG_COUNT__", str(len(SPINNER_NAMES))).replace(
        "__CATEGORY_NAMES__", json.dumps(CATEGORY_NAMES)
    )


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
    bound_host, bound_port = cast(tuple[str, int], server.server_address)
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


def _port_number(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer between 0 and 65535") from exc
    if not 0 <= port <= 65_535:
        raise argparse.ArgumentTypeError("port must be an integer between 0 and 65535")
    return port


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unicode-animatio-web",
        description="Run a local browser demo for unicode_animations.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=_port_number, default=0, help="Port to bind (default: auto)")
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
