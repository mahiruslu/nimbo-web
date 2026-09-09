# nimboapp.vercel.app

The public site for the Nimbo kids app: legal documents, support, and the app's
remote configuration endpoint.

Plain static HTML — no framework, no build step on the host. `build.py` is the
authoring tool; its output is committed.

```
index.html                 Landing (TR)          /
en/                        Landing (EN)          /en
gizlilik/                  Privacy Policy (TR)   /gizlilik
privacy/                   Privacy Policy (EN)   /privacy
kullanim-kosullari/        Terms of Use (TR)     /kullanim-kosullari
terms/                     Terms of Use (EN)     /terms
destek/                    Support + FAQ (TR)    /destek
support/                   Support + FAQ (EN)    /support
config/app-config.json     Remote config the app fetches at launch
assets/                    Brand SVGs (copied from the app repo) + stylesheet
```

## Editing

Edit `CONTENT` in `build.py`, then:

```bash
python3 build.py
python3 -m http.server 8080   # preview at http://localhost:8080
```

Turkish and English versions of a page live next to each other in `build.py` on
purpose: a legal page whose two translations drift apart is worse than one
language. Change both or neither.

### The facts the pages state

Four constants at the top of `build.py` are the only place a number about the
app is written down, so the landing, download and support pages cannot disagree:

- `APP_VERSION` — the version a visitor can actually download. It moves with the
  store release, **not** with the app repo, and it moves together with
  `latestVersion` in `config/app-config.json`. It is currently **1.7.0**.
- `ACTIVITIES` / `FREE_ACTIVITIES` — 502 and 164. Recount them from the content
  packs rather than from memory:

```bash
cd ../nimbo && npx tsx -e "
import { loadContentPacksFromFileSystem } from './scripts/loadContentPacks';
let total = 0, free = 0;
for (const pack of loadContentPacksFromFileSystem()) {
  const acts = pack.activities ?? [];
  total += acts.length;
  free += acts.filter((a) => a.isFree).length;
  console.log(pack.id, acts.length, acts.filter((a) => a.isFree).length);
}
console.log('TOTAL', total, 'FREE', free);
"
```

- `PRIVACY_VERSION` / `TERMS_VERSION` — bumped only when that document's text
  changes, each with its own date.

**The site describes the shipped build, not the working tree.** Copy that
describes an unreleased version has to go live *with* that release: it is what
App Review and a parent read while deciding, and a page promising a feature the
downloadable binary does not have is worse than a stale one.

Brand assets are copied from `nimbo/src/assets/brand/`, which is generated from
geometry — re-copy rather than hand-editing them here.

## The remote config endpoint

`config/app-config.json` is fetched by the app on every launch (an anonymous
GET; nothing is sent). Its shape must satisfy `isRemoteAppConfig` in
`nimbo/src/core/config/configValidation.ts` — **an invalid payload is rejected
wholesale** and the app silently falls back to its bundled copy.

After changing it, validate against the real validator before deploying:

```bash
cd ../nimbo && npx tsx -e "
import { readFileSync } from 'node:fs';
import { isRemoteAppConfig } from './src/core/config/configValidation';
const raw = JSON.parse(readFileSync('../nimbo-web/config/app-config.json','utf8'));
console.log(isRemoteAppConfig(raw) ? 'PASS' : 'FAIL');
"
```

Two rules that are easy to get wrong:

- **`version` must increase.** The app ignores a payload whose `version` is
  lower than the copy it already cached. It is at **7**, tracking the app's
  minor version (1.**7**.0) so the two are readable side by side — the counter
  only has to grow, so skipping numbers is free.
- **`storeUrl` must be an HTTPS URL on `apps.apple.com` or `play.google.com`.**
  Anything else — including an empty string — fails validation for the whole
  document, not just that field.

`minVersion` drives the undismissable force-update screen and `latestVersion` is
currently read by nothing, so bumping `latestVersion` to the shipping version is
a record, not a behaviour change. **Raising `minVersion` locks every older
install out until it updates** — only do it deliberately, and never above a
version that is actually live in both stores.

The optional `events` key schedules the seasonal world events. It is absent
here on purpose: the payload can only pick *when* an event runs, never invent
one — the ids, copy and rewards are authored in the app
(`src/core/world/world-event-rules.ts`), and an install that cannot reach this
file simply runs no event.

### The iOS store URL

`update.ios.storeUrl` points at the real App Store ID, `id6794716737`, issued
when the app was submitted for review (2026-08-29). It replaced the
`id0000000000` placeholder that shipped while the app had no ID yet.

The URL returns 404 until the app is actually released — that is expected and
harmless, because `minVersion` equals the shipping version, so the force-update
screen that would open it never fires. The Play URL has always been correct.

## Deploying

Hosted on Vercel as its own project (`nimbo-web`, team `mahiruslus-projects`),
separate from the `mahiruslu.me` portfolio. The GitHub repo is connected, so a
push to `main` deploys.

The live address is **https://nimboapp.vercel.app** — a Vercel-assigned domain,
chosen over a custom subdomain to avoid a DNS record. That means deployment
protection must stay **off**: Vercel Authentication only exempts *custom*
domains, so with it on, a `.vercel.app` address returns a login redirect to
everyone, including the app fetching its config and App Review reading the
privacy policy.

    Vercel → nimbo-web → Settings → Deployment Protection
      → Vercel Authentication → Disabled

Nothing here is secret, so public preview deployments are fine.

Verify:

```bash
curl -sI https://nimboapp.vercel.app/gizlilik | head -1
curl -s  https://nimboapp.vercel.app/config/app-config.json | head -c 80
```

### If you later want nimbo.mahiruslu.com

`nimbo.mahiruslu.com` is already added to this Vercel project and ownership is
verified; only DNS is missing. In Google Cloud DNS, in the `mahiruslu.com`
zone:

```
Name: nimbo   Type: CNAME   TTL: 300
Data: 54c585302a213047.vercel-dns-017.com.
```

That target is issued by Vercel for this project — prefer it over the generic
`cname.vercel-dns.com`.

**But note this is not free to switch to.** `NIMBO_WEB_ORIGIN` in the app
(`src/core/links/nimboLinks.ts`) is compiled into the binary, so moving the
config endpoint means shipping an app update and keeping the old address alive
until every install has taken it. Redirecting `nimboapp.vercel.app` would not
be enough on its own — treat the move as a release, not a DNS change.

## Support mailbox

`nimbo@mahiruslu.com` is referenced on every page and is submitted to both
stores as the support address. It must actually receive mail before submission.
