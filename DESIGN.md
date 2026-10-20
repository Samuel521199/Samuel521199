# Profile design

This repository owns the GitHub profile README at <https://github.com/Samuel521199>.

## Visual direction

Dark technical editorial layout, cyan `#65e5da`, violet `#ba9dec`, near-white typography. Strong hierarchy, one flagship project, two secondary visual cards, and a readable project index. Avoid invented achievements, skill percentages, production-readiness claims, and live-looking operational metrics.

`tools/build_assets.py` generates nine SVG layouts and decorative modules. The mecha hero embeds `assets/mecha-source.png` as a data URI so it works as a self-contained GitHub image; the original PNG is unchanged. System fonts, no scripts, foreign objects or remote image dependencies. Decorative motion includes a slow rotating core, low-contrast scan, code rain, circuit flow and gentle pulse. `prefers-reduced-motion` disables animation; static renderers retain the content. Compact layouts and descriptive image alternatives are included.

The mecha, hangar and drone workshop art are generated concept illustrations, not screenshots or implemented hardware. The built-in image generation tool was used (not a paid API/CLI script). Original production prompts are recorded below. Generated PNGs are stored in `assets/`, alongside reproducible layout code.

GitHub sanitizes README HTML, including scripts and inline styles. This design therefore uses Markdown, permitted HTML and embedded SVG images, rather than trying to replace GitHub's site-wide layout. GitHub's own theme remains controlled by the visitor.

## Content policy

Describe the public repository, not private local progress. In particular, JarvisSystem's public README was at 0.1.64 when checked on 2026-10-20; the profile intentionally links to the authoritative progress rather than freezing that version in a banner. Later local work is not evidence of publicly available capabilities.

Public inventory at review: 26 repositories, 9 forks, 17 non-forks including this profile and two empty repositories. The profile does not label all non-forks as original inventions. Forks are separated, empty repositories are not featured as completed work, and Word Front's content-key setup requirement is visible.

Descriptions were checked against repository metadata, README and root directories for the featured projects. This is a content review, not a fresh build or functional audit of those projects.

When updating descriptions: confirm public visibility and current README, edit `README.md`, regenerate layout assets if labels changed, and check both light/dark surroundings and narrow layouts. The statistics collector does not rewrite curated project descriptions or regenerate AI art.

## Automatic statistics

Authorized on 2026-10-20. `.github/workflows/profile-stats.yml` runs every six hours at UTC minute 23, on relevant default-branch source pushes, and on manual workflow dispatch. Other repositories do not directly trigger this workflow: their changes appear on its next successful collection. GitHub scheduling and image caching can delay display; the SVG states its UTC collection time. GitHub may disable schedules for public repositories with prolonged inactivity; the Actions page shows workflow health and offers manual execution.

`tools/update_stats.py` uses the public `/users/Samuel521199/repos` endpoint with pagination, explicitly rejects nonpublic/other-owner entries, and publishes only allowlisted metadata. No private repository endpoint or personal token is needed. The Actions token can write only this repository. Outputs: `data/public-projects.json`, `assets/stats.svg`, `assets/stats-compact.svg`. Network/API failures fail the job before touching generated outputs; a failed workflow does not commit partial data. Existing successfully collected pictures remain with their original timestamp.

Definitions: public count includes this profile and empty repositories; non-Fork does not mean original invention; language distribution counts the primary language of each non-Fork repository, skipping unknown values, not byte shares or proficiency. Stars and forks received sum the currently public inventory. Featured dates use `pushed_at` in UTC, not general metadata `updated_at`. Newly private/deleted repositories disappear from the next snapshot; curated prose is reviewed separately.

Local refresh: `python tools/update_stats.py`. Validate collector boundaries: `python -m unittest discover -s tests`. No package dependencies. The job commits only its three generated outputs and does not recurse on its bot commits.

## Sources

- [Public repository API](https://api.github.com/users/Samuel521199/repos?per_page=100)
- [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [GitHub markup sanitization](https://github.com/github/markup#github-markup)

The statistics workflow above is the only scheduled job introduced here. No paid model calls or third-party analytics service are used by updates.

## Artwork prompts

**Mecha hero (`assets/mecha-source.png`, built-in image generation):**

Create one polished wide cinematic banner asset for Samuel's GitHub programmer profile, original mecha + cyberpunk art. Aspect ratio about 3:1 landscape, preferably 1536x512. A magnificent intricate graphite armored humanoid mech bust and helmet occupies the right 42 percent, three-quarter view facing slightly left, precise layered hard-surface metal plates, luminous narrow cyan visor, violet accent lighting, tiny amber indicator lights, elegant serious engineering aesthetic, intricate mechanical detail, beautiful material rendering. Dark midnight navy background #090f19, subtle vertical cyan code-rain and circuit traces across the scene, atmospheric holographic concentric HUD ring behind the mech. Left 52 percent is quiet dark negative space with only very faint code rain so existing profile typography may overlay later. No text, no letters, no logo, no watermark, no UI labels, no weapons. Premium restrained sci-fi concept art, sophisticated contrast, exceptionally sharp render. This is an actual website illustration asset, not a UI mockup or screenshot. Keep head and shoulders fully within frame.

**Hangar (`assets/mecha-hangar.png`, built-in image generation):**

A cinematic panoramic illustration for a cyberpunk developer GitHub portfolio section banner. 3:1 wide landscape composition. The interior of an immense futuristic mecha hangar, three graphite and titanium humanoid mechs secured in docking gantries, central giant armored machine being serviced, layered industrial catwalks, overhead cranes, tiny maintenance robots for scale, luminous cyan reactor cores, violet volumetric light, amber safety strips and warm sparks. Deep midnight navy atmosphere, realistic hard-surface materials, intricate engineered details, balanced premium sci-fi art direction, strong cinematic depth and readable silhouettes. The central mech fully contained, symmetrical architectural composition with a subtle off-axis perspective. Dark enough to harmonize with a #090f19 cyan/violet website, but rich and luminous, not muddy. No words, no labels, no watermark, no logos, no UI or webpage mockup. Original concept art.

**Workshop (`assets/mecha-workshop.png`, built-in image generation):**

A cinematic panoramic original cyberpunk mecha engineering workshop illustration for a GitHub developer portfolio. Wide 3:1 landscape image. Close-to-medium view of an intricate levitating spherical reconnaissance drone with unfolded segmented fins and a luminous cyan optical lens, suspended over a precision maintenance bench. To the right a robotic arm adjusts an exposed violet reactor assembly and precision mech helmet component, tiny holographic circuit schematics without letters floating nearby. To the left layered trays of titanium parts and a glass window into a dark enormous mecha facility. Beautiful midnight navy / cyan / electric violet palette, warm amber accents, refined engineered detail, convincing metal microtexture, premium hard-surface sci-fi rendering, cinematic depth of field but main objects sharply readable. Energetic glowing light trails, intricate but uncluttered composition. No text, no logos, no watermark, no UI frame, no weapon or military insignia. Actual website artwork asset, not mockup.
