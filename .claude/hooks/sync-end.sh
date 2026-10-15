#!/usr/bin/env bash
# Sitzungsende: alle Aenderungen committen und auf GitHub pushen.
# Bricht ab, wenn eine private Mailadresse im Spiel waere (Repo ist oeffentlich).
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
case "$(git config user.email)" in
  *@users.noreply.github.com) ;;
  *) echo "[Sync] Abgebrochen: git user.email ist keine noreply-Adresse."; exit 0 ;;
esac
git add -A
if git diff --cached | grep -qiE '@(gmail|googlemail|outlook|hotmail|gmx|bluewin|icloud|yahoo)\.'; then
  git reset -q
  echo "[Sync] Abgebrochen: private Mailadresse in den Aenderungen gefunden."
  exit 0
fi
git diff --cached --quiet || git commit -q -m "Auto-Sync $(date '+%Y-%m-%d %H:%M')"
git push -q >/dev/null 2>&1 || echo "[Sync] Push fehlgeschlagen - wird beim naechsten Ende erneut versucht."
exit 0
