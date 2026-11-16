# Spin The Wheel
**PM:** Matthew Chen  
**TNPG:** Spin The Wheel  
**Roster + Roles:**
- Matthew Chen – Project Manager, Scripter (`matthewc800@nycstudents.net`)
- Sakina Raza – CSS, Design Doc (`sakinar3@nycstudents.net`)
- Caroline Tham – Jinja/HTML, Scripter (`carolinet19@nycstudents.net`)
- Efaz Khan – Scribe, SQL (`efazk3@nycstudents.net`)

**TARGET SHIP DATE:** 2026-11-18  
[edit here](https://docs.google.com/document/d/1yczQzKKzc1LoORiNu3Q-ItPYmsryOb6guuZ96N7YXkU/edit?tab=t.0)

---

## Summary & Problem Being Solved
We are building a collaborative storytelling website where registered users start stories and add to each other's narratives, seeing only the latest update and adding to each story only once. Unlike traditional single-author stories, having each writer build strictly off the immediately preceding contribution pushes stories in unexpected directions while displaying the complete story on contributors' profile pages.

### Target Users
- Writers who want to participate in quick collaborative storytelling.
- Readers who enjoy narratives with unexpected twists and turns.

---

## Minimum Viable Product (MVP)

### Core Features
1. Register and log in using Flask sessions.
2. Start a new story with a title and opening text.
3. Browse stories you haven't contributed to and add to one, seeing only the latest update, once per story.
4. Profile page listing every story you've contributed to, with the full text readable.

### Stretch Features
1. Show contributor usernames in order for each story.
2. Sort or search through stories on `/browse`.
3. Custom styling via CSS while maintaining full functionality if CSS is stripped.

### Explicit Non-Goals
1. Editing or deleting a contribution that is already submitted.
2. Comments, likes, or following users/stories.
3. Password reset functionality.

---

## Technology Stack
| Layer | Selected Tool |
|---|---|
| Backend Framework | Flask |
| Frontend Framework | Jinja2 / HTML / CSS |
| Database | SQLite3 |
| Authentication | Flask Sessions |

---

## Team Ownership Plan
| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| **Matthew Chen** | Authentication, Story Management | CSS / Static | Register/login/logout with sessions; story rules (create story, latest update, once per story) |
| **Sakina Raza** | CSS, HTML Templates | Flask Server | HTML page templates; CSS stylesheets; `design.pdf` |
| **Caroline Tham** | Flask Server (`serve.py`) | Story Management, Database | All routes wired together; session checks on protected pages |
| **Efaz Khan** | SQL Database (`db.py`) | HTML Templates, Authentication | Create the 3 tables with constraints; helper functions for users, stories, contributions |

---

## Program Components & Site Map

### Backend & Route Components
- **`/` (Landing Page):** Welcome page with links/buttons to `/register` or `/login` (redirects to `/profile` if already logged in).
- **`/register`:** Registration form checking `users` table for unique username and matching passwords before inserting and redirecting to `/profile` or `/login`.
- **`/login`:** Login form verifying username and password against `users` table and establishing Flask session.
- **`/profile`:** Protected user dashboard listing all stories the user has contributed to with full text readable, plus navigation to `/new`, `/browse`, and `/logout`.
- **`/new`:** Protected form taking a story title and opening text; inserts into `stories` and adds the first row into `contributions`, then redirects to `/profile`.
- **`/browse`:** Protected view listing story titles the logged-in user has not yet contributed to, linking each to `/add/<story_id>`.
- **`/add/<story_id>`:** Protected view showing only the latest contribution (`highest contribution_id`) for the selected story; verifies user hasn't contributed yet, inserts new contribution on submit, and redirects to `/profile`.
- **`/logout`:** Clears Flask session (`session.clear()` / `session.pop()`) and redirects to `/`.

### Site Map Flow
- `/` $\rightarrow$ `/register` or `/login` $\rightarrow$ `/profile`
- `/profile` $\rightarrow$ `/new` $\rightarrow$ (submit) $\rightarrow$ `/profile`
- `/profile` $\rightarrow$ `/browse` $\rightarrow$ `/add/<story_id>` $\rightarrow$ (submit) $\rightarrow$ `/profile`
- `/profile` $\rightarrow$ `/logout` $\rightarrow$ `/`

---

## Database Organization (`storytelling.db`)

1. **`users`**
   - `user_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
   - `username` (`TEXT UNIQUE`)
   - `password` (`TEXT`)
2. **`stories`**
   - `story_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
   - `title` (`TEXT`)
   - `user_id` (`INTEGER`, Foreign Key $\rightarrow$ `users.user_id`)
3. **`contributions`**
   - `contribution_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
   - `story_id` (`INTEGER`, Foreign Key $\rightarrow$ `stories.story_id`)
   - `user_id` (`INTEGER`, Foreign Key $\rightarrow$ `users.user_id`)
   - `body` (`TEXT`)
   - *Note:* When a user creates a story, their opening text is immediately saved as the first row in `contributions` so the creator cannot contribute to their own story a second time.

---

## Testing Plan & Completion Criteria
- **Database:** All 3 tables initialize cleanly; duplicate usernames and duplicate `(story_id, user_id)` contributions are rejected; helper functions accurately fetch user IDs, stories, and latest contributions.
- **Authentication:** Valid registration/login establishes session; mismatched passwords or invalid credentials show clear error feedback; logged-out access to protected routes redirects to `/login`.
- **Story Management:** Creating a story populates both `stories` and `contributions`; `/add/<story_id>` displays only the most recent contribution; contributed stories disappear from `/browse` and appear in full on `/profile`; non-existent `story_id`s and empty submissions fail gracefully.
- **Templates & CSS:** Every route and form works properly both with `style.css` applied and with CSS completely stripped away.