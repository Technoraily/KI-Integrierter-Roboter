# Am Projekt auf einem zweiten Computer arbeiten

Der Abgleich läuft über das GitHub-Repo. Beim Start einer Claude-Sitzung wird automatisch `git pull` ausgeführt, beim Beenden werden alle Änderungen committet und gepusht.

## 1. Hook-Konfiguration

Liegt im Repo als `.claude/settings.json` und kommt mit `git clone` mit – nichts zu tun. Inhalt zur Kontrolle:

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|clear|resume",
        "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/sync-start.sh\"" } ] }
    ],
    "SessionEnd": [
      { "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/sync-end.sh\"" } ] }
    ]
  }
}
```

## 2. Zweiter Computer einrichten

1. Git für Windows und Claude Code installieren.
2. Projekt holen:
   ```
   git clone https://github.com/Technoraily/KI-Integrierter-Roboter.git "C:\Claude\KI-Integrierter Roboter"
   ```
   (Gleicher Pfad wie auf dem ersten Computer ist empfohlen.)
3. **Wichtig, sonst wird die private Mailadresse öffentlich:** im Projektordner
   ```
   git config user.name "Nevio"
   git config user.email "275000754+Technoraily@users.noreply.github.com"
   ```
   Das End-Skript bricht ab, wenn hier keine noreply-Adresse steht.
4. Bei GitHub anmelden, damit Push funktioniert (z. B. `gh auth login` oder beim ersten Push im Browser-Fenster).
5. Fusion 360 mit demselben Autodesk-Konto: die Fusion-Dokumente liegen in der Autodesk-Cloud und sind schon synchron. Den Fusion-MCP-Add-in auf dem zweiten Computer separat installieren.

## Grenzen

- Nur an einem Computer gleichzeitig arbeiten, sonst gibt es Konflikte.
- Wird das Fenster hart geschlossen oder stürzt der Computer ab, läuft der Push erst beim nächsten Sitzungsende.
- Nicht synchronisiert werden: alles in `.gitignore` (z. B. `cad/Bambu Studio Saves/`, die `.docx`-Stücklisten) und das Claude-Gedächtnis unter `%USERPROFILE%\.claude` – die Regeln daraus stehen deshalb in `CLAUDE.md`.
- Jeder automatische Push ist sofort öffentlich sichtbar.
