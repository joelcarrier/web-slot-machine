# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite')

response.generic_patterns = ['*'] #if request.is_local else []

db.define_table('user',
    Field('id','id'),
    Field('username',unique=True),
    Field('credits','integer',default=20)
)


