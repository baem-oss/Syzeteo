# Syzeteo – Phase 3: TDD-Gate und GitHub-Branchschutz

**Stand:** 29.10.2026 · **Geltung:** Repository-Governance, nicht fachliche Vollabnahme.

## Stand der automatisierten Prüfungen

Die GitHub-Workflowdatei \`.github/workflows/tests.yml\` enthält:

1. \`traceability_check.py\`: Story-Mappings gegen den eingefrorenen Story-Bestand sowie Testreferenzen.
2. \`acceptance_criteria_check.py\`: gültige/stabile Kriterien-IDs, nichtleere Nachbedingungen, korrekte Story-Zuordnungen, **bidirektionale** Übereinstimmung von Kriteriums- und Story-Mapping und vorhandene Testmethoden mit direkten Assertions. Fehlende oder nicht gemappte Kriterien werden zurückgewiesen.
3. **Nur bei Pull Requests**: beide eingefrorenen Dateien \`Syzeteo-TDD-Baseline.json\` und \`Syzeteo-Akzeptanzkriterien-Baseline.json\` bleiben unverändert.
4. **Nur bei Pull Requests**: \`tdd_pr_evidence_check.py --base-ref origin/<Zielbranch>\`. Für jedes **gegenüber dem Zielbranch neu angelegte oder geänderte** Kriterium ist eine neue bzw. veränderte Assertion in einer referenzierten Testmethode **im selben PR** erforderlich. Bloß eine bestehende Testmethode neu zu referenzieren reicht nicht. Auch das Löschen bereits auf dem Zielbranch registrierter Kriterien wird abgewehrt.
5. \`regression_pipeline.py --native --release\` inklusive der Selbsttests der beiden Prüfer und Release-Hygiene.

**Grenzen:** Eine syntaktisch veränderte Assertion beweist weder ihre semantische Relevanz noch ausreichende Grenzfallabdeckung. Das fachliche Assertions-Review bleibt Pflicht. Ein in der CI gefundener Test kann immer noch qualitativ unzureichend sein; \`specified_partial\` ist deshalb **kein** Status „vollständig abgenommen“. Die manuell gemeldeten UI-PASS-Abnahmen bleiben getrennt dokumentiert.

## GitHub-Zweigschutz: ermittelter Zustand

Am 29.10.2026 über die GitHub-API verifiziert:

- Ruleset **„Ruleset Syzeteo“**, ID **22184406**:
  <https://github.com/baem-oss/Syzeteo/rules/22184406>
- \`enforcement = disabled\`.
- Zielbranch-Bedingung \`ref_name.include = []\`; damit ist aktuell auch kein konkreter Zielbranch erfasst.
- Das vorhandene Ruleset enthält außer Pull-Request-Pflicht und Blockade von Löschung/Force-Push auch Code-Scanning- und Code-Quality-Regeln. Deren tatsächliche Verfügbarkeit im Repository wurde **nicht** nachgewiesen.
- Der verbundene GitHub-Zugang hat **keine Administration-Rechte**. Der Branch-Protection-Endpunkt liefert HTTP 403; die Konfiguration kann daher nicht durch den Assistenten aktiviert oder vollständig ausgelesen werden.

**Folgerung:** GitHub-PR-Checks allein verhindern direkte Pushes nach \`main\` nicht. Der Schutz muss durch den Repository-Administrator aktiviert und anschließend überprüft werden. Das vorhandene Ruleset nicht blind aktivieren, weil die zusätzlichen Scanning-Regeln unbeabsichtigt Merge-Blockaden auslösen können.

## Erforderliche einmalige GitHub-Konfiguration

Im Repository unter **Settings → Rules → Rulesets**:

1. Das bestehende Ruleset hinsichtlich Zielbranch und Scanning-Voraussetzungen prüfen oder ein neues, auf \`main\` begrenztes **Branch Ruleset** anlegen.
2. Zielbranch **\`main\`** auswählen (Standardbranch oder explizites Muster \`refs/heads/main\`); **Enforcement: Active**.
3. **Require a pull request before merging** aktivieren. Bei Einzelentwicklern kann die Zahl erforderlicher Reviews \`0\` betragen; die verpflichtenden Tests sind wichtiger.
4. **Require status checks to pass** aktivieren und den erfolgreichen CI-Check des Workflows \`tests\` / Jobs **\`regression-and-traceability\`** aus GitHub Actions auswählen. Gegebenenfalls „Require branches to be up to date before merging“ aktivieren.
5. Löschung und Force-Push von \`main\` unterbinden. Bypass-Ausnahmen nur nach dokumentierter Begründung zulassen.
6. Vor einer zusätzlichen CodeQL-/Code-Quality-Sperre prüfen, dass die entsprechenden Checks tatsächlich laufen; nicht einfach den deaktivierten Bestand unverändert einschalten.
7. Die Einstellung speichern und über einen Test-PR prüfen, ob ein fehlschlagender Check den Merge verhindert und ob ein direkter Push ohne zulässigen Bypass zurückgewiesen wird. Solange diese Prüfung aussteht, lautet der Zweigschutzstatus **nicht verifiziert**.

**Anmerkung:** Die in der GitHub-Oberfläche verfügbaren Regeln hängen vom Repository-/Organisationsplan und den Rechten des angemeldeten Administrators ab. Ziel ist der nachweislich erzwungene Schutz; eine bloß konfigurierte Regel ohne wirksame Durchsetzung reicht nicht.

## Kontrollierte Kriterien-Migration

Die zwei historischen Baselines bleiben grundsätzlich **unverändert**; die laufende Arbeit wird immer gegen den aktuellen Zielbranch geprüft. Neue/angepasste Kriterien werden in einem normalen Fach-PR geändert und mit neuen/geänderten Assertions belegt. Eine spätere notwendige Migration der historischen Baselines erfordert einen **separaten PR**, ausdrückliche fachliche Freigabe und Anpassung des CI-Sperrverfahrens. Kriterien dürfen nicht allein zur Umgehung des Gates gelöscht oder umnummeriert werden.

## Browser-E2E (separater Nachweis)

Die vorhandenen Python- und Code-Renderingtests ersetzen keine echten Interaktionen über einen Browser. Für automatisierte Browser-E2E-Tests wäre eine reproduzierbare, isolierte Streamlit-Instanz mit fiktiven Daten, festen Benutzerkonten, Browser-/Viewport-Konfiguration und stabilen Assertions erforderlich. Eine solche Infrastruktur ist **noch nicht** Bestandteil dieses Phase-3-Gate-PRs. Die vom Projektverantwortlichen gemeldeten manuellen Freigaben von US #10, #21, #22 und #24 bleiben als solche dokumentiert.

## Phase-3-Status

- **Implementiert:** Test-Assertion-Gate, bidirektionale Traceability, Schutz beider Baselines in Pull Requests, Regression.
- **Nur durch Repository-Administrator abschließbar:** verpflichtende PRs und statusbasierter Branchschutz auf \`main\`.
- **Optionaler Ausbau:** automatisierte Browser-End-to-End-Tests mit isolierter Testumgebung.
