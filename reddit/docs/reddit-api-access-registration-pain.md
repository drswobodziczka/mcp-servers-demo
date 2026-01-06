# Reddit API access (2026): registration & approval friction ("pain")

## TL;DR

If you want to use Reddit’s Data API via OAuth (e.g. through PRAW), **the process may no longer be purely self-service**.

For new integrations, Reddit has introduced a **Responsible Builder Policy** and an **approval process** that can make obtaining working API access feel like a "pain" compared to the old flow.

## What changed (high level)

A recent announcement on r/redditdev states:

- **"Ending Self-Service API access"**
- Developers / researchers / moderators may need to **request approval** before getting access to the public Data API
- Reddit encourages building via **Devvit**; if your use case is not supported, they route you to a **support request form**

## Why it feels like a pain

- You can still find the classic **"create app"** entrypoint, but:
  - Access may depend on additional approvals
  - There is a multi-field request form asking for:
    - purpose/benefit
    - detailed description
    - what’s missing from Devvit
    - subreddits / scope
    - links to code

This is friction for simple read-only use cases (e.g. "analyze public discussions about topic X").

## KISS guidance for our use case (read-only analysis)

When describing the project (e.g. in a request):

- Keep it **read-only** (no posting/voting/messaging)
- Limit scope:
  - small number of posts per query
  - limited comments per thread
- Mention it’s for **personal / research analysis** and respects rate limits

## Relevant links

- Reddit API docs: https://www.reddit.com/dev/api
- Classic app registration (historical entrypoint): https://www.reddit.com/prefs/apps
- r/redditdev announcement (approval + end of self-service):
  - https://www.reddit.com/r/redditdev/comments/1oug31u/introducing_the_responsible_builder_policy_new/
- Responsible Builder Policy (linked from the announcement):
  - https://support.reddithelp.com/hc/articles/42728983564564
- Support request form mentioned in the announcement (developers / non-Devvit use cases):
  - https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164&tf_14867328473236=api_request_type_enterprise

## Notes

- If the support.reddithelp.com pages are blocked in some environments (403), you may need to open them in a normal browser session.
- For implementation we can proceed "mock-first" and plug credentials later (once access is granted).
