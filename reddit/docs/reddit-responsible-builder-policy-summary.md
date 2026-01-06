# Reddit Responsible Builder Policy (2026) — summary

## TL;DR

Reddit requires **explicit approval** before using Reddit Data APIs, and enforces strict rules around transparency, rate limits, privacy, and prohibition of (unapproved) commercialization / AI training.

For our use case (read-only Reddit opinion analysis): keep scope small, be transparent, respect rate limits, and avoid any form of user profiling or sensitive inference.

## Core restrictions (apply to everyone)

- Approval required
  - You must request access and get **explicit approval** before accessing Reddit data via the API.
  - You must comply with all applicable terms.
- Be transparent
  - Do not misrepresent or mask how/why you access Reddit data.
  - No multiple accounts / multiple requests for the same use case.
- Respect the limits
  - Do not circumvent or exceed access limits.
  - Avoid excessive usage that disrupts APIs or networks.

## Developers (non-commercial, incl. modtools)

- Reddit expects developers to use **Devvit** (Developer Platform) for building apps on Reddit.
- All developers must comply with **Developer Terms**.
- If the use case is not supported by Devvit: file a support ticket (approval path).

### Mod tools specifics

- Access granted solely for moderation actions.
- Must not leverage mod status for non-moderation functionality.
- Subject to Devvit App Review.

## Bots and automated activity

### Transparency requirements

- Bots must clearly disclose they are bots.
- Bots must not bypass bot labeling.
- Purpose and scope must be narrow (only needed subreddits/actions).
- Private communications require explicit user consent.

### Prohibited

- Manipulation of platform features (voting/karma).
- Circumventing safety mechanisms (blocking/bans).
- Spamming via automated posts/comments/DMs, including repeated content across subreddits.

## Researchers

(For accredited academics / Reddit for Researchers participants)

- Retain data only as long as necessary for the project.
- Re-run queries against latest exports to account for deletions.
- Must comply with Privacy Policy and applicable Reddit terms.

## Other prohibited practices (everyone)

- No unapproved commercialization or AI training
  - No selling/licensing/sharing/commercializing Reddit data without written approval.
  - Includes using Reddit data to train ML/AI models.
- No illegal or malicious activity
  - No deceptive/improper use.
  - Content posted via Data API must comply with Reddit Rules.
- Zero tolerance for privacy violations
  - Do not infer sensitive user traits (health, politics, sexual orientation, etc.).
  - No re-identification/de-anonymization.
- Do not disrupt APIs
  - No circumvention/exceeding limits.
  - No abusive usage.

## Enforcement

Reddit may:

- Revoke access tokens
- Suspend app/account
- Suspend associated accounts/bots/domains/subreddits

## Link

- Policy page: https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
