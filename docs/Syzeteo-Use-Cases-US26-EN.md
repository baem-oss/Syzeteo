# Syzeteo – Use Cases for US #26

Status: 31 August 2026

## Use Case: Abort Game

**Goal:**  
End an ongoing game without treating it as a regularly completed game.

**Precondition:**  
The Instructor is in an ongoing game.

**Successful Postcondition:**  
The game is aborted. It is neither ongoing nor regularly completed, cannot be resumed, and can subsequently be deleted.

**Failure Postcondition:**  
The game remains unchanged as an ongoing game.

**Actors:**  
Instructor

**Triggering Event:**  
The Instructor selects the “Abort Game” function.

**Description:**

1. Syzeteo asks the Instructor to confirm the abort.
2. The Instructor confirms the abort.
3. Syzeteo aborts the game.
4. Syzeteo confirms the successful abort and opens the Instructor page.

**Extensions:**

**2a. The Instructor does not confirm the abort.**  
2a1. Syzeteo closes the confirmation prompt and shows the ongoing game again.

**3a. Syzeteo cannot perform the abort.**  
3a1. Syzeteo informs the Instructor that the abort failed.  
3a2. Syzeteo shows the ongoing game again.

**Alternatives:**  
None.

---

## Use Case: Delete Game

**Goal:**  
Completely remove an aborted game so that the associated round can be conducted again for the respective course.

**Precondition:**  
The Instructor is on the Instructor page. At least one aborted game exists.

**Successful Postcondition:**  
The selected game and all data assigned exclusively to that game are deleted. The associated round is open again for the respective course.

**Failure Postcondition:**  
The selected game and all associated data remain unchanged.

**Actors:**  
Instructor

**Triggering Event:**  
The Instructor selects an aborted game for deletion.

**Description:**

1. Syzeteo shows the selected game and asks the Instructor to confirm the deletion.
2. The Instructor confirms the deletion.
3. Syzeteo deletes the selected game.
4. Syzeteo confirms the successful deletion to the Instructor.

**Extensions:**

**2a. The Instructor does not confirm the deletion.**  
2a1. Syzeteo closes the confirmation prompt and shows the Instructor page again.

**3a. Syzeteo cannot perform the deletion.**  
3a1. Syzeteo informs the Instructor that the deletion failed.  
3a2. Syzeteo shows the Instructor page again.

**Alternatives:**  
None.
