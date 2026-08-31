# Syzeteo – Constraints, Non-functional Requirements, and Business Rules

Status: 31 August 2026

## 1. Constraints (RANF)

- [x] **RANF #01 – Preservation of Existing Data**  
  **Type:** Technical constraint / migration constraint  
  **Requirement:**  
  When Syzeteo is updated, all existing domain data must be preserved completely and consistently. Changes to the database schema may only be performed in a way that allows existing data to be migrated without loss and to continue to be used correctly.  
  **Rationale:**  
  Version changes must not cause the loss or unintended modification of previously recorded course, student, question, round, or game data. A course deletion explicitly initiated by the Instructor under GR #10 and deletion of a previously aborted game under GR #11 are not updates of Syzeteo and therefore do not fall under this migration constraint.

## 2. Non-functional Requirements (NFANF)

- [x] **NFANF #01 – No Individual Performance Evaluation**  
  **Type:** Privacy  
  **Requirement:**  
  Syzeteo must not collect, store, or evaluate individual performance data of students. Student names may be used exclusively for organizational purposes of gameplay, in particular for:
  - team assignment,
  - attendance,
  - start player selection,
  - regular player selection,
  - opponent selection,
  - selection for Team Assist.

  Points, statistics, scores, and evaluations may only be maintained at team or course level.  
  **Rationale:**  
  Syzeteo is intended for playful review of learning content, not for individual performance assessment or the creation of personal performance profiles.

- [x] **NFANF #02 – Round-related Data Integrity**  
  **Type:** Integrity / consistency  
  **Requirement:**  
  Completed game turns, point totals, and logged questions must not be changed retroactively by later changes to master data or by adding late arrivals. Complete deletion of a course explicitly initiated by the Instructor under GR #10 and deletion of a previously aborted game under GR #11 are exempt. Undoing the most recently executed game step as defined in US #20 is likewise a defined game operation and does not constitute an impermissible retroactive change within the meaning of this requirement.  
  **Rationale:**  
  The documented game progression must remain traceable and consistent for as long as the associated course exists. Deliberately initiated deletion operations under GR #10 and GR #11 and the defined undo operation under US #20 are domain-defined exceptions.

- [x] **NFANF #03 – Compact Game View**  
  **Type:** Usability  
  **Requirement:**  
  The game view should use compact landscape-format cards with clearly readable question text and should, during normal gameplay, be operable without vertical scrolling wherever possible.  
  **Rationale:**  
  The application is used in teaching and particularly in projector-based classroom situations. Essential game information should therefore be immediately visible without unnecessary navigation.

- [x] **NFANF #04 – Access Control**  
  **Type:** Security / access control  
  **Requirement:**  
  Syzeteo game and administration functions may only be accessible after successful authentication.  
  **Rationale:**  
  Unauthorized persons must not be able to view or modify game-related or administrative data.

## 3. Business and Game Rules (GR)

- [x] **GR #01 – Uniform Question Set**  
  **Type:** Business rule  
  **Rule:**  
  The same set of eight subject-matter questions must be used for a round in all courses. Card positions may vary between courses.  
  **Rationale:**  
  This ensures that all courses play the same round on the same subject-matter basis.

- [x] **GR #02 – Immutable Question Set**  
  **Type:** Domain integrity rule  
  **Rule:**  
  Once a round has been successfully started for the first time, the question set assigned to that round must no longer be changed. This includes both the assignment of the eight subject-matter questions and the question and model-answer text used in the round. Later changes to a question in the global Question Pool must not retroactively change rounds that have already been started or played.  
  **Rationale:**  
  This preserves comparability, traceability, and the Question Log across all courses. The technical implementation may, in particular, use immutable round-specific copies of the questions and model answers used.

- [x] **GR #03 – Fixed Round Size**  
  **Type:** Game rule  
  **Rule:**  
  Each round consists of exactly eight subject-matter questions and one automatically added **Challenge Card** as the ninth card.  
  **Rationale:**  
  The fixed size defines the mandatory structure of a round.

- [x] **GR #04 – Strict Team Alternation**  
  **Type:** Game rule  
  **Rule:**  
  After each regular player turn, the other team must take the next turn. The team alternation must not be overridden by the player selection method.  
  **Rationale:**  
  Strict alternation ensures balanced participation by both teams.

- [x] **GR #05 – Single Regular Turn per Person**  
  **Type:** Game rule  
  **Rule:**  
  A person who has already taken a regular turn in a round must not be selected again for another regular player turn in the same round. Participation exclusively through **Team Assist** does not count as a regular player turn and does not make that person ineligible for a later regular player turn.  
  **Rationale:**  
  This is intended to involve as many different students as possible in regular player turns within a round without restricting the special function of Team Assist.

- [x] **GR #06 – Team Assist Exception**  
  **Type:** Game exception rule  
  **Rule:**  
  The regular participation restriction does not apply when selecting a person through **Team Assist**. Any present member of the relevant team may be selected, even if that person has already taken a regular turn in the same round or has already participated through Team Assist.  
  **Rationale:**  
  Team Assist is intentionally defined as an exception to regular player selection.

- [x] **GR #07 – Last Card by Instructor**  
  **Type:** Game rule  
  **Rule:**  
  The last remaining card of a round is always revealed and answered by the **Instructor**. Regardless of its card type, it is not scored. No points are awarded for the last card.  
  **Rationale:**  
  This defines the established ending of a round. The last card is excluded from regular scoring regardless of whether it is a subject-matter question or the Challenge Card.

- [x] **GR #08 – Player Selection Mode Before Game Start**  
  **Type:** Game configuration rule  
  **Rule:**  
  The mode for regular player selection from player 2 onward is set before a game starts. The default is random player selection. Once the game has started, the mode must not be changed for that ongoing game.  
  **Rationale:**  
  The selection mode must remain stable during an ongoing game while preserving the defined default behavior of Syzeteo.

- [x] **GR #09 – Use a Round Once per Course**  
  **Type:** Business rule  
  **Rule:**  
  A round may be conducted regularly only once in a course. A game that has been aborted and deleted under GR #11 does not count as a regular conduct of the round; the round may then be started again for the respective course.  
  **Rationale:**  
  This prevents the same round with the same question set from being entered multiple times in a course's results and question history without permanently treating false starts or aborted games as regular conduct.

- [x] **GR #10 – Complete Course Deletion**  
  **Type:** Data rule  
  **Rule:**  
  When a course is deleted by the **Instructor**, all data associated with that course is deleted completely. This includes, in particular, the course's students and team assignments, attendance data, ongoing, aborted, and completed games, scores, round results, course-specific Question Logs, and any other data assigned exclusively to that course. Global cross-course data, in particular learning units and questions in the global Question Pool, is not deleted.  
  **Rationale:**  
  Course deletion is defined as a complete domain deletion operation. At the same time, global learning content that is not assigned exclusively to the deleted course is preserved.

- [x] **GR #11 – Abort and Delete Game**  
  **Type:** Game and data rule  
  **Rule:**  
  An ongoing game may be aborted by the **Instructor**. An aborted game is neither ongoing nor regularly completed and cannot be resumed. Aborted games are shown on the **Instructor page** and may be deleted there by the Instructor. Only aborted games may be deleted through this function; regularly completed games are excluded. Deleting an aborted game removes the game and all data assigned exclusively to that game. After deletion, the respective round is open again for the respective course and may be started again.  
  **Rationale:**  
  Games started by mistake or no longer to be continued must not block ongoing gameplay or a later regular conduct of the round. At the same time, regularly completed games and their history remain protected.
