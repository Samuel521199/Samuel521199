"""Refresh public GitHub metadata and self-hosted dashboard SVGs.

Only Python's standard library is required. GITHUB_TOKEN is optional locally;
Actions uses its repository-scoped token. API errors leave published data intact.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import os
from urllib.request import Request, urlopen
from build_assets import svg, text

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Samuel521199"
FEATURED = ("JarvisSystem", "StructForge", "word-front")
COLORS = ("#65e5da", "#b496f0", "#82b9ff", "#e5bb7b", "#ec8cc1", "#89cbaa")


def get_json(path):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "Samuel521199-profile-stats",
               "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request("https://api.github.com"+path, headers=headers), timeout=30) as response:
        return json.load(response)


def fetch_repositories():
    repositories = {}
    for page in range(1, 101):
        batch = get_json(f"/users/{OWNER}/repos?type=owner&per_page=100&sort=full_name&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Invalid repository response")
        for repo in batch:
            if repo.get("private") or repo.get("visibility", "public") != "public":
                continue
            if repo.get("owner", {}).get("login", "").casefold() != OWNER.casefold():
                continue
            repositories[repo["id"]] = repo
        if len(batch) < 100:
            return sorted(repositories.values(), key=lambda r: r["name"].casefold())
    raise ValueError("Pagination did not complete")


def summarize(repos):
    nonfork = [r for r in repos if not r["fork"]]
    languages = Counter(r["language"] for r in nonfork if r.get("language"))
    return {
        "public_repositories": len(repos),
        "non_fork_repositories": len(nonfork),
        "fork_repositories": len(repos)-len(nonfork),
        "language_count": len(languages),
        "primary_languages": dict(sorted(languages.items(), key=lambda item: (-item[1], item[0]))),
        "stars": sum(r["stargazers_count"] for r in repos),
        "forks_received": sum(r["forks_count"] for r in repos),
    }


def dashboard(repos, summary, stamp, compact=False):
    w = 700 if compact else 1200
    h = 890 if compact else 590
    pad = 30
    body = text(pad, 39, "REPOSITORY TELEMETRY / PUBLIC GITHUB", 16, "#65e5da", 'class="mono"')
    body += text(pad, 68, "项目统计 · 自动采集，非实时", 16, "#b9c9dc")
    metrics = [(summary["public_repositories"], "公开仓库 / PUBLIC"),
               (summary["non_fork_repositories"], "非 Fork / NON-FORK"),
               (summary["fork_repositories"], "Fork / FORKS"),
               (summary["language_count"], "主语言种类 / LANGUAGES")]
    for i,(value,label) in enumerate(metrics):
        col, row = (i%2, i//2) if compact else (i,0)
        step = (w-2*pad)/(2 if compact else 4)
        x, y = pad+col*step, 130+row*106
        body += text(x,y,str(value),46,"#f1f7ff",'font-weight="700"')
        body += text(x,y+29,label,14,"#9fb8cd")
    base = 304 if compact else 202
    body += f'<path d="M{pad} {base-12}H{w-pad}" stroke="#2c4058"/>'
    body += text(pad,base+16,
                 f'STARS {summary["stars"]}     FORKS RECEIVED {summary["forks_received"]}',
                 16,"#b9a0f0",'class="mono"')
    body += text(pad,base+48,"非 Fork 仓库主语言分布 · 每仓库计 1",15,"#9fb8cd")
    # A variable-height list avoids clipping when new primary languages appear.
    language_rows = list(summary["primary_languages"].items())
    maximum = max(summary["primary_languages"].values(), default=1)
    for i,(language,count) in enumerate(language_rows):
        y = base+80+i*28
        color = COLORS[i%len(COLORS)]
        body += text(pad,y,language,15,color,'class="mono"')
        bar_x, bar_w = (210, w-300)
        body += f'<rect x="{bar_x}" y="{y-12}" width="{bar_w}" height="8" rx="4" fill="#172638"/>'
        body += f'<rect x="{bar_x}" y="{y-12}" width="{bar_w*count/maximum:.2f}" height="8" rx="4" fill="{color}"/>'
        body += text(w-pad,y,str(count),15,"#d7e5f4",'text-anchor="end" class="mono"')
    projects_y = base+90+28*len(language_rows)
    body += text(pad,projects_y,"FEATURED / 最近代码推送（UTC）",15,"#65e5da",'class="mono"')
    by_name = {r["name"]:r for r in repos}
    for i,name in enumerate(FEATURED):
        y = projects_y+35+i*(58 if compact else 32)
        repo = by_name.get(name)
        body += text(pad,y,name,16,"#edf5ff",'class="mono"')
        if repo:
            detail = f'{repo.get("language") or "—"}  ·  ★ {repo["stargazers_count"]}  ·  {(repo.get("pushed_at") or "—")[:10]}'
        else:
            detail = "当前公开列表不可用"
        body += text(pad if compact else w-pad,y+23 if compact else y,detail,14,"#9fb8cd",
                     '' if compact else 'text-anchor="end"')
    footer_y = projects_y + (205 if compact else 140)
    h = max(h,footer_y+74)
    body += text(pad,footer_y,"含主页仓库；未识别语言不计入语言分布。",13,"#8ca4bd")
    body += text(pad,footer_y+28,f"UPDATED {stamp} UTC · EVERY 6H + PROFILE PUSH",12,"#8ca4bd",'class="mono"')
    return svg(w,h,"Public repository statistics, last collected "+stamp+" UTC",body)


def main():
    repos = fetch_repositories()  # Collect all pages before changing any files.
    if not repos:
        raise ValueError("Empty public inventory; keeping the previous published data")
    summary = summarize(repos)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    fields = ("name","html_url","description","language","fork","archived","size",
              "updated_at","pushed_at","default_branch","stargazers_count","forks_count")
    inventory = {
        "checked_on": stamp[:10], "collected_at_utc": stamp,
        "source": f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100",
        "summary": summary,
        "repositories": [{k:r.get(k) for k in fields} for r in repos],
    }
    outputs = {
        ROOT/"data/public-projects.json": json.dumps(inventory,ensure_ascii=False,indent=2)+"\n",
        ROOT/"assets/stats.svg": dashboard(repos,summary,stamp),
        ROOT/"assets/stats-compact.svg": dashboard(repos,summary,stamp,True),
    }
    for path,content in outputs.items():
        path.parent.mkdir(exist_ok=True)
        temporary = path.with_suffix(path.suffix+".tmp")
        temporary.write_text(content,encoding="utf-8",newline="\n")
        temporary.replace(path)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
