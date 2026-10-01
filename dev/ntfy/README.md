# Local ntfy theme development

This setup supports the ntfy base stylesheet for ntfy's web app (Material UI).

## Start and compare

Run from this checkout's root:

```sh
docker compose -f dev/ntfy/compose.yaml up -d
```

| Address | Purpose |
| --- | --- |
| http://localhost:18092/themepark-alerts | Native ntfy without theme.park injection. |
| http://localhost:18093/themepark-alerts | Same app through nginx with theme.park CSS. |
| http://localhost:18871 | Live CSS and resources from this checkout. |

No login is configured. The one-shot `seed` service publishes six sample
notifications to `themepark-alerts` and `themepark-updates`: every priority,
tags shown as emoji, a click link, an action button, a markdown message and a
long one. Messages are kept for a week in the `cache` volume. Opening a topic
URL subscribes the browser to it; subscriptions live in the browser, not the
server, so a fresh browser profile needs to open the topic again.

Edit `css/base/ntfy/ntfy-base.css` and refresh port 18093. To change the
injected option:

```sh
TP_THEME=aquamarine docker compose -f dev/ntfy/compose.yaml up -d proxy
```

`NTFY_TAG` selects another release (default v2.28.0).

## Injection

ntfy serves the web app and the API on the same paths: `/<topic>` is the
topic page for a browser and the publish/subscribe endpoint for clients. The
proxy rewrites only HTML (nginx's default `sub_filter_types`), so JSON, SSE
and WebSocket responses pass through untouched. Check that a client request
such as `curl localhost:18093/themepark-alerts/json?poll=1` still returns
JSON.

## How the stylesheet hooks in

MUI styles components with generated single-class rules plus two-class rules
for states. Its stable hooks are the `Mui<Component>-<slot>` classes. Every
rule is prefixed with `body` so it out-ranks MUI's own without `!important`.
ntfy has its own light/dark setting, so everything is set explicitly rather
than per mode. Status colours (priority icons, error text, the warning
banner's icon) are left alone because they carry meaning.

Two places use MUI's own paper colour and needed their own rules: the sticky
"Subscribed topics" list subheader, and the message bar at the foot of a
topic (a Paper whose direct child is the text field).

## Verified and not

Verified with v2.28.0 in Chromium at 1440x900: every option in
`css/theme-options/`, with ntfy in its default light mode, on the topic page
with the seeded cards, the drawer and the message bar. Also night-owl and
catppuccin-latte with ntfy in dark mode, Settings and the Publish dialog.
Not verified: Firefox, Safari, phone widths, and attachments.

Save screenshots under `dev/artifacts/ntfy/`.
