---
layout: default
title: Newsbot – Self-Hosted News-Intelligence Pipeline (Python, SQLite, Ubuntu)
description: "What's the biggest story today, measured by how many outlets are covering it? A self-hosted pipeline that collects 59 RSS feeds from 42 outlets every 15 minutes into SQLite, with deduplication, feed-health monitoring, and verified backups. Ranking is in development."
stack:
  - Python
  - SQL (SQLite)
  - RSS
  - Ubuntu Server
  - systemd
  - ntfy.sh
  - Git
  - Claude Code
pipeline:
  - label: "Feeds"
    detail: "59 validated RSS feeds across 42 outlets"
  - label: "Collector"
    detail: "Runs every 15 minutes on a systemd timer, writes to SQLite, and deduplicates items"
  - label: "SQLite + health"
    detail: "Tracks the status of every feed, detects stale feeds, logs headline revisions, and keeps source-URL provenance"
  - label: "Clustering & ranking"
    detail: "Group headlines into stories and rank them by coverage"
    status: planned
  - label: "Morning digest"
    detail: "About 8am, short and ranked, with deduplication of continuing stories"
    status: planned
  - label: "Push to phone"
    detail: "Push notifications to the phone through ntfy.sh, a free, open-source push service"
  - label: "Two-way requests"
    detail: "Send a command from the phone and get a fresh update or data pull back"
    status: planned
---

<a href="/projects/" class="back-to-projects btn" aria-label="Back to projects page">&larr; Back to Projects</a>

<h1>Newsbot – Self-Hosted News-Intelligence Pipeline (Python, SQLite, Ubuntu)</h1>

<blockquote>
  <p>A self-hosted news-intelligence pipeline that polls 59 RSS feeds from 42 outlets every 15 minutes, stores and deduplicates every story in SQLite, and pushes to your phone. It's being extended to rank each day's biggest stories by how widely they're covered and to answer on-demand requests sent from the phone. It uses no paid services and no AI API calls.</p>
</blockquote>

<div>
{% include tech-badges.html %}
{% include project-callout.html text="Clustering, ranking, the morning digest, and phone requests are in development. The collection, storage, health, backup, and push layers are live." %}
</div>


<details open>
  <summary><strong>The Question</strong></summary>

  <div>

  <h3>What's actually the biggest story today, measured by how many outlets are covering it rather than by any one editor's choice?</h3>
  <p>Every outlet decides for itself what's important. Newsbot measures importance from the outside instead: if dozens of independent outlets are covering the same story, that story is big. That turns "what's the news today" into a data problem. It means collecting broadly, grouping headlines that describe the same event, counting coverage, and handling stories that continue across multiple days.</p>
  <p><strong>The goal (in development):</strong> a short, ranked digest on the phone each morning, plus the ability to ask the server for fresh data at any time.</p>

  </div>
</details>
<details>
  <summary><strong>System Diagram</strong></summary>

  <div>

  <p>Collection, storage, health monitoring, backups, and push delivery are live. Dashed stages are in development.</p>

  {% include pipeline-diagram.html caption="Backups: a nightly timer uses SQLite's backup API, runs an integrity check on the copy, has a proven restore path, and applies retention." %}

  <h3>Constraints</h3>
  <ul>
    <li><strong>$0 budget.</strong></li>
    <li><strong>No paid AI API calls inside the bot,</strong> so ranking is built from data and arithmetic. It keeps the bot free and makes the ranking transparent and explainable from the counts.</li>
    <li><strong>Fully isolated from other services on the same server,</strong> with its own directory, virtualenv, database, and user-scope timers.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Data-Quality Story</strong></summary>

  <div>

  <p>Most of the work so far has been data quality: catching duplicate records, broken feeds, and counting errors before they could distort the analysis.</p>

  <h3>Real Defects Found and Fixed</h3>
  <ul>
    <li><strong>Duplicate rows:</strong> BBC changes a fragment in its item IDs between fetches, which created duplicate rows. Fixed by normalizing the IDs, plus a migration of existing data.</li>
    <li><strong>Inflated counts:</strong> the "times seen" metric counted per document instead of per collection run. Fixed in collector v0.2.</li>
    <li><strong>Test polluting production:</strong> a validation script wrote to the live database by default. It now uses throwaway copies and needs an explicit flag to touch live data.</li>
    <li><strong>Off-by-a-fraction retention bug:</strong> a backup exactly 14 days old was deleted a day early because of a microseconds vs. whole-seconds mismatch. It was caught by a control test and fixed in the script.</li>
    <li><strong>Leftover sidecar files:</strong> backups were published in WAL mode, so every integrity check left sidecar files behind. Archives are now single self-contained files.</li>
    <li><strong>Unicode crash:</strong> a Unicode character crashed the notification title path. Fixed by sending the title in the JSON body.</li>
  </ul>

  <h3>How I Validate the Checks</h3>
  <p>Every check was validated with negative controls, meaning deliberately planted errors that the check had to catch before its results were trusted. The feed validation included deliberately bad URLs that the check had to reject. A check that can't fail proves nothing.</p>

  </div>
</details>
<details>
  <summary><strong>Sample Digest &amp; Exploratory Findings – In Development</strong></summary>

  <div>

  <p>Neither the digest nor the exploratory analysis exists yet, so there are no results to show here.</p>
  <ul>
    <li><strong>Deliberately waiting:</strong> clustering and ranking will be written after about a week of real data. Tuning them on one evening's headlines would overfit.</li>
    <li><strong>Next:</strong> clustering and ranking, then the 8am digest, then two-way phone requests.</li>
    <li><strong>After that, exploratory analysis:</strong> output by outlet, publish-to-fetch lag, and headline-revision rates.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Tools &amp; Constraints</strong></summary>

  <div>

  <h3>Project Facts</h3>
  <table>
    <tbody>
      <tr><th scope="row">My role</th><td>Designed and directed, built with Claude Code.</td></tr>
      <tr><th scope="row">Status</th><td>The collection, storage, health, backup, and push layers are live. Clustering, ranking, the morning digest, and two-way requests are in development.</td></tr>
      <tr><th scope="row">Sources</th><td>59 validated RSS feeds across 42 outlets</td></tr>
      <tr><th scope="row">Schedule</th><td>Every 15 minutes on a systemd timer; nightly verified backups</td></tr>
      <tr><th scope="row">Budget</th><td>$0</td></tr>
      <tr><th scope="row">AI usage</th><td>No paid AI API calls inside the bot</td></tr>
      <tr><th scope="row">Isolation</th><td>Fully isolated from other services on the same server</td></tr>
    </tbody>
  </table>

  <h3>Tech Stack</h3>
  <ul>
    <li><strong>Python:</strong> collector, feed validation, migrations, backup and retention scripts</li>
    <li><strong>SQL / SQLite:</strong> schema, deduplication, migrations, health and provenance tables</li>
    <li><strong>Linux and automation:</strong> Ubuntu Server, systemd timers, self-hosted and unattended</li>
    <li><strong>Reliability:</strong> verified backups, restore test, retention, health watchdog (being added)</li>
    <li><strong>Delivery:</strong> ntfy.sh, a free, open-source push service</li>
    <li><strong>Git / GitHub:</strong> private repo, commits verified by object hash</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Current Status</strong></summary>

  <div>

  <p><em>As of 2026-09-20.</em></p>
  <ul>
    <li><strong>Live:</strong> validated and deployed 59 feeds from 42 outlets; collection runs unattended every 15 minutes</li>
    <li><strong>Live:</strong> nightly verified backups, with the restore path proved</li>
    <li><strong>Live:</strong> ntfy push delivery proved end to end, with notifications received on the phone</li>
    <li><strong>Being added:</strong> a health watchdog</li>
    <li><strong>In development:</strong> clustering and ranking, then the 8am digest, then two-way phone requests</li>
  </ul>
  <p>Source code is currently private.</p>

  </div>
</details>
