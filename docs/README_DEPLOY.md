# GitHub Pages deployment

The portfolio is dependency-free static HTML, CSS and JavaScript. GitHub Pages publishes only `docs/`.

## Current state

Prepared on 9 September 2026 against repository commit `82c5e6f1f1641626a9297090107473e37ae85644`. GitHub deployment has not occurred: the connected account `eshukiran` has read-only access to the target repository owned by `EshuKiran119`.

## Required repository configuration

The repository owner must connect GitHub with write access to `EshuKiran119/eswar-test-repository`. In Settings → Pages, select **GitHub Actions** as the build source. The current connector does not expose a Pages settings mutation, so enabling this source may require the owner in GitHub settings.

Once access is available, merge the prepared overlay without removing project folders. Push the portfolio, README updates, validation script and workflow to `main`, then inspect the `Validate and deploy QA portfolio` workflow until deployment succeeds.

Expected address: `https://eshukiran119.github.io/eswar-test-repository/`. This is a deployment target, not a verified live URL yet. No CNAME or custom domain is used.

## Validation and publication order

1. Run `python3 scripts/validate_portfolio.py` and `node --check docs/app.js`.
2. Deploy the site and verify an unauthenticated HTTPS 200 response and correct content; verify HTTP redirects to HTTPS.
3. Check desktop and mobile navigation, LinkedIn and GitHub links, contact URI targets and both resume downloads.
4. Add the verified public URL to the resume, regenerate its PDF from the DOCX, inspect both pages and update both download assets.
5. Redeploy the updated assets and verify their hashes against the final delivered files.
6. Update the root README deployment status only after those checks pass.

Resume download filenames remain stable. Both current resumes contain the published Sites portfolio URL: https://eswar-sai-kiran-quality-engineering.singamsettykiran119.chatgpt.site. Native hosting reports a successful public deployment; direct anonymous HTTP checks from this workspace were blocked, so incognito verification remains unconfirmed.

## Local preview

`npm run dev` starts a dependency-free Node development server; it is not used by GitHub Pages. `/__qa_mobile` is a local-only 390 × 844 preview frame for responsive checks and is not a deployed file. Normal production files live in `docs/`.
