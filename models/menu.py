response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
    ((IMG(_src=URL(c='static',f='icons/application_home.png')),T(' Index ')),URL('default','index')==URL(),URL('default','index'),[]),
    ((IMG(_src=URL(c='static',f='icons/page_add.png')),T(' Add Entry ')),URL('default','file_management_create')==URL(),URL('default','file_management_create'),[]),
    ((IMG(_src=URL(c='static',f='icons/page_go.png')),T(' View all ')),URL('default','file_management_select')==URL(),URL('default','file_management_select'),[]),
    ((IMG(_src=URL(c='static',f='icons/report_magnify.png')),T(' Search  ')),URL('default','file_management_search')==URL(),URL('default','file_management_search'),[]),
    #((IMG(_src=URL(c='static',f='icons/help.png')),T(' Help ')),URL('plugin_wiki','page/help')==URL(),URL('plugin_wiki','page/help'),[]),
   # ((IMG(_src=URL(c='static',f='icons/flag_green.png')),T(' Plan ')),URL('plan','plan')==URL(),URL('plan','plan'),[]),
    
]
