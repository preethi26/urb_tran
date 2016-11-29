import json
import datetime
def index():
    form=SQLFORM.factory(Field('date','date'),
                    Field('place','string',requires =IS_IN_SET(['Chennai' , 'Tirupathi','Nellore' ,'Gudur' , 'Sri Kalahasti'] ) ))
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
    print "**********"
    data=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],[12,0],]
    
    rows = db(db.schedule.id>0).select()
    for row in rows:
        data[row.slot][1] = data[row.slot][1] + row.people
        
        print data[row.slot]
    for i in range(1,12):
        a = data[i][1]
        a = str(a).strip('L')
        data[i][1] = int(a)
    return locals()


def graphs_place():
    print "$$$$$$$$$$$$$$"
    #dados_chart="[{name: 'Batata', y: },{name: 'Tomate', y: },{name: 'Mamão', y: }]" #Change this dynamically
    places = {}
    rows = db(db.schedule.id>0).select()
    for row in rows:
        a = row.people
        a = str(a).strip('L')
        row.people = int(a)
        if places.has_key(row.destination):
            places[row.destination] = places[row.destination] + row.people
        else:
            places.update({row.destination: row.people})
    
    temp = places.items()
    print temp
    dados_chart = ""
    
    # forming the dados chart in the required format
    for i in range(0,len(temp)):
        temp1 = {}
        temp1.update({ 'name' : temp[i][0]})
        print "a"
        temp1.update({ 'y' : temp[i][1]})
        temp1 = str(temp1)
        print temp1
        
        temp2 = temp1.split(',')
        a = temp2[0][2:3] + temp2[0][4:len(temp2[0])]
        b = temp2[1][2:6] + temp2[1][7:len(temp2[1])-1]
        
        temp1 = "{" + b + "," + " " + a + "}"
        
        
        dados_chart = dados_chart + temp1
    dados_chart = "[" + dados_chart + "]"
    print dados_chart

        
    
    dados_map={}
    dados_map["dados"]=dados_chart
    chart="""
    <script type="text/javascript">
    Highcharts.setOptions({
        lang:{
        downloadJPEG: "Download em imagem JPG",
        downloadPDF: "Download em documento PDF",
        downloadPNG: "Download em imagem PNG",
        downloadSVG: "Download em vetor SVG",
        loading: "Lendo...",
        noData: "Sem dados para mostrar",
        printChart: "Imprimir Gráfico",
        }
        });

            // Build the chart
            $('#chart').highcharts({
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Meu Gráfico'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        credits:{enabled:false},
        series: [{
            name: 'Vendar por porcentagem',
            colorByPoint: true,
                data: %(dados)s
                }]
            });
    </script>
    """ %dados_map
    return dict(chart=XML(chart))




def schedule():
    vars = request.get_vars
    place = vars.b
    date = vars.a
    rows = db( db.schedule.destination == place and db.schedule.date_ == date    ).select()
    data =[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],[12,0],]
    for row in rows:
        a = row.slot
        a = str(a).strip('L')
        row.slot = int(a)
        
        a = row.people
        a = str(a).strip('L')
        row.people = int(a)
        data[row.slot][1] = data[row.slot][1] + row.people
    rows1 = db(db.schedule.destination ==place and db.schedule.date_ == date ).select(orderby = db.schedule.slot)
    print data
    return locals()

def algo():
       
    
    name_ = request.args(0)
    number_ = request.args(1)
    email_ = request.args(2)

    date1 = request.args(3)
    slot_ = request.args(4)
    destination_ = request.args(5)
    
    slot_.replace("_",":")
    print "^^^^^^^^^",slot_

    slot_strip = slot_.split('-')[0]
    
    if slot_strip == '8_00AM':
        slot_ = 1
    if(slot_strip) == '9_00AM':
        slot_ = 1
    if(slot_strip) == '10_00AM':
        slot_ = 2
    if(slot_strip) == '11_00AM':
        slot_ = 3
    if(slot_strip) == '12_00PM':
        slot_ = 4
    if(slot_strip) == '1_00PM':
        slot_ = 5
    if(slot_strip) == '2_00PM':
        slot_ = 6
    if(slot_strip) == '3_00PM':
        slot_ = 7
    if(slot_strip) == '4_00PM':
        slot_ = 8
    if(slot_strip) == '5_00PM':
        slot_ = 9
    if(slot_strip) == '6_00PM':
        slot_ = 10
    if(slot_strip) == '7_00PM':
        slot_ = 11
    if(slot_strip) == '8_00PM':
        slot_ = 12
    
    date1 = date1.split('-')
    date1 = datetime.date(int(date1[0]), int(date1[1]),int(date1[2]))

   
    db.details.insert(name = name_, email_id=email_ , destination = destination_, date_ = date1 , slot = slot_ )

    rows1 = db(db.schedule.destination==destination_).select()
    if(len(rows1)==0):
        for i in range(1,12):
            db.schedule.insert ( destination =destination_ ,status= 'pending',date_=date1 , people=0 , slot = i  )
    flag = 10
    flag=0


    rows = db(db.schedule.destination == destination_ and db.schedule.date_==date1 and db.schedule.slot==slot_ ).select()


    if (flag==0):
        for row in rows :
        
            number_ = int(number_)
            if (row.status =='confirmed' and row.people + number_ <=30) :
                print "11111111111111"
                db(db.schedule.id == row.id ).update(people = row.people+number_)
                string = "your request has been processed successfully. you can board the bus in slot:" + str(slot_) + "to" + str(destination_)
                flag=1
                break




    if flag==0:
        for row in rows :
            number_ = int(number_)

            if (row.status == 'pending' ):
                print "222222222222222222"
                if (row.people + number_ < 10):
                    db(db.schedule.id == row.id).update(people = row.people+number_ )
                    string = "your request has been processed successfully. you can board the bus in slot:" + str(slot_) + "to" + str(destination_) + "but the bus still needs " + str(10 - row.people + number_) + "people to get confirmed"
                if (row.people + number_ >= 10):
                    db(db.schedule.id == row.id).update(status ='confirmed' )
                    db(db.schedule.id == row.id).update(people = row.people+number_ )
                    string = "your request has been processed successfully. you can board the bus in slot:" + str(slot_) + "to" + str(destination_)
                flag=1
                break




    if flag==0:
        for row in rows :
            number_ = int(number_)    
            if(row.status =='confirmed' and row.people + number_ >30):
                print "333333333333333"
                if (number_ < 10):
                    db.schedule.insert ( destination =destination_ ,status= 'pending',date_=date1 , people=number_ , slot =slot_  )
                    string = "your request has been processed successfully. you can board the bus in slot:" + str(slot_) + "to" + str(destination_) + "but the bus still needs " + str(30 - row.people + number_) + "people to get confirmed"
                else :
                    db.schedule.insert ( destination =destination_ ,status= 'confirmed',date_=date1 , people=number_ , slot =slot_  )
                    string = "your request has been processed successfully. you can board the bus in slot:" + str(slot_) + "to" + str(destination_)
                flag=1
                break




    return locals()
