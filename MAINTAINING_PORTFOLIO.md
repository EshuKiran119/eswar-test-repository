# Editing and maintaining the portfolio

All portfolio source is ordinary HTML, CSS and JavaScript. There is no proprietary editor or production build dependency.

## Files to edit

| Change | Source |
|---|---|
| Experience, capabilities, projects and contact details | `docs/index.html` |
| Layout, colors, spacing and responsive behavior | `docs/styles.css` |
| Mobile menu and navigation behavior | `docs/app.js` |
| Resume content and DOCX formatting | `scripts/build_resume.py` |
| Recruiter downloads | `docs/assets/Eswar_Sai_Kiran_Singamsetty_ATS_Resume.pdf` and `.docx` |
| Search metadata and site address | `docs/index.html`, `docs/sitemap.xml`, `docs/robots.txt` |
| Source showcase download | `docs/assets/Eswar_QA_Framework_Showcase.zip` |
| GitHub Pages deployment | `.github/workflows/deploy-portfolio-pages.yml` |
| Executed sample evidence | `SAMPLE_VERIFICATION.md` |

## Preview and publish

From the repository root:

```sh
npm run dev
```

Open `http://localhost:4173/`. The optional `/__qa_mobile` route provides a 390-pixel preview frame; it is a development tool and is not published.

Before committing a website change:

```sh
python3 scripts/validate_portfolio.py
node --check docs/app.js
git diff --check
```

Once this source is in the selected GitHub repository and Pages is configured to use GitHub Actions, committing and pushing changes under `docs/` to `main` runs **Validate and deploy QA portfolio**. Check its successful deployment before sharing an updated address. Ordinary changes to sample code do not redeploy the website unless the downloadable package also changes.

## Regenerating the resume

Edit the facts and wording in `scripts/build_resume.py`, or edit the supplied Word document directly. For reproducible Word generation, install `scripts/requirements-resume.txt` in a Python virtual environment and run:

```sh
python3 scripts/build_resume.py --verified-portfolio 'YOUR_VERIFIED_PUBLIC_URL'
```

The result is written under `build/resume/`. Export it to PDF using Word or LibreOffice. Inspect both pages, verify links, and replace both stable filenames in `docs/assets/` together. The script does not claim to verify the URL or enforce a page count after future edits. Recheck the experience duration whenever updating the date.

## Moving to GitHub Pages

Current publication is on the temporary Sites address. The intended `EshuKiran119/eswar-test-repository` GitHub Pages address has not been deployed. See `docs/README_DEPLOY.md` for the access blocker and exact publication order.

After a GitHub Pages deployment succeeds and its address opens anonymously, update the canonical URL, Open Graph URL, sitemap, robots file, README, both resumes and project links together. Keep asset links relative so project-path hosting works. Do not add an unregistered custom domain.

The new frameworks are fictional personal samples. Keep employer source, credentials, customer data and internal endpoints out of every public commit. Record execution honestly in `SAMPLE_VERIFICATION.md` when adding or running capabilities.
