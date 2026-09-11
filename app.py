"""
Ask Me Anything (AMA) — Flask backend (Clean White Background & Hover Effects without Flower Animation)
"""

import os
import html
import logging

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7882277298:AAHCKsrRVV4677FtMgxCqIO3XUftpjuvc8Y")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6915043499")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

MAX_MESSAGE_LENGTH = 500
MAX_NAME_LENGTH = 60

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ask Me Anything</title>
  <meta name="description" content="Send a question — anonymously if you like.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #ffffff;
      --panel: #ffffff;
      --panel-border: #e2d4f2;
      --input-bg: #faf7ff;
      --ink: #2d233d;
      --ink-muted: #796b8c;
      --accent: #9b51e0;
      --accent-deep: #7b2cbf;
      --error: #e25a5a;
      --success: #27ae60;
      --radius-panel: 28px;
      --radius-input: 10px;
      --radius-btn: 12px;
      --font-display: 'Fraunces', Georgia, serif;
      --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-body);
      color: var(--ink);
      background: var(--bg);
      min-height: 100vh;
      position: relative;
    }

    .page {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: clamp(1rem, 4vw, 3rem);
    }
    .panel {
      width: 100%;
      max-width: 440px;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-panel);
      padding: clamp(1.75rem, 5vw, 2.75rem);
      text-align: left;
      box-shadow: 0 20px 45px -15px rgba(155, 81, 224, 0.15);
      animation: rise 0.5s ease both;
      transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    
    /* 🌟 Panel Hover Effect */
    .panel:hover {
      transform: translateY(-4px);
      border-color: rgba(155, 81, 224, 0.5);
      box-shadow: 0 25px 50px -12px rgba(155, 81, 224, 0.25);
    }

    @keyframes rise {
      from { opacity: 0; transform: translateY(14px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .panel__icon {
      width: 30px; height: 30px; color: var(--accent); margin-bottom: 1.1rem;
      transition: transform 0.3s ease;
    }
    .panel:hover .panel__icon {
      transform: scale(1.1) rotate(10deg);
    }
    .panel__title {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: clamp(1.6rem, 4.5vw, 2.1rem);
      line-height: 1.15;
      margin: 0 0 0.5rem;
      color: var(--ink);
    }
    .panel__subtitle {
      font-family: var(--font-display);
      font-style: italic;
      font-weight: 500;
      font-size: clamp(0.95rem, 2vw, 1.05rem);
      color: var(--ink-muted);
      margin: 0 0 1.75rem;
      max-width: 34ch;
    }
    .field { margin-bottom: 1.35rem; }
    .field label {
      display: block; font-weight: 600; font-size: 0.85rem; color: var(--ink); margin-bottom: 0.45rem;
    }
    .field__hint { font-weight: 400; color: var(--ink-muted); font-size: 0.8em; margin-left: 0.3em; }
    
    input[type="text"], textarea {
      width: 100%;
      background: var(--input-bg);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-input);
      padding: 0.7rem 0.85rem;
      font-family: var(--font-body);
      font-size: 1rem;
      color: var(--ink);
      transition: all 0.25s ease;
      resize: vertical;
    }
    
    /* 🌟 Input & Textarea Hover Effect */
    input[type="text"]:hover, textarea:hover {
      border-color: rgba(155, 81, 224, 0.5);
      background: #ffffff;
    }
    input[type="text"]:focus, textarea:focus {
      outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(155, 81, 224, 0.2);
      background: #ffffff;
    }
    .char-count { text-align: right; font-size: 0.75rem; color: var(--ink-muted); margin-top: 0.35rem; font-variant-numeric: tabular-nums; }
    
    .submit-btn {
      width: 100%; border: none; border-radius: var(--radius-btn);
      padding: 0.85rem 1.5rem; font-family: var(--font-body); font-size: 1rem; font-weight: 600;
      color: #ffffff; background: linear-gradient(180deg, var(--accent), var(--accent-deep));
      cursor: pointer; transition: all 0.25s ease;
      box-shadow: 0 10px 20px -8px rgba(155, 81, 224, 0.6);
    }
    
    /* 🌟 Button Hover & Active Effect */
    .submit-btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 14px 24px -6px rgba(155, 81, 224, 0.8);
      filter: brightness(1.08);
    }
    .submit-btn:active:not(:disabled) {
      transform: translateY(1px);
    }

    .submit-btn:disabled { cursor: not-allowed; opacity: 0.85; transform: none; }
    .submit-btn.is-success { background: linear-gradient(180deg, var(--success), #219653); box-shadow: 0 10px 20px -8px rgba(39, 174, 96, 0.6); }
    .btn-content { display: inline-flex; align-items: center; justify-content: center; gap: 0.55rem; }
    .spinner {
      width: 15px; height: 15px; border: 2px solid rgba(255, 255, 255, 0.35);
      border-top-color: #ffffff; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .check-icon { width: 16px; height: 16px; flex-shrink: 0; }
    .form-status { min-height: 1.2rem; font-size: 0.85rem; color: var(--ink-muted); margin: 0.9rem 0 0; }
    .form-status.is-error { color: var(--error); }
    .form-status.is-success { color: var(--success); }
    @media (max-width: 420px) {
      .page { padding: 0; }
      .panel { min-height: 100vh; border-radius: 0; border: none; box-shadow: none; display: flex; flex-direction: column; justify-content: center; }
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="panel">
      <svg class="panel__icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect x="4" y="10" width="40" height="28" rx="4" stroke="currentColor" stroke-width="2" />
        <path d="M6 13L24 27L42 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <h1 class="panel__title">Ask me anything</h1>
      <p class="panel__subtitle">Questions land straight in my inbox — no names required.</p>
      <form id="ama-form" novalidate>
        <div class="field">
          <label for="name">Name <span class="field__hint">optional</span></label>
          <input type="text" id="name" name="name" placeholder="Anonymous" autocomplete="name" maxlength="60">
        </div>
        <div class="field">
          <label for="message">Your question</label>
          <textarea id="message" name="message" rows="4" placeholder="What do you want to know?" required maxlength="500"></textarea>
          <div class="char-count"><span id="char-count">0</span>/500</div>
        </div>
        <button type="submit" id="submit-btn" class="submit-btn">
          <span class="btn-content"><span class="btn-text">Send question</span></span>
        </button>
        <p id="form-status" class="form-status" role="status" aria-live="polite"></p>
      </form>
    </section>
  </main>
  <script>
    const form = document.getElementById('ama-form');
    const nameInput = document.getElementById('name');
    const messageInput = document.getElementById('message');
    const charCount = document.getElementById('char-count');
    const submitBtn = document.getElementById('submit-btn');
    const btnContent = submitBtn.querySelector('.btn-content');
    const formStatus = document.getElementById('form-status');
    const ORIGINAL_BTN_HTML = btnContent.innerHTML;
    const CHECK_ICON = `<svg class="check-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

    messageInput.addEventListener('input', () => { charCount.textContent = messageInput.value.length; });
    function setStatus(message, type) {
      formStatus.textContent = message;
      formStatus.classList.remove('is-error', 'is-success');
      if (type) { formStatus.classList.add(`is-${type}`); }
    }
    function setLoading() {
      submitBtn.disabled = true;
      submitBtn.classList.remove('is-success');
      btnContent.innerHTML = '<span class="spinner" aria-hidden="true"></span><span class="btn-text">Sending…</span>';
      setStatus('', null);
    }
    function setSuccess() {
      submitBtn.classList.add('is-success');
      btnContent.innerHTML = `${CHECK_ICON}<span class="btn-text">Sent</span>`;
      setStatus('Your question is on its way and I will answer in a note . Thank you!', 'success');
    }
    function setError(message) {
      submitBtn.disabled = false;
      submitBtn.classList.remove('is-success');
      btnContent.innerHTML = ORIGINAL_BTN_HTML;
      setStatus(message || 'Something went wrong. Please try again.', 'error');
    }
    function resetButton() {
      submitBtn.disabled = false;
      submitBtn.classList.remove('is-success');
      btnContent.innerHTML = ORIGINAL_BTN_HTML;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = messageInput.value.trim();
      if (!message) { setError('Please write a question before sending.'); messageInput.focus(); return; }
      const name = nameInput.value.trim() || 'Anonymous';
      setLoading();
      try {
        const response = await fetch('/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, message }),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success) { throw new Error(data.error || 'Failed to send your question.'); }
        setSuccess();
        setTimeout(() => {
          form.reset();
          charCount.textContent = '0';
          resetButton();
          setStatus('', null);
          nameInput.focus();
        }, 2200);
      } catch (err) { setError(err.message); }
    });
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return HTML_PAGE


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()[:MAX_NAME_LENGTH] or "Anonymous"
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"success": False, "error": "Message cannot be empty."}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "success": False,
            "error": f"Message is too long (max {MAX_MESSAGE_LENGTH} characters).",
        }), 400

    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID":
        app.logger.warning("Telegram credentials are still placeholders.")
        return jsonify({
            "success": False,
            "error": "Server is missing Telegram credentials.",
        }), 500

    safe_name = html.escape(name)
    safe_message = html.escape(message)

    telegram_text = (
        "📥 <b>New Question Received!</b>\n"
        f"👤 <b>From:</b> {safe_name}\n"
        f"💬 <b>Message:</b> {safe_message}"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": telegram_text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        app.logger.error("Telegram API error: %s", exc)
        return jsonify({
            "success": False,
            "error": "Could not deliver the message to Telegram. Please try again shortly.",
        }), 502

    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
