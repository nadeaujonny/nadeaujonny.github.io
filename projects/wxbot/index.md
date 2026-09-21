---
layout: default
title: wxbot – Automated Weather Data Pipeline with QC, Anomaly Detection & Forecast Scorecard
description: "Where is the weather actually unusual today, not just hot? A design-stage weather data pipeline planned to compare station reports against 1991–2020 normals, with a data-quality layer and an NWS forecast-accuracy scorecard. In development."
stack:
  - Python
  - SQL (SQLite)
  - Ubuntu Server
  - systemd
  - NWS API
  - ntfy
  - Git
  - Claude Code
pipeline:
  - label: "Ingest"
    detail: "NOAA/NWS data every ~5 minutes, conditional download"
  - label: "Parse + QC"
    detail: "Quality control with exclusion counts by reason"
  - label: "Raw database"
    detail: "14-day rolling"
  - label: "Nightly rollup"
    detail: "Hourly → daily"
  - label: "Durable database"
    detail: "Aggregates, daily summaries, events, scorecard"
  - label: "Analysis"
    detail: "Extremes, anomalies, records, alerts, forecast scorecard"
  - label: "Phone push"
    detail: "Morning brief, weekly digest, on-demand replies"
---

<a href="/projects/" class="back-to-projects btn" aria-label="Back to projects page">&larr; Back to Projects</a>

<h1>wxbot – Automated Weather Data Pipeline with QC, Anomaly Detection &amp; Forecast Scorecard</h1>

<blockquote>
  <p>An automated weather-intelligence pipeline designed to ingest worldwide weather-station reports every few minutes, apply data-quality controls, and flag where weather is most unusual for the place and date. It will push briefs and on-demand answers to a phone, with a forecast-accuracy scorecard measuring how often National Weather Service forecasts miss.</p>
</blockquote>

<div>
{% include tech-badges.html %}
{% include project-callout.html text="Design stage – in development. No code is running yet; this page describes the planned system." %}
</div>


<details open>
  <summary><strong>The Question</strong></summary>

  <div>

  <h3>Where is the weather actually unusual today – not just hot?</h3>
  <ul>
    <li><strong>Raw extremes are predictable and boring.</strong> The hottest place on Earth is almost always the Persian Gulf, Sahara, or Death Valley; the coldest is Antarctica. The newsworthy question is <em>anomaly</em>: "Chicago is 22°F above normal" is news; "Kuwait is 115°F" is not.</li>
    <li><strong>"Hottest right now" is a data-quality problem in disguise.</strong> A stuck sensor reading 140°F wins every time unless quality control catches it. Stations go silent, report stale data, disagree with neighbours, and issue corrections.</li>
    <li><strong>Anomaly definitions have traps.</strong> Comparing an 8 a.m. temperature to the normal <em>daily high</em> makes every morning look cold. The definition has to be chosen by measurement and stated in every output.</li>
    <li><strong>Forecast accuracy is measurable but rarely measured personally.</strong> Logging NWS forecasts and matching them to what actually happened produces an accuracy scorecard by city and lead time – a classic analyst deliverable.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Data Sources &amp; Constraints</strong></summary>

  <div>

  <h3>Planned Data Sources (free, government-first)</h3>
  <table style="table-layout: fixed; overflow-wrap: anywhere;">
    <thead>
      <tr><th scope="col">Source</th><th scope="col">Data</th><th scope="col">Role</th></tr>
    </thead>
    <tbody>
      <tr><td>NOAA Aviation Weather Center</td><td>METAR observations from airport stations worldwide</td><td>Core observation feed</td></tr>
      <tr><td>National Weather Service API</td><td>Forecasts, observations, severe alerts</td><td>Scorecard + alerts</td></tr>
      <tr><td>NOAA Regional Climate Centers (ACIS)</td><td>1991–2020 station normals, daily records</td><td>Anomalies and records (US)</td></tr>
      <tr><td>Storm Prediction Center / National Hurricane Center</td><td>Severe-storm outlooks, active hurricanes</td><td>Severe-weather layer</td></tr>
      <tr><td>NOAA buoys &amp; tides (NDBC, CO-OPS)</td><td>Ocean temp, waves, tides</td><td>Local brief</td></tr>
      <tr><td>EPA AirNow (optional)</td><td>Air quality</td><td>Local brief</td></tr>
    </tbody>
  </table>

  <h3>Constraints</h3>
  <ul>
    <li><strong>$0 budget</strong></li>
    <li><strong>Terms of use read and documented for every source before use</strong></li>
    <li><strong>No scraping</strong> – only published files and documented APIs</li>
    <li><strong>No AI/LLM calls inside the pipeline</strong> – all summaries built from data and arithmetic</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Planned Architecture</strong></summary>

  <div>

  <p>Planned to run 24/7 on a home server, scheduled with systemd services.</p>

  {% include pipeline-diagram.html caption="All stages are planned; nothing is running yet. Raw observations will be kept in a 14-day rolling database; a nightly rollup (hourly → daily) will feed a durable database of aggregates, daily summaries, events, and the scorecard." %}

  </div>
</details>
<details>
  <summary><strong>Planned Approach</strong></summary>

  <div>

  <h3>Data Quality Control</h3>
  <p>Every reading will pass a set of rules before it can count:</p>
  <ul>
    <li><strong>Physical plausibility bounds,</strong> set from measured data, not guessed</li>
    <li><strong>Internal consistency:</strong> whole-degree temperature vs. the precise tenths value in the report remarks</li>
    <li><strong>Temporal jumps:</strong> change vs. the station's own previous report</li>
    <li><strong>Spatial consistency:</strong> disagreement with nearby stations</li>
    <li><strong>Staleness:</strong> observations too old to count as "current"</li>
    <li><strong>Corrections:</strong> corrected reports will replace originals, with no double counting</li>
    <li><strong>Every exclusion counted by reason</strong> – a filter that silently drops data is how a real record gets thrown away</li>
    <li><strong>Negative controls:</strong> planted 140°F and stale readings must be excluded; a planted genuine extreme must be kept</li>
  </ul>

  <h3>Anomaly Definition</h3>
  <ul>
    <li>Observed vs. 1991–2020 normals for that station and date</li>
    <li>The definition will be chosen by measurement to avoid the time-of-day trap, and stated in every output</li>
    <li>Records: record highs/lows set today</li>
  </ul>

  <h3>Forecast Accuracy Scorecard</h3>
  <ul>
    <li>Log NWS forecasts daily from Phase 1 (unlogged days are unrecoverable)</li>
    <li>Match the forecast window to the official observation window (a known source of silent error)</li>
    <li>Error by city, lead time, and season; "biggest forecast miss yesterday"</li>
  </ul>

  <h3>Station Data-Quality Report</h3>
  <p>Which stations report bad data, go silent, or disagree with neighbours – tracked over time.</p>

  <h3>Data Lifecycle / Storage</h3>
  <ul>
    <li><strong>Tiered retention:</strong> raw 14 days → hourly aggregates 90 days → daily summaries 2 years</li>
    <li>Rollup verified before any deletion; disk budget with alarms</li>
    <li>Sizing will be set from measured rows/day and bytes/day, not estimates</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Planned Engineering Practices</strong></summary>

  <div>

  <ul>
    <li><strong>Measure before building.</strong> A formal measurement phase will answer every unknown about external services before any pipeline code is written.</li>
    <li><strong>Negative controls on every check</strong> – a check that can't fail isn't a check.</li>
    <li><strong>"Couldn't look" ≠ "nothing there."</strong> Distinct outcomes for data / no change / empty / error / unreachable; HTTP 200 will not be treated as success.</li>
    <li><strong>Staleness is its own failure mode</strong> – the pipeline will flag data that stops updating instead of passing it off as current.</li>
    <li><strong>Provenance:</strong> every run row stamped with the system invocation ID, traceable to logs.</li>
    <li><strong>Verified backups:</strong> integrity-checked copies, test restores, retention only after verification.</li>
    <li><strong>Reliability:</strong> long-running listener with auto-restart, reconnect without replaying old commands, and a heartbeat + health check to be proven by deliberately killing the service.</li>
    <li><strong>Security hygiene:</strong> secrets outside the repo, never logged; phone commands are read-only by design.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Tech Stack &amp; Status</strong></summary>

  <div>

  <h3>Project Facts</h3>
  <table>
    <tbody>
      <tr><th scope="row">My role</th><td>Designed and directed; to be built with Claude Code.</td></tr>
      <tr><th scope="row">Status</th><td>Design complete as of 2026-09-20.</td></tr>
      <tr><th scope="row">Budget</th><td>$0</td></tr>
      <tr><th scope="row">Runtime</th><td>Planned to run 24/7 on a home server</td></tr>
      <tr><th scope="row">AI usage</th><td>No AI/LLM calls inside the pipeline</td></tr>
    </tbody>
  </table>

  <h3>Planned Tech Stack</h3>
  <ul>
    <li><strong>Python</strong> (standard library first): ingest, parsing, QC, analysis</li>
    <li><strong>SQLite:</strong> schema, aggregations, rollups, scorecard queries</li>
    <li><strong>Linux (Ubuntu Server):</strong> systemd scheduled services, backups, monitoring</li>
    <li><strong>ntfy</strong> push notifications</li>
    <li><strong>Git/GitHub</strong></li>
  </ul>

  <h3>Build Roadmap</h3>
  <table>
    <thead>
      <tr><th scope="col">Phase</th><th scope="col">Scope</th></tr>
    </thead>
    <tbody>
      <tr><td>0</td><td>Measurement (Step 0): answer every unknown about external services before any pipeline code is written</td></tr>
      <tr><td>1</td><td>Ingest, QC, storage, forecast logging</td></tr>
      <tr><td>2</td><td>Morning brief</td></tr>
      <tr><td>3</td><td>On-demand phone commands – <strong>V1 milestone</strong></td></tr>
      <tr><td>4</td><td>Anomalies &amp; records</td></tr>
      <tr><td>5</td><td>Severe weather</td></tr>
      <tr><td>6</td><td>Home (local) brief</td></tr>
      <tr><td>7</td><td>Forecast scorecard &amp; station QC report</td></tr>
      <tr><td>8</td><td>Weekly digest</td></tr>
    </tbody>
  </table>

  <p>Source code is not yet published.</p>

  </div>
</details>
