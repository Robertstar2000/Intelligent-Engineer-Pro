# Checking Book Project Status in Hermes

When needing to verify the existence or status of a book project (e.g., "Tomorrow Remembered"), use the following steps:

1. Search for files or content matching the project title (case-insensitive):
   ```bash
   search_files pattern="(?i)Tomorrow Remembered" target=files
   search_files pattern="(?i)Tomorrow Remembered" target=content
   ```

2. Check common book directories:
   - `~/books/`
   - `~/book-sources/`
   - `~/projects/`
   - `~/hermes/books/`

3. If not found, consider:
   - The project may be in a different Hermes profile.
   - The project may not yet be started or files may be named differently.
   - Consult any project specification or outline documents (e.g., SPECIFICATION.md) for hints.

4. For broader discovery, list recent sessions to see if work was done on the project:
   ```bash
   session_search query="Tomorrow Remembered" limit=5
   ```

5. If still unclear, ask the user for the exact path or alternative titles.