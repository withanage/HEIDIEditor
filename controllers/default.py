# -*- coding: utf-8 -*-
### required - do no delete
#import oxgarage

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
def index():
    return dict()

def error():
    return dict()

def typesetter(upload_file_name):
	metypeset_conversion(upload_file_name)
	row = db(db.t_file_management.f_original_document==upload_file_name).select().first()
	row.update(f_tei_xml_file=upload_file_name.rsplit('.', 1)[0]+'_tei.xml', f_nlm_xml_file=upload_file_name.rsplit('.', 1)[0]+'_nlm.xml')
	row.update_record() 

@auth.requires_login()
def file_management_create():
    upload_file_name = None
    form=crud.create(db.t_file_management)
    if form.accepts(request,session):
        upload_file_name = form.vars.f_original_document
        if request.vars.f_original_document!=None:
            form.vars.f_original_filename = request.vars.f_original_document.filename
            crud.settings.create_onaccept = typesetter(upload_file_name)
            redirect(URL('file_management_select'))
        #result=oxgrarage_conversion(upload_file_name)
    return dict(form=form,result= db(db.t_file_management.f_original_document==upload_file_name).select().first())

@auth.requires_login()
def file_management_read():
    record = db.t_file_management(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_file_management,record)
    return dict(form=form)

@auth.requires_login()
def file_management_update():
    record = db.t_file_management(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_file_management,record,next='file_management_read/[id]',
                     ondelete=lambda form: redirect(URL('file_management_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_login()
def file_management_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_file_management[f]==v or db.t_file_management
    except: redirect(URL('error'))
    rows=db(query)(db.t_file_management.active==True).select(db.t_file_management.id,db.t_file_management.f_filename,db.t_file_management.f_original_document,\
    db.t_file_management.f_tei_xml_file, db.t_file_management.f_nlm_xml_file, db.t_file_management.f_xhtml_file, db.t_file_management.f_pdf_file,\
    db.t_file_management.modified_on,db.t_file_management.modified_by, orderby=~db.t_file_management.modified_on)
    return dict(rows=rows)

@auth.requires_login()
def file_management_search():
    form, rows=crud.search(db.t_file_management,query=db.t_file_management.active==True)
    return dict(form=form, rows=rows)

def enterkey_create():
    result='not ok'
    form=crud.create(db.t_enter_key)
    if form.accepts(request,session):
        response.flash=("done")

    return dict(form=form, result=result)
