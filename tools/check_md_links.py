"""Check the internal links of the repository's Markdown files.

Every link [text](target) to a local file must point to an existing file or folder, and every
#anchor must exist in the target file, either as an explicit <a id="..."></a> or as a heading
(GitHub slug). External links (http, https, mailto) are not checked.

Run from the repository root:  make check-links
"""
import os
import re
import subprocess
import sys

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ANCHOR = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def strip_code(text):
    text = re.sub(r"^(```|~~~).*?^\1", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def slug(heading):
    """GitHub heading slug: drop markup and punctuation, lower case, spaces to hyphens."""
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # keep link text
    h = re.sub(r"[`*_]", "", h).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path, cache={}):
    if path not in cache:
        with open(path, encoding="utf8") as fh:
            text = fh.read()
        found, seen = set(ANCHOR.findall(text)), {}
        for line in strip_code(text).splitlines():
            m = HEADING.match(line)
            if m:
                s = slug(m.group(1))
                n = seen.get(s, 0)
                seen[s] = n + 1
                found.add(s if n == 0 else f"{s}-{n}")
        cache[path] = found
    return cache[path]


def main():
    files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
    errors = []
    for md in files:
        with open(md, encoding="utf8") as fh:
            text = strip_code(fh.read())
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:", target):
                continue
            path, _, frag = target.partition("#")
            dest = os.path.normpath(os.path.join(os.path.dirname(md), path)) if path else md
            if not os.path.exists(dest):
                errors.append(f"{md}: missing file {target}")
            elif frag and dest.endswith(".md") and frag not in anchors(dest):
                errors.append(f"{md}: missing anchor {target}")
    for e in errors:
        print(e)
    print(f"==> {len(files)} Markdown files checked, {len(errors)} broken link(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
