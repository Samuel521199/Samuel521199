# Profile design

This repository owns the GitHub profile README at <https://github.com/Samuel521199>.

## Visual direction

Dark technical editorial layout, cyan `#65e5da`, violet `#ba9dec`, near-white typography. Strong hierarchy, one flagship project, two secondary visual cards, and a readable project index. Avoid invented achievements, skill percentages, production-readiness claims, and live-looking operational metrics.

All illustrations are code-native vector typography and technical diagrams in `assets/`. `tools/build_assets.py` is their editable source; run `python tools/build_assets.py` to regenerate six SVGs. They use system fonts, no external resources, and no scripts or foreign objects. Motion is decorative: a slow orbit, low-contrast scan and gentle pulse. `prefers-reduced-motion` disables the animation; static renderers retain the full content. The README includes a compact hero for small screens and descriptive image alternatives.

GitHub sanitizes README HTML, including scripts and inline styles. This design therefore uses Markdown, permitted HTML and embedded SVG images, rather than trying to replace GitHub's site-wide layout. GitHub's own theme remains controlled by the visitor.

## Content policy

Describe the public repository, not private local progress. In particular, JarvisSystem's public README was at 0.1.64 when checked on 2026-10-20; the profile intentionally links to the authoritative progress rather than freezing that version in a banner. Later local work is not evidence of publicly available capabilities.

Public inventory at review: 26 repositories, 9 forks, 17 non-forks including this profile and two empty repositories. The profile does not label all non-forks as original inventions. Forks are separated, empty repositories are not featured as completed work, and Word Front's content-key setup requirement is visible.

Descriptions were checked against repository metadata, README and root directories for the featured projects. This is a content review, not a fresh build or functional audit of those projects.

When updating: confirm public visibility and current README, edit descriptions in `README.md`, update `data/public-projects.json`, regenerate assets if their labels changed, and visually check both GitHub light/dark surroundings and a narrow viewport.

## Sources

- [Public repository API](https://api.github.com/users/Samuel521199/repos?per_page=100)
- [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [GitHub markup sanitization](https://github.com/github/markup#github-markup)

No scheduled maintenance, paid API calls or external analytics are required.
