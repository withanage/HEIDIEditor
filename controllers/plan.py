# -*- coding: utf-8 -*-
### required - do no delete


@auth.requires_login()
def plan():
    
    return dict()

def new():
    form = SQLFORM.factory(db.contacts,db.groups)

    if form.accepts(request.vars):
        _id_user = db.contacts.insert(**db.contacts._filter_fields(form.vars))

        form.vars.contact = _id_user

        id = db.groups.insert(**db.groups._filter_fields(form.vars))

        response.flash = 'User registered successfully'
    return locals()

def update():
    id = request.args(0)

    group = db(db.groups.id == id).select()[0]

    form = SQLFORM(db.contacts, group.contact.id)
    group = SQLFORM(db.group, group.id)

    # Adding the group form
    form.append(group)

    if form.accepts(request.vars):

        # Updating the contacts
        db.contacts.update(**db.contacts._filter_fields(form.vars))

        # Atualizando o grupo
        old_group = db(db.groups.id == group.id).select().first()
        old_group.update_record(group=group.vars.group)

        response.session = 'Updated with success!'

    return locals()
