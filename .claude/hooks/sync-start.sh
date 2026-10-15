#!/usr/bin/env bash
# Sitzungsstart: neuesten Stand von GitHub holen, dann HANDOFF.md ausgeben.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
if git pull --rebase --autostash -q >/dev/null 2>&1; then
  echo "[Sync] Stand von GitHub geholt ($(git log -1 --format='%h %cd' --date=format:'%d.%m. %H:%M'))."
else
  git rebase --abort >/dev/null 2>&1
  echo "[Sync] WARNUNG: git pull fehlgeschlagen (offline oder Konflikt) - lokaler Stand, bitte pruefen."
fi
[ -f HANDOFF.md ] && cat HANDOFF.md
exit 0
