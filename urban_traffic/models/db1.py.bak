# -*- coding: utf-8 -*-
db.define_table('user_data',Field('latitude','float',requires=IS_NOT_EMPTY()),
                Field('longitude','float',requires=IS_NOT_EMPTY()),
                Field('time_stamp','string',requires=IS_NOT_EMPTY( ) ),
                  Field('dest','string',requires=IS_NOT_EMPTY( ) ))

db.define_table('details' , Field('name','string',requires =   IS_NOT_EMPTY()),
                Field ('email_id' , 'string' , requires =   IS_NOT_EMPTY()),
                Field ('destination' , 'string' , requires =   IS_NOT_EMPTY()),
                Field ('date_' , 'date' , requires =   IS_NOT_EMPTY()),
                Field ('slot' , 'integer' , requires =   IS_NOT_EMPTY() ) )

db.define_table('schedule' , Field('destination','string',requires =   IS_NOT_EMPTY()),
                Field('status','string',requires =   IS_NOT_EMPTY()),
                 Field ('date_' , 'date' , requires =   IS_NOT_EMPTY()),
                 Field ('people' , 'integer' , requires =   IS_NOT_EMPTY() ) ,
                Field ('slot' , 'integer' , requires =   IS_NOT_EMPTY() ) )
