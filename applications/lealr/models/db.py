# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## connect to Google BigTable (optional 'google:datastore://namespace')
db = DAL('google:datastore')
## store sessions and tickets there
session.connect(request, response, db=db)
## or store session in Memcache, Redis, etc.
## from gluon.contrib.memdb import MEMDB
## from google.appengine.api.memcache import Client
## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=True)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

##database

################################
####thread######################
################################ 
db.define_table('thread',
    Field('user_id','string', readable=False, writable=False),
    Field('title','string', length=120),
    Field('url_title', readable=False, writable=False),
    Field('thread_content','text'),
    Field('collection_name_array','list:string'),
)

################################
####thread_like#################
################################ 
db.define_table('thread_like',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('user_ip','string', readable=False, writable=False),
    Field('thread_id','string', readable=False, writable=False),
    Field('vote_location', 'string'),
)

################################
####thread_dislike##############
################################ 
db.define_table('thread_dislike',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('user_ip','string', readable=False, writable=False),
    Field('thread_id','string', readable=False, writable=False),
    Field('vote_location', 'string'),
)

################################
####thread_comment##############
################################ 
db.define_table('thread_comment',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('thread_id','reference thread', readable=False, writable=False),
    Field('parent_comment_id','string', readable=False, writable=False),
    Field('collection_comment','string', readable=False, writable=False),
    Field('comment_content','string'),
)

################################
####thread_tag##################
################################ 
db.define_table('thread_tag',
    Field('thread_id','reference thread'),
    Field('tag','string'),
    Field('user_id','string'),
)

################################
####collection##################
################################ 
db.define_table('collection',
    Field('title','string', unique=True, length=120),
    Field('description','string'),
    Field('creator_id','string', default=auth.user_id, readable=False, writable=False),
)

################################
####collection_picture##########
################################ 
db.define_table('collection_picture',
    Field('collection_id', 'reference collection', readable=False, writable=False),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
    
)

################################
####collection_tag##############
################################ 
db.define_table('collection_tag',
    Field('collection_id','string'),
    Field('tag','string'),
    Field('user_id','string'),

)

################################
####collection_member###########
################################
db.define_table('collection_member',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('collection_id','reference collection'),
    Field('collection_membergroup_id_array','list:string'),
)

################################
####collection_membergroup########
################################
db.define_table('collection_membergroup',
    Field('collection_id','integer'),
    Field('title','string'),
    Field('description','string'),
)

################################
####collection_membergroup_permissions
################################
db.define_table('collection_membergroup_permissions',
    Field('collection_id','reference collection'),
    Field('collection_membergroup_id','reference collection_membergroup'),
    Field('permissions','string'),
)

################################
####collection_style############
################################
db.define_table('collection_style',
    Field('collection_id','reference collection'),
    Field('title','string'),
    Field('description','string'),
    Field('collection_style','string')
)

         
################################
####member_avatar###############
################################
db.define_table('member_avatar',
    Field('user_id', 'string'),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)

################################
####message_thread##############
################################
db.define_table('message_thread',
    Field('title','string', length=120),
    Field('message_content','text'),
    Field('user_id_array','list:string'),
)

################################
####message_comment#############
################################
db.define_table('message_comment',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('message_thread_id','reference thread', readable=False, writable=False),
    Field('message_content','text'),
    Field('collection_name_array','list:string'),
)

################################
####follower####################
################################
db.define_table('follower',
    Field('user_following_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('user_followed_id','reference auth_user', readable=False, writable=False)
)

################################
####feed_post###################
################################
db.define_table('feed_post',
    Field('user_id', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('user_feed_id','reference auth_user', readable=False, writable=False),
    Field('post_content','text'),
    
)

    
db.auth_user.first_name.readable = db.auth_user.first_name.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False 

auth.enable_record_versioning(db)
