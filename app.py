import logging
import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from supabase import Client, create_client
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
logging.basicConfig(level=logging.INFO)
def get_supabase() -> Client:
    """Create the Supabase client using credentials from .env."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_secret_key = os.getenv("SUPABASE_SECRET_KEY")
    if not supabase_url or not supabase_secret_key:
        raise RuntimeError(
            "Supabase credentials are missing. Add SUPABASE_URL and "
            "SUPABASE_SECRET_KEY to your .env file."
        )
    return create_client(supabase_url, supabase_secret_key)
def database_ready(view_function):
    """Show a friendly message if the Supabase connection is not configured."""
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        try:
            get_supabase()
        except Exception as error:
            app.logger.error("Supabase configuration error: %s", error)
            flash(str(error), "error")
            return render_template("index.html", notes=[], setup_error=True)
        return view_function(*args, **kwargs)

    return wrapper
@app.route("/")
@database_ready
def index():
    try:
        response = (
            get_supabase()
            .table("notes")
            .select("id, title, content, created_at, updated_at")
            .order("updated_at", desc=True)
            .execute()
        )
        notes = response.data or []
        return render_template("index.html", notes=notes, setup_error=False)
    except Exception:
        app.logger.exception("Could not load notes")
        flash("Could not load your notes. Check your Supabase table and connection.", "error")
        return render_template("index.html", notes=[], setup_error=False)
@app.route("/create", methods=["POST"])
@database_ready
def create_note():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title:
        flash("Please enter a title for your note.", "error")
        return redirect(url_for("index"))

    try:
        get_supabase().table("notes").insert({
            "title": title,
            "content": content,
        }).execute()
        flash("Your note was created.", "success")
    except Exception:
        app.logger.exception("Could not create note")
        flash("Could not create the note. Please check your Supabase setup.", "error")

    return redirect(url_for("index"))


@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
@database_ready
def edit_note(note_id):
    supabase = get_supabase()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title:
            flash("The note title cannot be empty.", "error")
            return redirect(url_for("edit_note", note_id=note_id))

        try:
            response = (
                supabase.table("notes")
                .update({"title": title, "content": content})
                .eq("id", note_id)
                .execute()
            )
            if not response.data:
                return abort(404)
            flash("Your changes were saved.", "success")
            return redirect(url_for("index"))
        except Exception:
            app.logger.exception("Could not update note %s", note_id)
            flash("Could not update the note. Please try again.", "error")
            return redirect(url_for("edit_note", note_id=note_id))

    try:
        response = (
            supabase.table("notes")
            .select("id, title, content, created_at, updated_at")
            .eq("id", note_id)
            .execute()
        )
        if not response.data:
            abort(404)
        return render_template("edit.html", note=response.data[0])
    except Exception:
        app.logger.exception("Could not find note %s", note_id)
        abort(404)


@app.route("/delete/<int:note_id>", methods=["POST"])
@database_ready
def delete_note(note_id):
    try:
        get_supabase().table("notes").delete().eq("id", note_id).execute()
        flash("Your note was deleted.", "success")
    except Exception:
        app.logger.exception("Could not delete note %s", note_id)
        flash("Could not delete the note. Please try again.", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    # For local development only. Do not use Flask's debug server in production.
    app.run(debug=True)
