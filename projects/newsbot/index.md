---
layout: default
title: Newsbot – Ranking the News by Outlet Count (Python, SQLite, TF-IDF)
description: "A self-hosted pipeline that ranks each day's news by how many distinct outlets carried a story, and a one-week case study of what that count can and cannot tell us."
stack:
  - Python
  - SQL (SQLite)
  - RSS
  - TF-IDF clustering
  - Permutation testing
  - Ubuntu Server
  - systemd
  - GitHub Actions
  - Claude Code
pipeline:
  - label: "Feeds"
    detail: "76 RSS/Atom feeds from 54 outlets"
  - label: "Collect"
    detail: "Every 15 minutes into SQLite"
  - label: "Group into stories"
    detail: "Last 24 hours, grouped by word overlap"
  - label: "Rank"
    detail: "Each story weighted by how many distinct outlets carried it"
  - label: "Morning digest"
    detail: "The top 10 stories, one link each, pushed to a phone"
---

<a href="/projects/" class="back-to-projects btn" aria-label="Back to projects page">&larr; Back to Projects</a>

<h1>Newsbot – Ranking the News by Outlet Count (Python, SQLite, TF-IDF)</h1>

<blockquote>
  <p>Newsbot reads 76 news feeds from 54 outlets every 15 minutes, groups the headlines into stories, and each morning sends a phone the ten stories carried by the most independent outlets. This case study uses one week of real data to ask what that outlet count can and cannot tell us.</p>
</blockquote>

<div>
{% include tech-badges.html %}
{% include project-callout.html label="Source code:" text='The repository is private. Code available on request – see <a href="/#contact">Contact</a>.' %}
</div>


<details open>
  <summary><strong>The Question</strong></summary>

  <div>

  <h3>If a story's rank is "how many outlets ran it", what could make that rank misleading?</h3>
  <ol>
    <li><strong>Timing.</strong> Is there a real pattern in who reports a story first, or does it only look that way because some outlets publish more?</li>
    <li><strong>Copies.</strong> When several outlets run the same wire-agency text, is one source counted several times?</li>
    <li><strong>Fixes that backfire.</strong> When one story is split across two lines, would a rule that joins them make the ranking better, or quietly worse?</li>
  </ol>

  </div>
</details>
<details>
  <summary><strong>The Data</strong></summary>

  <div>

  {% include pipeline-diagram.html %}

  <ul>
    <li><strong>Collected:</strong> headlines, summaries and links from 76 feeds by 54 outlets. When we first saw an item is stored apart from when the outlet says it was published, because the two often disagree.</li>
    <li><strong>How often:</strong> every 15 minutes, plus up to 3 minutes of random delay. A run takes about 3 minutes, so two items seen in the same run cannot be put in order.</li>
    <li><strong>Unit of analysis:</strong> each morning, the last 24 hours are grouped into stories by word overlap (TF-IDF, which discounts common words, with average-link clustering at a 0.3 similarity cut-off). A story's weight is its number of distinct outlets.</li>
    <li><strong>The week:</strong> seven mornings, 21–27 September 2026, 493 to 1,828 items each. That gave 803 stories with at least two outlets, 331 with three or more, and 180 with four or more.</li>
    <li><strong>Limitation:</strong> the last three mornings are real runs. The first four are replays using today's summaries, because outlets rewrite them and the old text was not kept.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>Finding 1 – Who Breaks Stories First</strong></summary>

  <div>

  <h3>A real pattern, but no outlet dominates</h3>
  <p><strong>Method:</strong> in each of the 180 stories with four or more outlets, the "first" outlet is the one whose earliest item arrived in the story's first collection run (tied outlets share the credit; 18 stories had a tie). Each outlet's first-place rate is compared with what chance predicts from its share of the story's items.</p>
  <p><strong>Result:</strong> of the 24 outlets in at least 10 of these stories, six fall outside the middle 90% of what 500 random shuffles produce.</p>

  <div style="overflow-x: auto;">
  <table class="results-table">
    <thead>
      <tr><th scope="col">Outlet</th><th scope="col">Stories</th><th scope="col">First-place rate</th><th scope="col">Chance rate</th><th scope="col">vs. shuffles</th></tr>
    </thead>
    <tbody>
      <tr><td>Financial Times</td><td>17</td><td>0.41</td><td>0.14</td><td>above</td></tr>
      <tr><td>Washington Post</td><td>20</td><td>0.30</td><td>0.13</td><td>above</td></tr>
      <tr><td>ABC News</td><td>39</td><td>0.29</td><td>0.14</td><td>above</td></tr>
      <tr><td>NBC News</td><td>56</td><td>0.27</td><td>0.16</td><td>above</td></tr>
      <tr><td>CBS News*</td><td>83</td><td>0.22</td><td>0.18</td><td>within</td></tr>
      <tr><td>NPR</td><td>32</td><td>0.03</td><td>0.16</td><td>below</td></tr>
      <tr><td>UPI</td><td>67</td><td>0.06</td><td>0.23</td><td>below</td></tr>
    </tbody>
  </table>
  </div>
  <p><em>*For scale: the outlet in the most stories. "vs. shuffles" is where the outlet falls against the middle 90% of 500 shuffles.</em></p>

  <p><strong>The shuffle test:</strong> shuffling arrival times within each story keeps every outlet's volume but destroys any real timing. The spread of first-place rates then falls from 0.095 to 0.028, which is what pure chance gives (0.029). The real data's total deviation from chance is 77.2; over 200 shuffles the median is 47.4 and the maximum 66.0. <strong>None of the 200 reaches the real value</strong>, so the pattern is not just a side effect of how much each outlet publishes.</p>
  <p><strong>Limits:</strong> "first" means first in the outlet's feed, which mixes newsroom speed with how often the feed refreshes. In 43 stories the runner-up arrived in the same run or the next. And six outliers of 24 (chance alone gives about 2.4) is only modest evidence about any single outlet; the overall result is the strong one.</p>

  </div>
</details>
<details>
  <summary><strong>Finding 2 – Copied Wire Text Barely Moves the Count</strong></summary>

  <div>

  <h3>Small effect, unreliable rule, so nothing was built</h3>
  <p><strong>Method:</strong> fixed before any result was read. Two items from different outlets in one story are copies if their headline word sets overlap by 90% or more, or their summaries are identical. Outlets linked by copies collapse into one "source".</p>
  <p><strong>Result:</strong> 23 of 331 stories with three or more outlets contain copied text, and the outlet total across them falls from 1,555 to 1,526 (−1.9%). Ranking by sources instead of outlets changes 4 of the week's 70 top-10 lines.</p>
  <p><strong>The rule's errors are as large as its effect.</strong> All 30 stories with a matched pair were labelled: 17 looked like shared copy, 7 like independent outlets writing near-identical short headlines, and 6 were unclear. These labels were judgement calls made by the AI assistant during the analysis, are listed in full in the project's reports, and were not reviewed by a human expert. No threshold separates the two:</p>

  <div style="overflow-x: auto;">
  <table class="results-table">
    <thead>
      <tr><th scope="col">Copy rule</th><th scope="col">Stories losing outlets</th><th scope="col">Outlets lost (of 1,555)</th><th scope="col">Top-10 changes (of 70)</th></tr>
    </thead>
    <tbody>
      <tr><td>Identical headline or summary</td><td>13</td><td>13</td><td>1</td></tr>
      <tr><td>Same word set, or identical summary</td><td>21</td><td>22</td><td>4</td></tr>
      <tr><td><strong>Overlap ≥ 0.9 (the rule measured)</strong></td><td><strong>23</strong></td><td><strong>29</strong></td><td><strong>4</strong></td></tr>
      <tr><td>Overlap ≥ 0.8</td><td>44</td><td>70</td><td>7</td></tr>
      <tr><td>Overlap ≥ 0.7</td><td>72</td><td>144</td><td>12</td></tr>
    </tbody>
  </table>
  </div>
  <p><em>Stories with three or more outlets.</em></p>

  <p><strong>And text can't see the copies that matter most.</strong> ABC News marks wire-agency stories in its URLs. Of 17 such items in multi-outlet stories, only 4 match another outlet under the rule; the others had been retitled.</p>
  <p><strong>Decision: don't build it.</strong> The effect is small, the rule is about as often wrong as right, and the biggest source of inflation is invisible to it.</p>

  </div>
</details>
<details>
  <summary><strong>Finding 3 – A Bad Merge Caught Before It Shipped</strong></summary>

  <div>

  <h3>A fix for split stories quietly suppressed a different story</h3>
  <p><strong>The problem:</strong> the 0.3 cut-off sometimes splits one story in two. The week had 19 such pairs among the mornings' top 20 stories.</p>
  <p><strong>Choosing a rule:</strong> of five join rules tried, the one chosen (join two top-20 stories whose average similarity is at least 0.25) was fixed before any result was seen. Its 7 merges were labelled 6 same story, 1 unclear, 0 different. These labels were judgement calls made by the AI assistant during the analysis, are listed in full in the project's reports, and were not reviewed by a human expert. A rival rule was rejected because its one wrong merge joined two different Supreme Court rulings.</p>
  <p><strong>Switched on:</strong> the rule was built behind a switch that defaults to off, and "off" was proven to leave the digest byte-identical. Switched on for a re-run of 27 September, it made two merges. One worked: the lead story grew from 11 to 13 outlets. The other joined a US–China tariffs story to "White House: Trump, Xi agree on 'super intelligence' dialogue" at 0.251, just over the bar. Both covered one summit, but the merged story now counted as a Trump story, and the digest's one-Trump-story-a-day cap held it back. A rule meant to fix duplicate lines had, through an unrelated rule, suppressed a trade story. That morning's top 10 did not change, but this was exactly the interaction the analysis had warned about.</p>
  <p><strong>Response:</strong> the merge is not applied. A log-only mode, built and still switched off, will record what each merge would do, including whether it creates a Trump story, without changing the message.</p>

  </div>
</details>
<details>
  <summary><strong>How the Findings Are Checked</strong></summary>

  <div>

  <p>Every check is shown to be able to give the other answer. A check that can't fail proves nothing.</p>
  <ul>
    <li><strong>Negative controls:</strong> the copy rule passes 11 planted cases, and each of six deliberately broken versions of it fails at least one.</li>
    <li><strong>Shuffle test:</strong> destroy the real signal, keep everything else, and confirm the result disappears.</li>
    <li><strong>Independent re-computation:</strong> before re-ranking by sources, the same code ranking by outlets had to reproduce the real top 10 on all seven mornings.</li>
    <li><strong>Deliberate breakage:</strong> break a new feature on purpose and confirm the tests go red. The split-merge switch has 7 such planted breaks, all caught.</li>
    <li><strong>Automated tests:</strong> 10 test suites run in GitHub Actions on every push; a one-line break pushed into each of two new code paths turned only that path's test red. Another 9 suites need the live data and run only on the home server.</li>
  </ul>

  </div>
</details>
<details>
  <summary><strong>What's Next</strong></summary>

  <div>

  <ol>
    <li><strong>Turn on split-merge logging,</strong> read two weeks of logs, and decide how a merge should interact with the Trump cap before any merge is applied.</li>
    <li><strong>Repeat the breaks-first measurement</strong> over more weeks, for stronger evidence about each outlet.</li>
    <li><strong>Log a wire-copy source count</strong> beside the outlet count, and measure how many outlets mark wire copy anywhere (URL, byline, category).</li>
    <li><strong>Review the feed list</strong> once the 17 newest feeds have seven full mornings, with the rule for dropping a feed written down first.</li>
  </ol>

  </div>
</details>
<details>
  <summary><strong>Project Facts</strong></summary>

  <div>

  <table>
    <tbody>
      <tr><th scope="row">My role</th><td>Designed and directed, built with Claude Code.</td></tr>
      <tr><th scope="row">Status</th><td>Collection and the morning digest run unattended; the digest has been live since 26 September 2026. New ranking rules ship switched off until there is evidence to turn them on.</td></tr>
      <tr><th scope="row">Sources</th><td>76 RSS/Atom feeds from 54 outlets</td></tr>
      <tr><th scope="row">Code</th><td>Private repository; available on request</td></tr>
    </tbody>
  </table>

  </div>
</details>
