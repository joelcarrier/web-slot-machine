# -*- coding: utf-8 -*-

def index():
    redirect(URL(c='default',f='play'))

def play():

    # redirect to login if no user in session
    if not session.user:
      redirect(URL(c='default',f='login'))

    # same if the session contains a user that no longer appears valid
    user = db.user[session.user.id]
    if not user:
      redirect(URL(c='default',f='login'))

    credits = user.credits
    return dict(credits=credits)

def spin():
    import random
    user = db.user[session.user.id]

    #following will be used in the view
    credits = 0 #will contain user credits after spin
    delta = 0 #will contain winnings if any
    #default slots to black (only remain black if no credit)
    slot_one_color = slot_two_color = slot_three_color = '#000'

    #check balance before accepting a credit
    credits = user.credits
    if credits < 1:
        #user is broke
        #won't spin
        pass
    else:
       #user can afford to play
       user.update_record(credits = user.credits - 1) #take a credit from user
       slot_one = random.randint(1,3) #spin!
       slot_two = random.randint(1,3) #spin!
       slot_three = random.randint(1,3) #spin!
       delta = 0 
       if slot_one == slot_two == slot_three:
         delta = slot_one * 4 
         user.update_record(credits=user.credits+delta)
       credits = user.credits
       #map slot values to colors
       color_map = {}
       color_map[1] = '#3A87AD'
       color_map[2] = '#F89406'
       color_map[3] = '#B94A48'

       slot_one_color=color_map[slot_one]
       slot_two_color=color_map[slot_two]
       slot_three_color=color_map[slot_three]

    return dict(
            slot_one_color=slot_one_color,
            slot_two_color=slot_two_color,
            slot_three_color=slot_three_color,
            credits=credits,
            delta=delta
            ) 

def credits():
    import time
    time.sleep(5)
    user = db.user[session.user.id]
    return user.credits
 
def evict_user():
    username = None
    if session.user:
      user = db.user[session.user.id]
      username = user.username
      db(db.user.id == session.user.id).delete()
      session.user = None
    return dict(username=username)

def login():
    login_form = FORM()
    login_form.append(INPUT(_id='username',_name='username',_style="width:250px;height:30px;"))
    if login_form.process().accepted:
        username = login_form.vars.username
        db.user.update_or_insert(username=username)
        session.user = db(db.user.username==username).select().first()
        session.flash = "Welcome " + username
        redirect(URL(c='default',f='index'))
    else:
        session.flash = "Please enter a username to start or resume a game."
    return dict(login_form=login_form)
        
def logout():
    session.user = None
    redirect(URL(c='default',f='login'))

