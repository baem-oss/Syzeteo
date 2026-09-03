# Syzeteo – Use Cases for US #26

Status: 3 September 2026

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
4. Syzeteo confirms the successful abort to the Instructor.
5. Syzeteo opens the Instructor page.

**Extensions:**  
None.

**Alternatives:**

**2a. The Instructor cancels the abort.**  
2a1. Syzeteo closes the confirmation prompt.  
2a2. Syzeteo shows the ongoing game to the Instructor again.

**3a. Syzeteo cannot abort the ongoing game.**  
3a1. Syzeteo informs the Instructor that the abort failed.  
3a2. Syzeteo shows the ongoing game to the Instructor again.

---

## Use Case: Delete Game

**Goal:**  
Delete an aborted game so that the associated round can be conducted again for the respective course.

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

1. Syzeteo shows the selected game to the Instructor.
2. Syzeteo asks the Instructor to confirm the deletion.
3. The Instructor confirms the deletion.
4. Syzeteo deletes the selected game.
5. Syzeteo confirms the successful deletion to the Instructor.

**Extensions:**  
None.

**Alternatives:**

**3a. The Instructor cancels the deletion.**  
3a1. Syzeteo closes the confirmation prompt.  
3a2. Syzeteo shows the Instructor page to the Instructor again.

**4a. Syzeteo cannot delete the selected game.**  
4a1. Syzeteo informs the Instructor that the deletion failed.  
4a2. Syzeteo shows the Instructor page to the Instructor again.
