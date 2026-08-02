# SIH Matchmaker Platform

A full-stack role-based portal for the Smart India Hackathon (SIH) allowing students to form teams, and college admins to shortlist them.

## Tech Stack
- **Frontend**: Vanilla HTML/CSS/JS (MPA Architecture) with a custom Glassmorphism/Neon design system.
- **Backend**: FastAPI, SQLModel, Alembic, PostgreSQL.
- **Auth**: Secure JWT HttpOnly Cookies.

## Local Setup

### 1. Database
Your project is pre-configured to connect to your Supabase project **`SIH-Management-Portal-V2`**.
Open the `backend/.env` file and replace `[YOUR_DATABASE_PASSWORD]` with your actual Supabase database password.

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Generate the initial database migration script based on your Postgres DB
alembic revision --autogenerate -m "Initial Schema"

# Apply the tables to the database
alembic upgrade head

# Start the server
uvicorn main:app --reload --port 8000
```

### 3. Frontend
Use Live Server (VSCode extension) or Python's HTTP Server:
```bash
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000` in your browser. Ensure `js/api.js` `API_URL` points to `http://localhost:8000/api/v1`.

### 4. Super Admin Setup
By design, Super Admin registration is disabled for security.
You must manually seed a Super Admin in your PostgreSQL `users` table:
```sql
INSERT INTO "user" (id, email, hashed_password, name, role, is_active) 
VALUES (gen_random_uuid(), 'super@admin.com', '$2b$12$YourHashedPasswordHere', 'Super Admin', 'SuperAdmin', true);
```
*(Generate a bcrypt hash for the password manually using Python's `passlib` or an online generator).*

## Deployment Guidelines

### Frontend (Vercel)
1. Push the repository to GitHub.
2. Import the project into Vercel.
3. Set the **Root Directory** to `frontend`.
4. Deploy. (Note your new Vercel URL).
5. Update `js/api.js` to point `API_URL` to your live Render backend URL.

### Backend (Render)
1. The project includes a `render.yaml` file for easy deployment via Render Blueprint.
2. Connect your GitHub repository in Render.
3. It will automatically detect `render.yaml` and provision a Web Service pointing to the `backend/` directory.
4. **Important**: Under your Render Environment variables, set `CORS_ORIGINS` to your Vercel frontend URL so cookies are permitted across origins. Set your production `DATABASE_URL`.
