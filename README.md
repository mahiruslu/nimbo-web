# nimbo.mahiruslu.com

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
  lower than the copy it already cached.
- **`storeUrl` must be an HTTPS URL on `apps.apple.com` or `play.google.com`.**
  Anything else — including an empty string — fails validation for the whole
  document, not just that field.

### ⚠️ Before release: the iOS store URL is a placeholder

`update.ios.storeUrl` is `https://apps.apple.com/tr/app/nimbo/id0000000000`
because the App Store ID does not exist yet. It validates, and it cannot be
reached today (`minVersion` equals the shipping version, so force-update never
fires), but **replace it with the real ID as soon as App Store Connect issues
one.** The Play URL is already correct.

## Deploying

Hosted on Vercel as its own project, separate from `mahiruslu.me`.

The Vercel project (`nimbo-web`, team `mahiruslus-projects`) and the domain are
already created. Only the DNS record is outstanding.

**In Google Cloud DNS**, where `mahiruslu.com` is managed, add one record in the
`mahiruslu.com` zone:

```
Name:  nimbo
Type:  CNAME
TTL:   300
Data:  54c585302a213047.vercel-dns-017.com.
```

That target is issued by Vercel for this specific project — prefer it over the
generic `cname.vercel-dns.com`. If the zone will not accept a CNAME, A records
to `216.198.79.1` and `64.29.17.1` work too, but a CNAME survives Vercel
changing its IPs.

Vercel has already verified ownership of the subdomain (the apex is in use by
another project on the same account), so the certificate is issued as soon as
the record resolves — usually a few minutes.

Verify:

   ```bash
   curl -sI https://nimbo.mahiruslu.com/gizlilik | head -1
   curl -s  https://nimbo.mahiruslu.com/config/app-config.json | head -c 80
   ```

`vercel.json` sets the cache policy for the config endpoint (5 minutes) and a
strict CSP — the site has no scripts at all, so `default-src 'none'` holds.

Deployment protection is on with `all_except_custom_domains`: the `*.vercel.app`
URLs require a Vercel login, `nimbo.mahiruslu.com` is public. Leave it that way
— the app fetches the config anonymously and App Review has to read the privacy
policy without an account.

## Support mailbox

`nimbo@mahiruslu.com` is referenced on every page and is submitted to both
stores as the support address. It must actually receive mail before submission.
