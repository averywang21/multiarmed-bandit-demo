from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flaskblog import db
from flask_login import current_user, login_required
from flaskblog.models import Machine, User
from sqlalchemy import desc
from scipy.stats import beta
import random


trials = Blueprint('trials', __name__)
random.seed(137)

@trials.route("/trial")
@login_required
def show_trial():
    confidence_level = float(request.args.get('ci', default=0.95))
    last_action = int(request.args.get('last_action', default=-1))
    last_action_success = (request.args.get('last_action_success', default="False") == "True")
    game_number = int(request.args.get('game_number', default=0))
    machines = Machine.query.filter_by(user_id=current_user.id, game_number=game_number).all()
    if len(machines) == 0:
        abort(403)
    total_success, total_attempts = 0, 0
    confidence_intervals = {}
    for machine in machines:
        total_success += machine.success_count
        total_attempts += machine.total_count
        if machine.total_count == 0:
            confidence_intervals[machine] = (0, 1)
        else:
            confidence_intervals[machine] = beta.ppf([(1-confidence_level)/2, 1-(1-confidence_level)/2], 
                                            machine.success_count+1,
                                            machine.total_count - machine.success_count+1)
        max_attempts = machine.max_attempts
    return render_template('trial.html', machines=machines, 
                                        total_success=total_success, 
                                        total_attempts=total_attempts,
                                        total_attempts_allowed=max_attempts,
                                        ci=confidence_level,
                                        last_action=last_action,
                                        last_action_success=last_action_success,
                                        confidence_intervals=confidence_intervals,
                                        game_number=game_number)

@trials.route("/trial/<int:pull_machine>")
@login_required
def pull_machine_trial(pull_machine):
    confidence_level = float(request.args.get('ci', default=0.95))
    game_number = int(request.args.get('game_number', default=0))
    pulled_machine = Machine.query.filter_by(user_id=current_user.id, game_number=game_number, machine_number=pull_machine).first()
    if random.random() < pulled_machine.true_prob:
        pulled_machine.success_count += 1
        last_action_success = True
    else:
        last_action_success = False
    pulled_machine.total_count += 1
    
    db.session.commit()
    return redirect(url_for("trials.show_trial", ci=confidence_level, last_action=pulled_machine.machine_number, last_action_success = last_action_success, game_number=game_number))

@trials.route("/trial/reset")
@login_required
def machine_reset():
    confidence_level = float(request.args.get('ci', default=0.95))
    machines = Machine.query.filter_by(user_id=current_user.id, game_number=0).all()
    for machine in machines:
        machine.success_count = 0
        machine.total_count = 0
        machine.lower_ci = 0
        machine.upper_ci = 1
    db.session.commit()
    return redirect(url_for("trials.show_trial", ci=confidence_level))

@trials.route("/results")
def show_results():
    scores = db.session.query(Machine, \
            db.func.sum(Machine.success_count).label("success_count"), \
                db.func.sum(Machine.total_count), User)\
                .filter_by(game_number=0)\
                .join(User)\
                .group_by(Machine.user_id).order_by(desc("success_count")).all()

    return render_template("results.html", scores=scores)

