def index():
    form=SQLFORM.factory(Field('date','date'),
                    Field('place','string',requires =IS_IN_DB( db, 'details.destination' ) ))
    if form.process().accepted:
        redirect(URL('schedule', vars=dict( a=form.vars.date, b = form.vars.place )  ))
        
    return locals()

def graph():
    destination = str(request.args[0])
    rows = db(db.user_data.dest==destination).select(orderby=db.user_data.time_stamp)
    data = list()
    for i in range(24):
        data.append([i,0])
    for row in rows:
        timestring = str(row.time_stamp)
        print timestring
        hour = int(timestring.split(':')[0])
        print "hour = " , hour
        data[hour][1] = data[hour][1] + 1
    
    return locals()
    
def recieve():
    import datetime
    import time
    time =  datetime.datetime.now().time()
    latitude = request.vars.latitude
    longitude = request.vars.longitude
    db.user_data.insert(latitude=latitude,longitude=longitude,time_stamp=time)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())




def graphs_time():
    
    
    
    return locals()
def graphs_place():
    return locals()

def schedule():
    vars = request.get_vars
    place = vars.b
    date = vars.a
    rows = db( db.schedule.destination == place and db.schedule.date_ == date    ).select()
    
    return locals()

def algo():
    vars = request.get_vars
    name_ = vars.name
    email_ = vars.email
    destination_ = vars.destination
    date1 = vars.date
    slot_ = vars.slot
    number_ = vars.number
    
    db.details.insert(name = name_, email_id=email_ , destination = destination_, date_ = date1 , slot = slot_ )
    
    
    rows1 = db(db.schedule.destination==destination_).select()
    if(len(rows1)==0):
        db.schedule.insert ( destination =destination_ ,status= 'pending',date_=date1 , people=0 , slot =slot_  )
        
        
    rows = db(db.schedule.destination == destination_ and db.schedule.date_==date1 and db.schedule.slot==slot_ ).select()
    for row in rows:
        if (row.status =='confirmed' and row.number + number_ <=30) :
            db(db.schedule.id == row.id ).update(people = people+number)
        elif (row.status == 'pending' and row.number + number_ >= 10):
            db(db.schedule.id == row.id).update(people = people+number )
            db(db.schedule.id == row.id).update(status ='confirmed' )
    db.schedule.insert ( destination =destination_ ,status= 'pending',date_=date1 , people=number_ , slot =slot_  )

    
    
    
    return locals()
