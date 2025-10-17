# ShareJadPi v4.5.4

Date: 2025-10-17

## Highlights

- Ultra-reliable online wait flow: redirect only when Cloudflare tunnel is truly reachable
- No token in URL: secure POST-based auth sets cookie then redirects to clean path
- Fixed double-token bug in some redirects
- Faster first/second opens with caching
  - Server-side hostname reachability cache (2 min)
  - Client-side localStorage cache (2 min) to skip the wait page
- Smarter readiness probe
  - Backend now checks `/<health>` (public, tiny) via the tunnel instead of HEAD to `/?k=...`
  - Avoids CORS/redirect noise and reduces false positives
- DoH (dns.google) assist for status messages
  - We use DoH only to inform UX; no redirect based on DoH alone

## Technical changes

- `sharejadpi.py`
  - `APP_VERSION = "4.5.4"`
  - New route: `/auth/enter` (POST) accepts token, sets `sjk` cookie (HttpOnly), redirects to clean `/`
  - `/api/tunnel/status`:
    - Returns `url` as base (no token)
    - Reachability check switched to `GET https://<tunnel>/health` with 8s timeout
    - Server-side cache: hostname -> last success timestamp (TTL=120s)
  - `/online-wait` script:
    - Secure POST redirect instead of tokenized URL
    - Uses DoH for messaging only; redirect happens on `reachable: true` or via manual button
    - Local cache to skip wait for recently-verified hostnames

## Upgrade notes

- No action required for users
- If you automated testing against the old `/?k=...` redirect pattern, update tests to accept POST-based `/auth/enter` flow

## Known

- Cloudflare quick tunnels may still take a few seconds to publish DNS; the wait page will show progress until `/health` returns 200
- On extremely slow edge cases, use the "Open Link Now" button (still secure POST)
