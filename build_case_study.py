"""Builds a self-contained, interactive index.html case study."""

import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "out" / "all_100.json"
VERIFIED_STRESS_PATH = Path(__file__).resolve().parent / "out" / "verified_stress_test.json"
OUT_HTML_PATH = Path(__file__).resolve().parent / "index.html"

def main():
    data = json.loads(DATA_PATH.read_text())
    verified_stress = json.loads(VERIFIED_STRESS_PATH.read_text()) if VERIFIED_STRESS_PATH.exists() else []

    data_json = json.dumps(data)
    stress_json = json.dumps(verified_stress)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Composio App Research: 100 Apps Evaluated by AI Agent</title>
  <meta name="description" content="A comprehensive research case study evaluating 100 enterprise and developer platforms for Composio agent toolkit buildability, auth mix, multi-tenant gating, and MCP ecosystem support." />
  
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />

  <style>
    :root {{
      --bg-base: #0a0d14;
      --bg-surface: #111622;
      --bg-surface-elevated: #182030;
      --bg-card: rgba(24, 32, 48, 0.7);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(99, 102, 241, 0.4);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --accent-primary: #6366f1;
      --accent-primary-hover: #4f46e5;
      --accent-secondary: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-purple: #a855f7;

      --badge-green-bg: rgba(16, 185, 129, 0.15);
      --badge-green-text: #34d399;
      --badge-green-border: rgba(16, 185, 129, 0.3);

      --badge-yellow-bg: rgba(245, 158, 11, 0.15);
      --badge-yellow-text: #fbbf24;
      --badge-yellow-border: rgba(245, 158, 11, 0.3);

      --badge-red-bg: rgba(244, 63, 94, 0.15);
      --badge-red-text: #fb7185;
      --badge-red-border: rgba(244, 63, 94, 0.3);

      --badge-blue-bg: rgba(99, 102, 241, 0.15);
      --badge-blue-text: #818cf8;
      --badge-blue-border: rgba(99, 102, 241, 0.3);

      --badge-purple-bg: rgba(168, 85, 247, 0.15);
      --badge-purple-text: #c084fc;
      --badge-purple-border: rgba(168, 85, 247, 0.3);

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --shadow-subtle: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
      --shadow-glow: 0 0 30px -5px rgba(99, 102, 241, 0.2);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}

    a {{
      color: var(--accent-secondary);
      text-decoration: none;
      transition: color 0.15s ease;
    }}

    a:hover {{
      color: #38bdf8;
      text-decoration: underline;
    }}

    /* Container */
    .container {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Glow backdrop */
    .glow-bg {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 1000px;
      height: 400px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(6, 182, 212, 0.05) 50%, rgba(10, 13, 20, 0) 70%);
      pointer-events: none;
      z-index: 0;
    }}

    /* Header */
    header {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(10, 13, 20, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 0;
    }}

    .nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .logo-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, #6366f1, #06b6d4);
      color: white;
      font-weight: 800;
      font-size: 14px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
    }}

    .brand-title {{
      font-size: 16px;
      font-weight: 600;
      color: var(--text-primary);
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .nav-link {{
      color: var(--text-secondary);
      font-size: 14px;
      font-weight: 500;
      transition: color 0.15s ease;
    }}

    .nav-link:hover {{
      color: var(--text-primary);
      text-decoration: none;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      border: 1px solid transparent;
    }}

    .btn-primary {{
      background: var(--accent-primary);
      color: white;
    }}

    .btn-primary:hover {{
      background: var(--accent-primary-hover);
      text-decoration: none;
      box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
    }}

    .btn-outline {{
      background: rgba(255, 255, 255, 0.04);
      border-color: var(--border-subtle);
      color: var(--text-primary);
    }}

    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      text-decoration: none;
    }}

    /* Hero Section */
    .hero {{
      position: relative;
      padding: 56px 0 40px;
      text-align: center;
    }}

    .hero-tag {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(99, 102, 241, 0.1);
      border: 1px solid var(--border-focus);
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      color: #a5b4fc;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }}

    .hero-tag .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }}

    .hero h1 {{
      font-size: 42px;
      font-weight: 800;
      letter-spacing: -1px;
      line-height: 1.15;
      margin-bottom: 16px;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero p {{
      font-size: 17px;
      color: var(--text-secondary);
      max-width: 820px;
      margin: 0 auto 36px;
      line-height: 1.6;
    }}

    /* Stat Cards Bar */
    .stat-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 48px;
    }}

    .stat-card {{
      background: var(--bg-card);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      text-align: left;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .stat-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.18);
    }}

    .stat-card::after {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--accent-gradient, linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)));
    }}

    .stat-value {{
      font-size: 32px;
      font-weight: 800;
      color: var(--text-primary);
      font-feature-settings: "tnum";
      margin-bottom: 4px;
      display: flex;
      align-items: baseline;
      gap: 6px;
    }}

    .stat-unit {{
      font-size: 16px;
      font-weight: 500;
      color: var(--text-muted);
    }}

    .stat-label {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
      margin-bottom: 2px;
    }}

    .stat-desc {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    /* Section Wrapper */
    .section-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 32px;
      margin-bottom: 40px;
      box-shadow: var(--shadow-subtle);
    }}

    .section-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .section-title {{
      font-size: 22px;
      font-weight: 700;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-subtitle {{
      font-size: 14px;
      color: var(--text-secondary);
      margin-top: 4px;
    }}

    /* Headline Patterns Grid */
    .patterns-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 28px;
    }}

    .pattern-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .pattern-card-title {{
      font-size: 15px;
      font-weight: 700;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .progress-bar-group {{
      margin-bottom: 12px;
    }}

    .progress-labels {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-secondary);
      margin-bottom: 6px;
      font-weight: 500;
    }}

    .progress-track {{
      height: 8px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 4px;
      overflow: hidden;
      display: flex;
    }}

    .progress-segment {{
      height: 100%;
      transition: width 0.3s ease;
    }}

    .pattern-takeaway {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.5;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .pattern-takeaway strong {{
      color: var(--text-primary);
    }}

    /* Key Insights Box */
    .insights-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}

    .insight-card {{
      background: rgba(99, 102, 241, 0.04);
      border: 1px solid rgba(99, 102, 241, 0.15);
      border-radius: var(--radius-md);
      padding: 18px;
    }}

    .insight-card h4 {{
      font-size: 14px;
      font-weight: 700;
      color: #c7d2fe;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .insight-card p {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.5;
    }}

    /* Table Toolbar */
    .toolbar {{
      display: flex;
      gap: 12px;
      margin-bottom: 20px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .search-box {{
      flex: 1;
      min-width: 240px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px 14px 10px 36px;
      font-size: 13px;
      color: var(--text-primary);
      font-family: inherit;
      outline: none;
      transition: border-color 0.15s ease;
    }}

    .search-input:focus {{
      border-color: var(--accent-primary);
    }}

    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
      pointer-events: none;
    }}

    .filter-select {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      font-size: 13px;
      color: var(--text-primary);
      font-family: inherit;
      outline: none;
      cursor: pointer;
    }}

    .filter-select:focus {{
      border-color: var(--accent-primary);
    }}

    .results-count {{
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 500;
      margin-left: auto;
    }}

    /* Matrix Table */
    .table-container {{
      overflow-x: auto;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      background: var(--bg-surface-elevated);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    th {{
      background: rgba(17, 22, 34, 0.95);
      color: var(--text-secondary);
      font-weight: 600;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 10;
      user-select: none;
      cursor: pointer;
    }}

    th:hover {{
      color: var(--text-primary);
    }}

    td {{
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-secondary);
      vertical-align: middle;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    .app-name-cell {{
      font-weight: 600;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .app-category-badge {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
      display: block;
      margin-top: 2px;
    }}

    /* Badges */
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
      border: 1px solid transparent;
      letter-spacing: 0.2px;
    }}

    .badge-buildable-now {{
      background: var(--badge-green-bg);
      color: var(--badge-green-text);
      border-color: var(--badge-green-border);
    }}

    .badge-friction {{
      background: var(--badge-yellow-bg);
      color: var(--badge-yellow-text);
      border-color: var(--badge-yellow-border);
    }}

    .badge-blocked {{
      background: var(--badge-red-bg);
      color: var(--badge-red-text);
      border-color: var(--badge-red-border);
    }}

    .badge-oauth {{
      background: var(--badge-blue-bg);
      color: var(--badge-blue-text);
      border-color: var(--badge-blue-border);
    }}

    .badge-apikey {{
      background: var(--badge-purple-bg);
      color: var(--badge-purple-text);
      border-color: var(--badge-purple-border);
    }}

    .badge-mcp-official {{
      background: rgba(6, 182, 212, 0.15);
      color: #38bdf8;
      border-color: rgba(6, 182, 212, 0.3);
    }}

    .badge-mcp-community {{
      background: rgba(148, 163, 184, 0.15);
      color: #cbd5e1;
      border-color: rgba(148, 163, 184, 0.25);
    }}

    .badge-mcp-no {{
      background: rgba(100, 116, 139, 0.1);
      color: #94a3b8;
    }}

    .confidence-meter {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--text-primary);
    }}

    .confidence-bar-bg {{
      width: 44px;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
      overflow: hidden;
    }}

    .confidence-bar-fill {{
      height: 100%;
      background: var(--accent-emerald);
    }}

    .details-btn {{
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .details-btn:hover {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-primary);
      border-color: rgba(255, 255, 255, 0.2);
    }}

    /* Agent Architecture Section */
    .arch-diagram {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
      position: relative;
    }}

    .arch-step {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      position: relative;
    }}

    .step-num {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--accent-primary);
      color: white;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 12px;
    }}

    .step-title {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 6px;
    }}

    .step-desc {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.5;
    }}

    .code-pill {{
      display: inline-block;
      background: rgba(0, 0, 0, 0.4);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #93c5fd;
      border: 1px solid rgba(255, 255, 255, 0.05);
      margin-top: 6px;
    }}

    .human-agent-split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 20px;
    }}

    @media (max-width: 768px) {{
      .human-agent-split {{
        grid-template-columns: 1fr;
      }}
    }}

    .split-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
    }}

    .split-card.agent-card {{
      border-left: 4px solid var(--accent-secondary);
    }}

    .split-card.human-card {{
      border-left: 4px solid var(--accent-amber);
    }}

    .split-title {{
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .split-list {{
      list-style: none;
    }}

    .split-list li {{
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 8px;
      position: relative;
      padding-left: 18px;
      line-height: 1.5;
    }}

    .split-list li::before {{
      content: '✓';
      position: absolute;
      left: 0;
      color: var(--accent-emerald);
      font-weight: bold;
    }}

    .split-card.human-card .split-list li::before {{
      content: '★';
      color: var(--accent-amber);
    }}

    /* Verification Honesty Section */
    .honesty-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 16px;
    }}

    .honesty-table th {{
      background: var(--bg-surface-elevated);
      padding: 10px 14px;
    }}

    .honesty-table td {{
      padding: 12px 14px;
      background: rgba(255, 255, 255, 0.01);
    }}

    /* Modal / Drawer */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      max-width: 680px;
      width: 100%;
      padding: 28px;
      box-shadow: var(--shadow-subtle), var(--shadow-glow);
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
    }}

    .modal-close {{
      position: absolute;
      top: 20px;
      right: 20px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
    }}

    .modal-close:hover {{
      color: var(--text-primary);
    }}

    .modal-header {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .modal-app-name {{
      font-size: 24px;
      font-weight: 800;
      color: var(--text-primary);
    }}

    .modal-row {{
      margin-bottom: 14px;
    }}

    .modal-row-label {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }}

    .modal-row-content {{
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.5;
    }}

    /* Code Block */
    pre.code-snippet {{
      background: #05070a;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 16px;
      overflow-x: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: #38bdf8;
      margin-top: 12px;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border-subtle);
      padding: 40px 0 60px;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
    }}

    .footer-links {{
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-top: 12px;
    }}
  </style>
</head>
<body>
  <div class="glow-bg"></div>

  <!-- Header -->
  <header>
    <div class="container nav-inner">
      <div class="logo-group">
        <span class="logo-badge">COMPOSIO</span>
        <span class="brand-title">App Research Pipeline Case Study</span>
      </div>
      <div class="nav-links">
        <a href="#patterns" class="nav-link">Findings & Patterns</a>
        <a href="#matrix" class="nav-link">100-App Matrix</a>
        <a href="#architecture" class="nav-link">Agent Architecture</a>
        <a href="#verification" class="nav-link">Verification</a>
        <a href="https://github.com/krbok/Composio" target="_blank" class="btn btn-outline">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          GitHub Repo
        </a>
      </div>
    </div>
  </header>

  <main class="container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-tag">
        <span class="dot"></span> 100 Apps Researched &bull; Verified Agent Loop
      </div>
      <h1>Can It Be a Composio Agent Toolkit?</h1>
      <p>
        Evaluating 100 top enterprise and developer platforms across 10 categories for auth mechanics, multi-tenant gating, API surfaces, and first-party Model Context Protocol (MCP) support. Built using Claude Agent SDK and Composio's free search tools.
      </p>

      <!-- Stat Cards -->
      <div class="stat-grid">
        <div class="stat-card" style="--accent-gradient: linear-gradient(90deg, #10b981, #06b6d4)">
          <div class="stat-value">65<span class="stat-unit">%</span></div>
          <div class="stat-label">Buildable Immediately</div>
          <div class="stat-desc">Self-serve multi-tenant OAuth/API key</div>
        </div>

        <div class="stat-card" style="--accent-gradient: linear-gradient(90deg, #6366f1, #a855f7)">
          <div class="stat-value">66<span class="stat-unit">%</span></div>
          <div class="stat-label">OAuth2 Dominance</div>
          <div class="stat-desc">Standard multi-tenant authorization code</div>
        </div>

        <div class="stat-card" style="--accent-gradient: linear-gradient(90deg, #06b6d4, #3b82f6)">
          <div class="stat-value">73<span class="stat-unit">%</span></div>
          <div class="stat-label">Official MCP Support</div>
          <div class="stat-desc">First-party server or remote endpoint</div>
        </div>

        <div class="stat-card" style="--accent-gradient: linear-gradient(90deg, #f59e0b, #f43f5e)">
          <div class="stat-value">32<span class="stat-unit">%</span></div>
          <div class="stat-label">Gated with Friction</div>
          <div class="stat-desc">Admin review, partner approval, paid plan</div>
        </div>

        <div class="stat-card" style="--accent-gradient: linear-gradient(90deg, #f43f5e, #94a3b8)">
          <div class="stat-value">3<span class="stat-unit">%</span></div>
          <div class="stat-label">Strictly Blocked</div>
          <div class="stat-desc">Salesforce B2C, Ahrefs Connect, Sherlock CLI</div>
        </div>
      </div>
    </section>

    <!-- Findings & Patterns Section -->
    <section id="patterns" class="section-box">
      <div class="section-header">
        <div>
          <h2 class="section-title">Headline Patterns & Macro Insights</h2>
          <p class="section-subtitle">Key architectural takeaways from clustering 100 enterprise and developer platforms.</p>
        </div>
      </div>

      <div class="patterns-grid">
        <!-- Auth Mix Pattern -->
        <div class="pattern-card">
          <div class="pattern-card-title">
            <span>🔑 Authentication Protocol Mix</span>
          </div>
          <div class="progress-bar-group">
            <div class="progress-labels">
              <span>OAuth2 (66%)</span>
              <span>API Key (28%)</span>
              <span>Basic/Other (6%)</span>
            </div>
            <div class="progress-track">
              <div class="progress-segment" style="width: 66%; background: var(--accent-primary);"></div>
              <div class="progress-segment" style="width: 28%; background: var(--accent-purple);"></div>
              <div class="progress-segment" style="width: 6%; background: var(--text-muted);"></div>
            </div>
          </div>
          <div class="pattern-takeaway">
            <strong>The Takeaway:</strong> OAuth 2.0 is the undisputed standard for multi-tenant SaaS. API keys dominate developer infra, data scraping, and specialized fintech/AI protocols.
          </div>
        </div>

        <!-- Self-Serve vs Gating Pattern -->
        <div class="pattern-card">
          <div class="pattern-card-title">
            <span>🚪 Developer Gating Landscape</span>
          </div>
          <div class="progress-bar-group">
            <div class="progress-labels">
              <span>Self-Serve (65%)</span>
              <span>Admin Review (16%)</span>
              <span>Partner/Paid (19%)</span>
            </div>
            <div class="progress-track">
              <div class="progress-segment" style="width: 65%; background: var(--accent-emerald);"></div>
              <div class="progress-segment" style="width: 16%; background: var(--accent-amber);"></div>
              <div class="progress-segment" style="width: 19%; background: var(--accent-rose);"></div>
            </div>
          </div>
          <div class="pattern-takeaway">
            <strong>The Takeaway:</strong> While 65% are frictionless self-serve, 35% enforce human checkpoints (e.g. app review, marketplace listing, or enterprise subscriptions) before multi-tenant distribution.
          </div>
        </div>

        <!-- MCP Ecosystem Pattern -->
        <div class="pattern-card">
          <div class="pattern-card-title">
            <span>⚡ MCP Ecosystem Readiness</span>
          </div>
          <div class="progress-bar-group">
            <div class="progress-labels">
              <span>Official MCP (73%)</span>
              <span>Community MCP (24%)</span>
              <span>No MCP (3%)</span>
            </div>
            <div class="progress-track">
              <div class="progress-segment" style="width: 73%; background: var(--accent-secondary);"></div>
              <div class="progress-segment" style="width: 24%; background: #94a3b8;"></div>
              <div class="progress-segment" style="width: 3%; background: rgba(255,255,255,0.1);"></div>
            </div>
          </div>
          <div class="pattern-takeaway">
            <strong>The Takeaway:</strong> Over 70% of platforms now publish first-party MCP servers (HubSpot, Stripe, Brex, Ramp, Xero, Smartsheet, Consensus, Devin), establishing MCP as a primary agent interface.
          </div>
        </div>
      </div>

      <!-- Deep Dive Insights -->
      <div class="insights-strip">
        <div class="insight-card">
          <h4>1. The "Personal App" Illusion</h4>
          <p>
            Many platforms (e.g., Zendesk, Close, Copper, Pipedrive) let single developers spin up private OAuth apps instantly, but building a <em>multi-tenant toolkit</em> (where arbitrary third-party users authorize their own accounts) requires global client conversion, marketplace review, or partner agreements.
          </p>
        </div>

        <div class="insight-card">
          <h4>2. Category Polarization</h4>
          <p>
            <strong>Developer Infra</strong> (Vercel, Supabase, Cloudflare) and <strong>Productivity</strong> (Notion, Linear, Harvest) are >85% frictionless self-serve. In contrast, <strong>Marketing/Ads</strong> (Meta, Google, LinkedIn) and <strong>Enterprise ERP/CRM</strong> require rigorous app verification and business checks.
          </p>
        </div>

        <div class="insight-card">
          <h4>3. The 3 Hard Blockers</h4>
          <p>
            Only 3 apps are strictly blocked: <em>Salesforce Commerce Cloud</em> (closed on-demand sandboxes requiring commercial contracts), <em>Ahrefs Connect</em> (strictly mandates an Enterprise tier + sales review for OAuth), and <em>Sherlock</em> (open-source local CLI with no hosted service).
          </p>
        </div>
      </div>
    </section>

    <!-- Interactive 100-App Matrix Table -->
    <section id="matrix" class="section-box">
      <div class="section-header">
        <div>
          <h2 class="section-title">The 100-App Buildability Matrix</h2>
          <p class="section-subtitle">Complete, filterable findings researched and validated across all 10 categories.</p>
        </div>
        <button id="exportJsonBtn" class="btn btn-outline">Export JSON</button>
      </div>

      <!-- Filter Toolbar -->
      <div class="toolbar">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Search app, category, one-liner, or blocker..." />
        </div>

        <select id="categoryFilter" class="filter-select">
          <option value="">All Categories (10)</option>
          <option value="CRM and Sales">1. CRM & Sales</option>
          <option value="Support and Helpdesk">2. Support & Helpdesk</option>
          <option value="Communications and Messaging">3. Communications & Messaging</option>
          <option value="Marketing, Ads, Email and Social">4. Marketing & Ads</option>
          <option value="Ecommerce">5. Ecommerce</option>
          <option value="Data, SEO and Scraping">6. Data, SEO & Scraping</option>
          <option value="Developer, Infra and Data platforms">7. Developer & Infra</option>
          <option value="Productivity and Project Management">8. Productivity & PM</option>
          <option value="Finance and Fintech">9. Finance & Fintech</option>
          <option value="AI, Research and Media-native">10. AI & Media-native</option>
        </select>

        <select id="buildFilter" class="filter-select">
          <option value="">All Buildability</option>
          <option value="buildable-now">Buildable Now (65)</option>
          <option value="buildable-with-friction">With Friction (32)</option>
          <option value="blocked">Blocked (3)</option>
        </select>

        <select id="authFilter" class="filter-select">
          <option value="">All Auth Methods</option>
          <option value="OAuth2">OAuth2</option>
          <option value="API key">API Key</option>
          <option value="Basic">Basic</option>
          <option value="other">Other / CLI</option>
        </select>

        <select id="mcpFilter" class="filter-select">
          <option value="">All MCP Status</option>
          <option value="yes-official">Official MCP</option>
          <option value="yes-community">Community MCP</option>
          <option value="no">No MCP</option>
        </select>

        <span id="resultsCounter" class="results-count">Showing 100 of 100 apps</span>
      </div>

      <!-- Matrix Table -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th onclick="sortTable('app')"># / App ⬍</th>
              <th onclick="sortTable('category')">Category ⬍</th>
              <th onclick="sortTable('auth_method')">Auth ⬍</th>
              <th onclick="sortTable('self_serve_status')">Gating ⬍</th>
              <th onclick="sortTable('api_surface')">Surface ⬍</th>
              <th onclick="sortTable('has_mcp')">MCP ⬍</th>
              <th onclick="sortTable('buildability')">Buildability ⬍</th>
              <th onclick="sortTable('confidence')">Confidence ⬍</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="matrixTableBody">
            <!-- Rows injected by JavaScript -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- Agent Architecture & Process Section -->
    <section id="architecture" class="section-box">
      <div class="section-header">
        <div>
          <h2 class="section-title">Agent Architecture & Isolation</h2>
          <p class="section-subtitle">How Claude Agent SDK was orchestrated with Composio search tools and Pydantic validation.</p>
        </div>
      </div>

      <div class="arch-diagram">
        <div class="arch-step">
          <div class="step-num">1</div>
          <div class="step-title">Autonomous Search Loop</div>
          <div class="step-desc">
            Equipped Claude with free, unauthenticated Composio tools (<span class="code-pill">COMPOSIO_SEARCH_WEB</span> & <span class="code-pill">FETCH_URL_CONTENT</span>) to find and parse official documentation.
          </div>
        </div>

        <div class="arch-step">
          <div class="step-num">2</div>
          <div class="step-title">Multi-Tenant Evaluation</div>
          <div class="step-desc">
            Enforced strict judging criteria targeting multi-tenant distribution rather than private developer access. Mandatory dedicated searches for official/community MCP servers.
          </div>
        </div>

        <div class="arch-step">
          <div class="step-num">3</div>
          <div class="step-title">Pydantic Tool Boundary</div>
          <div class="step-desc">
            Turn completed by invoking <span class="code-pill">submit_finding</span>. Enums and URL schemas validated directly at the tool-call boundary; invalid values trigger immediate re-prompting.
          </div>
        </div>

        <div class="arch-step">
          <div class="step-num">4</div>
          <div class="step-title">Dual-Signal Verification</div>
          <div class="step-desc">
            Output cross-checked against Composio's real catalog (<span class="code-pill">composio.toolkits.get</span>) and an independent secondary WebSearch/WebFetch pass to detect non-determinism.
          </div>
        </div>
      </div>

      <div class="human-agent-split">
        <div class="split-card agent-card">
          <div class="split-title">
            <span>🤖 What the Agent Handled Autonomously</span>
          </div>
          <ul class="split-list">
            <li>Parsed 100+ complex developer portals, auth guides, and API schemas.</li>
            <li>Identified obscure multi-tenant gating policies (e.g., Zendesk Global OAuth client review requirements).</li>
            <li>Discovered active first-party MCP servers (73% of sample) from newly published 2024-2026 endpoints.</li>
            <li>Extracted direct documentation evidence URLs actually fetched during execution.</li>
          </ul>
        </div>

        <div class="split-card human-card">
          <div class="split-title">
            <span>👤 Where Human Engineering Was Needed</span>
          </div>
          <ul class="split-list">
            <li><strong>Tool Sandboxing & Isolation:</strong> Claude CLI subprocess was stripping environmental API keys to prevent unintended metered billing and bypass ambient tool leakage.</li>
            <li><strong>Multi-tenant Definition Guardrails:</strong> System prompt required refinement to stop agents from rounding up "private personal API key" paths to "self-serve multi-tenant".</li>
            <li><strong>Reconciliation of Catalog Disagreements:</strong> Diagnosed why 6 apps differed from Composio's legacy API-key catalog entries.</li>
            <li><strong>Resumable Pipeline Architecture:</strong> Implemented incremental disk flushing to recover gracefully from rate limits without data loss.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Verification & Accuracy Honesty Section -->
    <section id="verification" class="section-box">
      <div class="section-header">
        <div>
          <h2 class="section-title">Verification Honesty & Catalog Cross-Check</h2>
          <p class="section-subtitle">Transparent accounting of hits, misses, and catalog discrepancies.</p>
        </div>
      </div>

      <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">
        To ensure high empirical accuracy, we cross-checked the agent's findings against Composio's deterministic catalog (<span class="code-pill">composio.toolkits.get</span>) and performed secondary browser/search passes. Out of 50 matched toolkits, 44 agreed immediately. The 6 disagreements revealed an important truth:
      </p>

      <div class="table-container">
        <table class="honesty-table">
          <thead>
            <tr>
              <th>App</th>
              <th>Agent Finding</th>
              <th>Composio Catalog</th>
              <th>Root Cause & Accuracy Verdict</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Close CRM</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (admin-approval)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Agent is more accurate for multi-tenancy.</strong> Composio uses single-user API keys. True multi-tenant Close apps require Close approval to become public OAuth apps.</td>
            </tr>
            <tr>
              <td><strong>Front</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (partner-gated)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Agent is more accurate for multi-tenancy.</strong> Front supports API keys for internal scripts, but multi-tenant apps require official App Store partner review.</td>
            </tr>
            <tr>
              <td><strong>Ahrefs</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (partner-gated)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Agent is correct.</strong> Ahrefs API v3 supports OAuth2 via "Ahrefs Connect", strictly requiring Enterprise plan + sales approval. API key is personal single-account only.</td>
            </tr>
            <tr>
              <td><strong>Vercel</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (self-serve-free)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Both valid.</strong> Composio uses personal access tokens; Vercel Integrations platform supports self-serve multi-tenant OAuth2 apps.</td>
            </tr>
            <tr>
              <td><strong>Cloudflare</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (self-serve-free)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Both valid.</strong> Cloudflare supports both scoped API Tokens and OAuth 2.0 applications for third-party integrations.</td>
            </tr>
            <tr>
              <td><strong>Consensus</strong></td>
              <td><span class="badge badge-oauth">OAuth2</span> (self-serve-free)</td>
              <td><span class="badge badge-apikey">API_KEY</span></td>
              <td><strong>Agent caught the latest 2025/2026 update.</strong> Consensus released an official OAuth2 PKCE MCP server (<span class="code-pill">mcp.consensus.app/mcp</span>) alongside its legacy REST API key.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Runnable Proof / How to Run Section -->
    <section class="section-box">
      <div class="section-header">
        <div>
          <h2 class="section-title">Runnable Proof & Reproducibility</h2>
          <p class="section-subtitle">Step-by-step instructions to run the research agent and reproduce all 100 rows locally.</p>
        </div>
      </div>

      <pre class="code-snippet"><code># 1. Clone the repository
git clone https://github.com/krbok/Composio.git
cd Composio

# 2. Setup Python environment & Claude CLI
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
npm install   # Installs local @anthropic-ai/claude-code for reproducible agent execution

# 3. Configure Composio API Key
cp .env.example .env
# Edit .env and add: COMPOSIO_API_KEY=your_key_here

# 4. Run the 5-app stress test or the full 100-app research pipeline
python -m research.stress_test     # Fast 5-app benchmark
python -m research.run_all         # Resumable 100-app batch runner
python -m research.verify_stress_test # Dual-pass verification loop</code></pre>
    </section>
  </main>

  <!-- Modal for App Deep Dive -->
  <div id="detailModal" class="modal-overlay" onclick="closeModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeModal()">&times;</button>
      <div class="modal-header">
        <h3 id="modalAppName" class="modal-app-name">App Name</h3>
        <span id="modalCategory" class="badge badge-oauth">Category</span>
      </div>

      <div class="modal-row">
        <div class="modal-row-label">Summary & Integration Verdict</div>
        <div id="modalOneLiner" class="modal-row-content"></div>
      </div>

      <div class="modal-row">
        <div class="modal-row-label">Multi-Tenant Gating & Main Blocker</div>
        <div id="modalBlocker" class="modal-row-content"></div>
      </div>

      <div class="modal-row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
        <div>
          <div class="modal-row-label">Auth Method</div>
          <div id="modalAuth" class="modal-row-content"></div>
        </div>
        <div>
          <div class="modal-row-label">Self-Serve Status</div>
          <div id="modalGating" class="modal-row-content"></div>
        </div>
        <div>
          <div class="modal-row-label">API Surface & Breadth</div>
          <div id="modalSurface" class="modal-row-content"></div>
        </div>
        <div>
          <div class="modal-row-label">MCP Support</div>
          <div id="modalMcp" class="modal-row-content"></div>
        </div>
      </div>

      <div class="modal-row" style="margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
        <div class="modal-row-label">Verified Documentation Evidence</div>
        <div class="modal-row-content">
          <a id="modalEvidence" href="#" target="_blank" rel="noopener noreferrer">View Official Docs ↗</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <div class="container">
      <p>Composio App Research Pipeline &bull; Automated Agent Loop with Dual-Stage Verification</p>
      <div class="footer-links">
        <a href="https://github.com/krbok/Composio" target="_blank">GitHub Repository</a>
        <a href="https://composio.dev" target="_blank">Composio.dev</a>
        <a href="https://docs.composio.dev" target="_blank">Composio Documentation</a>
      </div>
    </div>
  </footer>

  <!-- Interactive JavaScript Engine -->
  <script>
    const appsData = {data_json};
    let currentSort = {{ field: 'app', asc: true }};
    let filteredData = [...appsData];

    function renderTable() {{
      const tbody = document.getElementById('matrixTableBody');
      tbody.innerHTML = '';

      filteredData.forEach((row, index) => {{
        const tr = document.createElement('tr');

        // Build badges
        let buildBadge = '';
        if (row.buildability === 'buildable-now') {{
          buildBadge = '<span class="badge badge-buildable-now">Buildable Now</span>';
        }} else if (row.buildability === 'buildable-with-friction') {{
          buildBadge = '<span class="badge badge-friction">With Friction</span>';
        }} else {{
          buildBadge = '<span class="badge badge-blocked">Blocked</span>';
        }}

        let authBadge = '';
        if (row.auth_method === 'OAuth2') {{
          authBadge = '<span class="badge badge-oauth">OAuth2</span>';
        }} else if (row.auth_method === 'API key') {{
          authBadge = '<span class="badge badge-apikey">API Key</span>';
        }} else {{
          authBadge = `<span class="badge badge-mcp-community">${{row.auth_method}}</span>`;
        }}

        let mcpBadge = '';
        if (row.has_mcp === 'yes-official') {{
          mcpBadge = '<span class="badge badge-mcp-official">Official MCP</span>';
        }} else if (row.has_mcp === 'yes-community') {{
          mcpBadge = '<span class="badge badge-mcp-community">Community</span>';
        }} else {{
          mcpBadge = '<span class="badge badge-mcp-no">No MCP</span>';
        }}

        const confPct = Math.round(row.confidence * 100);

        tr.innerHTML = `
          <td>
            <div class="app-name-cell">
              <span>${{row.app}}</span>
            </div>
            <span class="app-category-badge">${{row.category}}</span>
          </td>
          <td>${{row.category}}</td>
          <td>${{authBadge}}</td>
          <td><span style="font-size: 12px; color: var(--text-secondary);">${{row.self_serve_status}}</span></td>
          <td><span style="font-size: 12px;">${{row.api_surface}} (${{row.api_breadth}})</span></td>
          <td>${{mcpBadge}}</td>
          <td>${{buildBadge}}</td>
          <td>
            <div class="confidence-meter">
              <span>${{confPct}}%</span>
              <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: ${{confPct}}%;"></div>
              </div>
            </div>
          </td>
          <td>
            <button class="details-btn" onclick="openModal(${{index}})">Inspect</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('resultsCounter').innerText = `Showing ${{filteredData.length}} of ${{appsData.length}} apps`;
    }}

    function applyFilters() {{
      const search = document.getElementById('searchInput').value.toLowerCase().trim();
      const cat = document.getElementById('categoryFilter').value;
      const build = document.getElementById('buildFilter').value;
      const auth = document.getElementById('authFilter').value;
      const mcp = document.getElementById('mcpFilter').value;

      filteredData = appsData.filter(item => {{
        if (cat && item.category !== cat) return false;
        if (build && item.buildability !== build) return false;
        if (auth && item.auth_method !== auth) return false;
        if (mcp && item.has_mcp !== mcp) return false;

        if (search) {{
          const matchName = item.app.toLowerCase().includes(search);
          const matchCat = item.category.toLowerCase().includes(search);
          const matchOne = item.one_liner.toLowerCase().includes(search);
          const matchBlock = (item.main_blocker || '').toLowerCase().includes(search);
          if (!matchName && !matchCat && !matchOne && !matchBlock) return false;
        }}
        return true;
      }});

      sortData();
      renderTable();
    }}

    function sortTable(field) {{
      if (currentSort.field === field) {{
        currentSort.asc = !currentSort.asc;
      }} else {{
        currentSort.field = field;
        currentSort.asc = true;
      }}
      sortData();
      renderTable();
    }}

    function sortData() {{
      filteredData.sort((a, b) => {{
        let vA = a[currentSort.field];
        let vB = b[currentSort.field];
        if (typeof vA === 'string') vA = vA.toLowerCase();
        if (typeof vB === 'string') vB = vB.toLowerCase();

        if (vA < vB) return currentSort.asc ? -1 : 1;
        if (vA > vB) return currentSort.asc ? 1 : -1;
        return 0;
      }});
    }}

    function openModal(index) {{
      const item = filteredData[index];
      if (!item) return;

      document.getElementById('modalAppName').innerText = item.app;
      document.getElementById('modalCategory').innerText = item.category;
      document.getElementById('modalOneLiner').innerText = item.one_liner;
      
      const blockerText = item.main_blocker || 'None — Fully self-serve and instantly buildable today.';
      document.getElementById('modalBlocker').innerText = blockerText;

      document.getElementById('modalAuth').innerText = item.auth_method;
      document.getElementById('modalGating').innerText = item.self_serve_status;
      document.getElementById('modalSurface').innerText = `${{item.api_surface}} (${{item.api_breadth}})`;
      document.getElementById('modalMcp').innerText = item.has_mcp;

      const evLink = document.getElementById('modalEvidence');
      evLink.href = item.evidence_url;
      evLink.innerText = item.evidence_url;

      document.getElementById('detailModal').style.display = 'flex';
    }}

    function closeModal(e) {{
      document.getElementById('detailModal').style.display = 'none';
    }}

    // Export JSON handler
    document.getElementById('exportJsonBtn').addEventListener('click', () => {{
      const blob = new Blob([JSON.stringify(filteredData, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'composio_100_apps_research.json';
      a.click();
    }});

    // Event Listeners
    document.getElementById('searchInput').addEventListener('input', applyFilters);
    document.getElementById('categoryFilter').addEventListener('change', applyFilters);
    document.getElementById('buildFilter').addEventListener('change', applyFilters);
    document.getElementById('authFilter').addEventListener('change', applyFilters);
    document.getElementById('mcpFilter').addEventListener('change', applyFilters);

    // Initial Render
    renderTable();
  </script>
</body>
</html>
"""
    OUT_HTML_PATH.write_text(html_content)
    print(f"Generated standalone case study at: {OUT_HTML_PATH}")

if __name__ == "__main__":
    main()
