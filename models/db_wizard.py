########################################
db.define_table('t_file_management',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('',(IMG(_src=URL(c='static',f='icons/page_edit.png'))),_href=URL('file_management_read',args=id))),
           label=T('Entry'),
          ),
    Field('f_filename', type='string',
          label=T('File Name')),
    Field('f_original_document', type='upload', notnull=True, 
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/page_white_word.png'))),_href=URL('download',args=x)) or '',
          label=T('Original')),
    Field('f_original_filename', readable=False, writable=False),
    Field('f_tei_xml_file', type='upload', notnull=False,
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/page_white_code.png'))),_href=URL('download',args=x)) or '',
          label=T('Tei XML'), readable=False, writable=False),
    Field('f_nlm_xml_file', type='upload', notnull=False,
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/page_white_code.png'))),_href=URL('download',args=x)) or '',
          label=T('NLM XML'), readable=False, writable=False),
    Field('f_xhtml_file', type='upload',
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/xhtml.png'))),_href=URL('download',args=x)) or '',
          label=T('XHTML'), readable=False, writable=False),
    Field('f_pdf_file', type='upload',
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/page_white_acrobat.png'))),_href=URL('download',args=x)) or '',
          label=T('Pdf '), readable=False, writable=False),
    Field('f_epub_file', type='upload',
          represent=lambda x: x and A((IMG(_src=URL(c='static',f='icons/page_white_swoosh.png'))),_href=URL('download',args=x)) or '',
          label=T('Epub'), readable=False, writable=False),
    Field('f_comment', type='text',
          label=T('Comment')),
    Field('active','boolean',default=True,
          label=T('Active'),writable=False,readable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified on'),writable=False,readable=False,
          update=request.now),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False),
    Field('modified_by',db.auth_user,default=auth.user_id,
          label=T('Modified by'),writable=False,readable=False,
          update=auth.user_id),
    format='%(f_original_document)s',
    migrate=settings.migrate)

db.define_table('t_file_management_archive',db.t_file_management,Field('current_record','reference t_file_management'))

db.define_table('t_enter_key',
    Field('f_filevalue', type='double'),
    Field('f_filename', type='string', notnull=True),
    Field('f_filevalue2', type='double'),
    Field('f_filevalue3', type='double'),
    migrate=True
)
db.t_enter_key.f_filename.requires=IS_IN_SET(['a','b'])

contacts= db.define_table('contacts',
    Field('name'),Field('email')
  )

group = db.define_table('groups',
    Field('contact',db.contacts, readable=False,writable=False),
    
  )
db.groups.contact.requires=IS_IN_DB(db,db.contacts.id)
