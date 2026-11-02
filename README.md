# Papertrail — Flask + Supabase Notepad

A beginner-friendly notepad web app built with Python Flask, HTML, CSS, and Supabase PostgreSQL. It supports all four CRUD operations:

- **Create:** add a note with a title and content.
- **Read:** view all saved notes, newest/most recently edited first.
- **Update:** edit an existing note.
- **Delete:** remove a note after a confirmation prompt.

## 1. Project files

```text
flask_supabase_notepad/
│
├── app.py                 # Flask routes and Supabase database operations
├── .env                   # Your private Supabase URL/key (do not share or upload)
├── .env.example           # Example environment-variable file
├── .gitignore             # Keeps .env and virtual environment out of Git
├── requirements.txt       # Python packages
├── supabase_schema.sql    # SQL to create the notes table
├── README.md              # Setup instructions
│
├── templates/
│   ├── base.html          # Shared page layout
│   ├── index.html         # Create and display notes
│   └── edit.html          # Update an existing note
│
└── static/
    └── style.css          # Front-end styling
```

## 2. Create your Supabase project

1. Open [https://supabase.com](https://supabase.com) and sign in.
2. Create a new project and wait for the database to finish setting up.
3. In your project, open **SQL Editor**.
4. Open the `supabase_schema.sql` file from this project, copy all its SQL, paste it into the SQL Editor, and click **Run**.
5. Confirm that a table named `notes` appears in **Table Editor**.

The SQL enables Row Level Security (RLS). This app uses a Supabase **secret key** from the Flask backend, so no public RLS policy is required for this local, single-user example. The SQL grants the `service_role` access needed by the backend client.

## 3. Add your Supabase credentials

In the Supabase Dashboard, open your project's **Connect** panel to copy the Project URL. Open **Settings → API Keys** to find your **secret key** (usually starts with `sb_secret_`).

Open the `.env` file in this project and replace the example values:

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_SECRET_KEY=sb_secret_your_actual_secret_key
FLASK_SECRET_KEY=put-a-long-random-secret-here
```

Keep the variable names exactly as shown. Do not put quotation marks around the values unless they are part of the value.

**Important:** The Supabase secret key has elevated access and bypasses Row Level Security. Keep it only in `.env` on a computer/server you control. Never paste it into HTML, CSS, JavaScript, a public GitHub repository, or a browser. The supplied `.gitignore` excludes `.env` from Git.

## 4. Create a Python virtual environment

Open a terminal inside the `flask_supabase_notepad` project folder.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

The `.venv` folder stores your project's installed Python packages. It is different from the `.env` file, which stores your secret configuration values.

## 5. Install the required packages

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run the application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

You can now create, view, edit, and delete notes. Your notes are stored in the Supabase `notes` table, not in a local file.

## 7. Common problems

### `Supabase credentials are missing`

Make sure the `.env` file is in the same folder as `app.py`. Check that `SUPABASE_URL` and `SUPABASE_SECRET_KEY` are filled in and spelled exactly as shown.

### `Invalid API key` or `401 Unauthorized`

Check that you copied the **secret key**, not the project reference or Project URL. Do not add spaces before or after the key.

### `relation "notes" does not exist`

Run `supabase_schema.sql` in the Supabase SQL Editor and confirm the `notes` table exists in the `public` schema.

### Permission or database API errors

Confirm that the Data API is enabled for your project and that the SQL grants in `supabase_schema.sql` have been applied. If your project's API settings restrict exposed schemas, make sure `public` is exposed.

## Security note

This is a local learning project and does not include user login. Anyone who can reach the running Flask app can create, view, edit, or delete notes in its connected database. Do not deploy it as a public website in this form. Before public deployment, add authentication and per-user database authorization, use HTTPS, set a strong `FLASK_SECRET_KEY`, and run behind a production WSGI server instead of Flask's debug server.
