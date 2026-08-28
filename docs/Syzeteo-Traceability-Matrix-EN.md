# Syzeteo – Traceability Matrix

Status: 27 August 2026

Source basis: `Syzeteo-L-US-EN.md` and `Syzeteo-RANF-etc-EN.md`

## 1. Review Principle

The matrix contains only relationships that are substantively or normatively well-founded. Purely technical or merely indirect dependencies are not represented as trace links.

Cross-cutting requirements are listed separately where repeating them in almost every table row would reduce the explanatory value of the matrix.

In particular:

- RANF #01 is a global migration constraint for all persistent domain data.
- NFANF #04 applies to all game and administration functions. US #05 provides the authentication entry point.
- NFANF #02 protects existing game and log data against unintended retroactive changes. Complete course deletion under GR #10 and the domain-defined undo operation under US #20 are explicitly excluded from this restriction.

## 2. Traceability Matrix: User Stories → Requirements

| **US** | User Story | Business/Game Rules | Non-functional Requirements | Explanation |
|---|---|---|---|---|
| **US #01** | Change Start Player | GR #04, GR #05 | NFANF #01 | The actual start player is subsequently subject to strict team alternation and the restriction against repeated regular turns. Use of the person's name for start player selection is permitted under NFANF #01. |
| **US #02** | Set Player Selection Mode | GR #04, GR #05, GR #08 | NFANF #01 | GR #08 governs timing, default value, and immutability of the mode. Team alternation and the regular participation restriction apply regardless of the selection mode. |
| **US #03** | Add Late Arrivals | GR #05, GR #06 | NFANF #01, NFANF #02 | Late arrivals are added to the pool of persons available for subsequent participation. Completed game turns must not be changed retroactively as a result. |
| **US #04** | Central Instructor Settings | GR #08 | – | The player selection mode is a game-relevant setting. Access control follows cross-cutting NFANF #04. |
| **US #05** | Sign In to the System | – | NFANF #04 | Sign-in is the direct mechanism for enforcing access control. |
| **US #06** | Manage Own Account | – | – | Access control follows cross-cutting NFANF #04. |
| **US #07** | Manage Courses | GR #10 | NFANF #02 | GR #10 defines complete deletion of all course-related data. NFANF #02 distinguishes this deliberate deletion operation from impermissible retroactive changes to master data. |
| **US #08** | Manage Students | – | NFANF #01, NFANF #02 | Student names may only be used for organizational purposes. Changes to the student population must not retroactively change historical game data. |
| **US #09** | Import Students | – | NFANF #01, NFANF #02 | The import creates organizational person data but no individual performance data. An import must not retroactively change historical game data. |
| **US #10** | Assign Students to Teams | – | NFANF #01, NFANF #02 | Team assignment is an explicitly permitted organizational purpose. Later team changes must not retroactively change historical game data. |
| **US #11** | Set Attendance | GR #05, GR #06 | NFANF #01 | Attendance determines the eligible population. GR #05 applies to regular turns; the exception under GR #06 applies to Team Assist. |
| **US #12** | Manage Learning Units | – | NFANF #02 | Changes to domain master data must not retroactively change already documented game progressions. |
| **US #13** | Manage Question Pool | GR #02 | NFANF #02 | Changes to the global Question Pool must not retroactively change rounds that have already been started or played. |
| **US #14** | Import and Export Learning Content | – | NFANF #02 | Imported changes to learning content must not retroactively change historical game and log data. |
| **US #15** | Configure Rounds | GR #01, GR #02, GR #03 | – | Round configuration uses eight subject-matter questions, the same question set across courses, and becomes immutable after the first successful start. |
| **US #16** | Start Game | GR #01, GR #02, GR #03, GR #08, GR #09 | NFANF #01 | Starting the game activates the question set, round structure, player selection mode, and the rule that a round is used only once per course. Personal data may only be processed for organizational purposes. |
| **US #17** | Conduct and Score Questions | GR #03, GR #04, GR #05, GR #07 | NFANF #01, NFANF #03 | Core regular gameplay: card structure, team alternation, single regular turn per person, and special handling of the last card. Points remain team-based. |
| **US #18** | Use Team Assist | GR #05, GR #06 | NFANF #01 | Team Assist participation is subject to the exception from the regular participation restriction and does not itself make a person ineligible for a later regular player turn. |
| **US #19** | Score Challenge Card | GR #03, GR #07 | NFANF #01 | The Challenge Card is the ninth card and is scored according to its special scoring logic unless it is the last remaining card. If it is last, it is answered by the Instructor and not scored under GR #07. |
| **US #20** | Undo Game Step | GR #04, GR #05, GR #06 | – | Undo must restore the previous domain-consistent game state. NFANF #02 explicitly clarifies that this defined game operation is not an impermissible retroactive change. |
| **US #21** | Resume Ongoing Game | GR #04, GR #05, GR #06, GR #07, GR #08, GR #09 | NFANF #02 | On resumption, the saved game state, participation status, player selection mode, and round identity must remain consistent. |
| **US #22** | Use Projector Mode | – | NFANF #03 | Projector Mode directly supports the compact and clearly readable game view. |
| **US #23** | Review Results | GR #09 | NFANF #01, NFANF #02 | The dashboard may show only team- and course-level evaluations and must rely on consistent historical game data. |
| **US #24** | Log Played Questions | GR #01, GR #02, GR #09 | NFANF #02 | The log must preserve a traceable record of the question set actually played per round and course for as long as the course has not been deleted under GR #10. |
| **US #25** | Check Round Coverage | GR #09 | NFANF #02 | The states open, ongoing, or played require unique use of a round per course and consistent stored data. |

## 3. Cross-cutting Requirements

### 3.1 RANF #01 – Preservation of Existing Data

RANF #01 applies to all persistent domain data when Syzeteo is updated. This includes in particular:

- courses,
- students,
- team assignments,
- learning units,
- questions,
- rounds,
- ongoing and completed games,
- scores,
- result data,
- Question Logs.

An explicitly initiated course deletion under GR #10 is not a system update and therefore does not conflict with RANF #01.

### 3.2 NFANF #04 – Access Control

NFANF #04 applies across the system:

- US #05 provides the authentication mechanism.
- US #01 through US #04 and US #06 through US #25 describe game or administration functions and may only be accessible after successful authentication.

## 4. Reverse Traceability: Requirements → User Stories

### 4.1 Business and Game Rules

| **Requirement** | Covered by User Stories |
|---|---|
| **GR #01 – Uniform Question Set** | US #15, US #16, US #24 |
| **GR #02 – Immutable Question Set** | US #13, US #15, US #16, US #24 |
| **GR #03 – Fixed Round Size** | US #15, US #16, US #17, US #19 |
| **GR #04 – Strict Team Alternation** | US #01, US #02, US #17, US #20, US #21 |
| **GR #05 – Single Regular Turn per Person** | US #01, US #02, US #03, US #11, US #17, US #18, US #20, US #21 |
| **GR #06 – Team Assist Exception** | US #03, US #11, US #18, US #20, US #21 |
| **GR #07 – Last Card by Instructor** | US #17, US #19, US #21 |
| **GR #08 – Player Selection Mode Before Game Start** | US #02, US #04, US #16, US #21 |
| **GR #09 – Use a Round Once per Course** | US #16, US #21, US #23, US #24, US #25 |
| **GR #10 – Complete Course Deletion** | US #07 |

### 4.2 Non-functional Requirements

| **Requirement** | Covered by User Stories |
|---|---|
| **NFANF #01 – No Individual Performance Evaluation** | US #01, US #02, US #03, US #08, US #09, US #10, US #11, US #16, US #17, US #18, US #19, US #23 |
| **NFANF #02 – Round-related Data Integrity** | US #03, US #07, US #08, US #09, US #10, US #12, US #13, US #14, US #21, US #23, US #24, US #25 |
| **NFANF #03 – Compact Game View** | US #17, US #22 |
| **NFANF #04 – Access Control** | US #05 as the authentication mechanism; US #01–US #04 and US #06–US #25 as protected game and administration functions |

### 4.3 Constraint

| **Requirement** | Scope |
|---|---|
| **RANF #01 – Preservation of Existing Data** | Global migration constraint for all persistent domain data present during a system update |

## 5. Completeness and Consistency Review

The consolidated requirements baseline contains:

- 25 User Stories
- 10 business and game rules
- 4 non-functional requirements
- 1 constraint

All 25 User Stories are included in the matrix.

All 10 business and game rules have at least one traceable link.

All 4 non-functional requirements are covered.

RANF #01 is included as a global cross-cutting requirement.

The previously open clarifications are resolved as follows:

1. Course deletion: complete deletion of all course-related data under US #07 and GR #10; global learning content is preserved.
2. Changes to questions: rounds that have already been started or played remain unchanged, including question and model-answer text, under GR #02.
3. Undo: explicitly permitted game operation under US #20 and NFANF #02.
4. Team Assist: participation exclusively through Team Assist does not make a person ineligible for a later regular player turn under GR #05 and GR #06.
5. Last card: the last remaining card is answered by the Instructor and not scored regardless of card type; no points are awarded under GR #07.

Result: Based on the consolidated documents, no identifiable domain contradictions or orphaned requirements remain.
