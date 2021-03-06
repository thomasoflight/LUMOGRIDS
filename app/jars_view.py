import time
from flask import render_template, redirect, url_for
from app import lumo_hub
from app.card_model import Card
from app.card_step_data_collect import get_incmplts_tuple
from app.forms import TodoButtonsImproved
from itertools import zip_longest

template_card = Card.objects.get(card_name="...")

@lumo_hub.route('/jars/<string:jar_from_url>/', methods=['GET', 'POST'])
def jars_view(jar_from_url):


    def get_jar_positions(position):
        if Card.objects(card_in_jar=jar_from_url,
                        card_active=position):

            found_active = Card.objects(card_in_jar=jar_from_url,
                                        card_active=position).get()
            return found_active

        else:
            return template_card

    jar_name = jar_from_url

    tl = get_jar_positions('top_left')
    tm = get_jar_positions('top_mid')
    tr = get_jar_positions('top_right')
    ml = get_jar_positions('mid_left')
    mr = get_jar_positions('mid_right')
    bl = get_jar_positions('botm_left')
    bm = get_jar_positions('botm_mid')
    br = get_jar_positions('botm_right')

    jar_positions = {
        'tl': tl,
        'tm': tm,
        'tr': tr,
        'ml': ml,
        'mr': mr,
        'bl': bl,
        'bm': bm,
        'br': br
        }

    form = TodoButtonsImproved()
    subforms = [f for f in form if f.type == 'FormField']

    for subform, card in zip_longest(subforms, jar_positions.values()):
        idx = 0
        for chk in subform:
            chk.id, chk.label = get_incmplts_tuple(card)[idx]
            idx += 1


    if form.validate_on_submit():
        subforms = [f for f in form if f.type == "FormField"]

        for s_f in subforms:
            card = jar_positions[s_f.name[:2]]

            for chk in s_f:
                n = chk.id

                if chk.data and n >= 0:
                    card.card_steps[n].step_status = 1

            card.save()

        return redirect(url_for('jars_view', jar_from_url=jar_from_url))

    return render_template('jars.html',
                           jar_name=jar_name,
                           jar_positions=jar_positions,
                           form=form)
