from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from requests import session
from .models import Note, Piece, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/delete/<int:iduser>', methods=['GET', 'POST'])
@login_required
def delete(iduser):
    if current_user.id==1:
      user_to_delete=User.query.get(iduser)
      try:
          db.session.delete(user_to_delete)
          db.session.commit()
          flash("User deleted",category='success')
      except:       
          flash("Problem occured",category='error')
      return redirect(url_for('views.admin'))
    else:
      return redirect(url_for('views.home'))

@views.route('/desactivate/<iduser>', methods=['GET', 'POST'])
@login_required
def desactivate(iduser):
    if current_user.id==1:
       user=User.query.get(iduser)
       if user:
         user.active=False
         db.session.commit()
       return redirect(url_for('views.admin'))
    else:
      return redirect(url_for('views.home'))


    



@views.route('/verify/<iduser>', methods=['GET', 'POST'])
@login_required
def verify(iduser):
    if current_user.id==1:
       user=User.query.get(iduser)
       if user:
         user.active=True
         db.session.commit()
       return redirect(url_for('views.admin'))
    else:
       return redirect(url_for('views.home'))


    


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template("settings.html", user=current_user)


@views.route('/recognition', methods=['GET', 'POST'])
@login_required
def recognition():
    if current_user.active==False:
      flash('You account is not verified yet', category='error')
      return redirect(url_for('views.home'))

    else:
      return render_template("recognition.html", user=current_user)


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if(current_user.id==1):
        current_user.active=True
        db.session.commit()
        our_users=User.query.order_by(User.id)
            
        return render_template("admin.html", user=current_user,our_users=our_users)
    else:
      return redirect(url_for('views.home'))

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if current_user.active==False:
        flash("Your Account Is not Activated Yet",category='error')
        return redirect(url_for('views.home'))
    else:
     if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("note.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/change/<int:iduser>', methods=['GET', 'POST'])
@login_required
def change(iduser):
  user=User.query.get(iduser)
  if(current_user.id==1):
    if request.method == 'POST':
        npassword = request.form.get('npassword')
        #user.password=generate_password_hash(npassword, method='sha256')
        #db.session.commit()
        flash('Informations Are Updated successfully!', category='success')
        redirect(url_for('views.admin'))
    return render_template("change.html", user=current_user,our_user=user)
  else:
    return redirect(url_for('views.home'))

@views.route('/reserve',methods=['GET','POST'])
@login_required
def reserve():
  Piece=Piece.query.order_by(Piece.id)

  return render_template("reserve.html",Piece=Piece)