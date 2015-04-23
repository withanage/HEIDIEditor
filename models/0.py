from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Publications application'
settings.subtitle = 'Cluster Publication'
settings.author = 'Dulip withanage'
settings.author_email = 'withanage@asia-europe.uni-heidelberg.de'
settings.keywords = 'epub, TEI, XML'
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'postgres://publications:XrOyBlpt@localhost:5432/publications'
settings.security_key = '2674c3a8-8bdd-4f1c-8eb1-efb9ec41ac24'
settings.email_server = 'localhost'
settings.email_sender = 'withanage@asia-europe.uni-heidelberg.de'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
