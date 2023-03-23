from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, current_user
from .models import Entry
from .forms import EntryForm, UpdateProfileForm
from . import db
from .utils import save_picture, amount_conversion

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/profile")
@login_required
def profile():
    total_entries = len(Entry.query.filter_by(user_id=current_user.id).all())
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "profile.html",
        title="Profile",
        total_entries=total_entries,
        profile_pic=image_file,
    )


@views.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("views.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "update_profile.html", title="Update profile", form=form, profile_pic=image_file
    )


@views.route("/entries")
@login_required
def entries():
    page = request.args.get("page", 1, type=int)
    all_entries = (
        Entry.query.filter_by(user_id=current_user.id)
        .order_by(Entry.date_added.desc())
        .paginate(page=page, per_page=5)
    )
    entries_for_balance = Entry.query.filter_by(user_id=current_user.id).all()
    balance = round(
        sum([round(entry.amount / 100, 2) for entry in entries_for_balance]), 2
    )
    return render_template("entries.html", all_entries=all_entries, balance=balance)


@views.route("/new_entry", methods=["GET", "POST"])
@login_required
def new_entry():
    form = EntryForm()
    if form.validate_on_submit():
        form.amount.data = amount_conversion(form.amount.data, form.entry_type.data)
        new_entry = Entry(amount=form.amount.data, user_id=current_user.id)
        db.session.add(new_entry)
        db.session.commit()
        flash(f"Added {form.entry_type.data} entry.", "success")
        return redirect(url_for("views.entries"))
    return render_template("new_entry.html", form=form)


@views.route("/update_entry/<int:entry_id>", methods=["GET", "POST"])
@login_required
def update_entry(entry_id):
    entry = Entry.query.get(entry_id)
    entry.amount = amount_conversion(entry.amount)
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        form.amount.data = amount_conversion(form.amount.data, form.entry_type.data)
        form.populate_obj(entry)
        db.session.commit()
        return redirect(url_for("views.entries"))
    return render_template("update_entry.html", form=form)


@views.route("/delete_entry/<int:entry_id>", methods=["GET", "POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("views.entries"))


@views.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@views.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@views.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500
