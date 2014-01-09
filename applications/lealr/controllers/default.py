################################################################
####controllers#################################################
################################################################

################################
####about#######################
################################
def about():
    return dict()
    
################################
####account#####################
################################
def account():             
    test='' 
    return dict(
    test=test
    )
    
################################
####collection##################
################################ 
def collection():
    if request.args(0) is None:
        redirect(URL('/collections'))
    if "." in request.args(0):
        collection_members=''
        form_create_usergroup=''
        collection_by_url = request.args(0).split(".")
        collection_by_url_array = []
        for collection in collection_by_url:
            collection_by_url_array.append(db(db.collection.title.replace(" ","-")==collection).select()[0])
        collection_thread_list = []
        for collection in collection_by_url_array:
            collection_thread_list.append(db(db.thread.collection_name_array.contains(collection['title'])).select())
        complete_collection_thread_list = []
        for thread_list in collection_thread_list:
            for thread in thread_list:
                complete_collection_thread_list.append(thread['url_title'])
        set_collection_thread_list = []    
        for title in set(complete_collection_thread_list):
            set_collection_thread_list.append(db(db.thread.url_title == title).select()[0])
    else:
        collection_members=''
        form_create_usergroup=''
        set_collection_thread_list = db(db.thread.collection_name_array.contains(request.args(0))).select()
        if request.args(1) == 'members':
            collection_members = db(db.collection_member.collection_id==collection_by_url_array[0]['id']).select()
        if request.args(1) == 'moderation':
            collection_members=''
        if request.args(1) == 'notices':
            collection_members=''
        if request.args(1) == 'styles':
            collection_members=''
        if request.args(1) == 'usergroups':
            collection_members=''
            form_create_usergroup = SQLFORM(db.collection_usergroup)

    return dict(
    form_create_usergroup=form_create_usergroup,
    collection_members=collection_members,
    set_collection_thread_list=set_collection_thread_list
    )
         
################################
####collections#################
################################  
def collections():
    form_create_collection = SQLFORM(db.collection)   
    #to-do, pagnation, sorting
    collection_list = db(db.collection).select()   
    if form_create_collection.process(formname='form_create_collection').accepted:           
        if session.tag_collection is not '':           
            collection_tag_array = session.collection_tag.split(',')        
            for a_tag in collection_tag_array:
                db.collection_tag.insert(collection_id = form_create_collection.vars.id, tag = a_tag)        
        session.flash = 'Collection Created'
        redirect(URL('/collections/' + str(form_create_collection.vars.title.replace(" ","-"))))
    elif form_create_collection.errors:
        session.flash = 'Error'   
        redirect(URL(''))
    collection_tag_list = db(db.collection_tag).select()
    collection_tag_list_array = []
    for tag in collection_tag_list:
        collection_tag_list_array.append(tag['tag'])               
    set_collection_tag_list = set(collection_tag_list_array)
    tag_collection_list_unsorted = list(set_collection_tag_list)
    combined_count_and_tag_array=[]
    for tag in tag_collection_list_unsorted:
        combined_count_and_tag_array.append([tag, collection_tag_list_array.count(tag)])
    from operator import itemgetter
    tag_collection_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))               
    promoted_thread_array = db(db.thread.collection_name_array.contains('promotion')).select()

    return dict(
    tag_collection_list_sorted_by_total_count=tag_collection_list_sorted_by_total_count,
    form_create_collection=form_create_collection,
    collection_list=collection_list,
    collection_tag_list=collection_tag_list,
    promoted_thread_array=promoted_thread_array,
    )
    
################################
####discover####################
################################
def discover():
    promoted_thread_array = db(db.thread.collection_name_array.contains('promotion')).select()
    return dict(
    promoted_thread_array=promoted_thread_array,
    ) 
      
################################
####faq#########################
################################     
def faq():
    return dict()
     
################################
####feed########################
################################
def feed():
    test=''
    promoted_thread_array = db(db.thread.collection_name_array.contains('promotion')).select() 
    return dict(
    test=test,
    promoted_thread_array=promoted_thread_array,
    )
       
################################
####inbox#######################
################################
def inbox():
    form_create_message = SQLFORM(db.message_thread)
    if form_create_message.process(formname='form_create_message').accepted: 
        session.flash = 'posted'
        redirect(URL('/inbox/' + form_create_message.vars.id))
    elif form_create_message.errors:
        session.flash = 'Error'   
        redirect(URL(''))         
    return dict(
    form_create_message=form_create_message
    )
          
################################
####index#######################
################################
def index():
    form_create_thread = SQLFORM(db.thread, onvalidation=validate_create_thread)
    if form_create_thread.process(formname='form_create_thread').accepted:
        thread_url = str(form_create_thread.vars.title.replace(" ","-")) + '.' + str(form_create_thread.vars.id)
        db(db.thread.id==form_create_thread.vars.id).update(url_title=thread_url)
        collection_list = session.collection_thread.split(',')
        db(db.thread.id==form_create_thread.vars.id).update(collection_name_array=collection_list)
        if session.tag_thread is not '':
            thread_tag_array = session.tag_thread.split(',')
            for a_tag in thread_tag_array:
                db.thread_tag.insert(thread_id = form_create_thread.vars.id, tag = a_tag)
        session.flash = "Thread Created"
        redirect(URL('/thread/' + str(thread_url)))
    elif form_create_thread.errors:
        session.flash = 'Error'   
        redirect(URL(''))
    form_create_collection = SQLFORM(db.collection)
    if form_create_collection.process(formname='form_create_collection').accepted:
        if session.tag_collection is not '':            
            collection_tag_array = session.collection_tag.split(',')            
            for a_tag in collection_tag_array:
                db.collection_tag.insert(collection_id = form_create_collection.vars.id, tag = a_tag)
        #add collection member
        db.collection_member.insert(collection_id = form_create_collection.vars.id, user_id = auth.user_id, collection_usergroup_id=0)
        session.flash = 'Collection Created'
        redirect(URL('/collection/' + str(form_create_collection.vars.title.replace(" ","-"))))
            
    elif form_create_collection.errors:
        session.flash = 'Error'   
        redirect(URL(''))
    collection_list = db(db.collection).select()    
    thread_tag_list = db(db.thread_tag).select()
    thread_tag_list_tag_array = []
    for tag in thread_tag_list:
        thread_tag_list_tag_array.append(tag['tag'])
    set_thread_tag_list = set(thread_tag_list_tag_array)
    tag_thread_list_unsorted = list(set_thread_tag_list)
    combined_count_and_tag_array=[]
    for tag in tag_thread_list_unsorted:
        combined_count_and_tag_array.append([tag, thread_tag_list_tag_array.count(tag)])
    from operator import itemgetter
    tag_thread_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))            
    complete_thread_list = db(db.thread).select()
    thread_like_array = []
    thread_dislike_array = []
    for thread in complete_thread_list:
        thread_like_array.append(db(db.thread_like.thread_id == thread['id']).select())
        thread_dislike_array.append(db(db.thread_dislike.thread_id == thread['id']).select())   
    promoted_thread_array = db(db.thread.collection_name_array.contains('promotion')).select()

    return dict(
    promoted_thread_array=promoted_thread_array,
    tag_thread_list_sorted_by_total_count=tag_thread_list_sorted_by_total_count,
    thread_like_array=thread_like_array,
    thread_dislike_array=thread_dislike_array,
    tag_thread_list_unsorted=tag_thread_list_unsorted,
    thread_tag_list_tag_array=thread_tag_list_tag_array,
    set_thread_tag_list=set_thread_tag_list,
    collection_list=collection_list,
    complete_thread_list=complete_thread_list,
    form_create_collection=form_create_collection,
    form_create_thread = form_create_thread
    )
    
################################
####member######################
################################
def member(): 
    form_create_avatar=''
    form_edit_avatar=''
    user_avatar=''
    if auth.user is not None:
        if auth.user.username == request.args(0):
            user_avatar = db(db.user_avatar.user_id==auth.user_id).select()
            if user_avatar == '':
                form_create_avatar = SQLFORM(db.user_avatar)
                form_edit_avatar=''
            else:
                #form_edit_avatar = SQLFORM(db.user_avatar, user_avatar[0]['id'])
                form_create_avatar=''
    id_from_username = db(db.auth_user.username == request.args(0)).select()[0]['id']
    user_content_threads = db(db.thread.user_id==id_from_username).select()
    user_followers = db(db.follower.user_followed_id==id_from_username).select()
    user_following = db(db.follower.user_following_id==id_from_username).select()
    user_collections = db(db.collection_member.user_id==id_from_username).select()
    user_feed = db(db.feed_post.user_feed_id == id_from_username).select()
    form_create_feed_post = SQLFORM(db.feed_post)
    if form_create_feed_post.process(formname='form_create_feed_post').accepted: 
        db(db.feed_post.id==form_create_feed_post.vars.id).update(user_id=auth.user_id)
        db(db.feed_post.id==form_create_feed_post.vars.id).update(user_feed_id=id_from_username)
        session.flash = 'posted'
        redirect(URL('/member/' + request.args(0)))
    elif form_create_feed_post.errors:
        session.flash = 'Error'   
        redirect(URL(''))
    
    return dict(
    user_feed=user_feed,
    form_create_feed_post=form_create_feed_post,
    user_followers=user_followers,
    user_following=user_following,
    user_collections=user_collections,    
    id_from_username=id_from_username,
    user_content_threads=user_content_threads,
    user_avatar=user_avatar,
    form_create_avatar=form_create_avatar,
    form_edit_avatar=form_edit_avatar,
    ) 
    

################################
####members#####################
################################
def members():
    test=''   
    return dict(
    test=test
    ) 
    
################################
####messages####################
################################ 
def messages():
    return dict()      
              
################################
####mycollections###############
################################
def mycollections():
    my_admin_collections = db(db.collection.creator_id == auth.user_id).select()  
    my_memberships = db(db.collection_member.user_id == auth.user_id).select()
    my_collections=[]
    #to do, user_groups..
    for member in my_memberships:
        my_collections.append(db(db.collection.id == member['collection_id']).select())
    return dict(
    my_admin_collections=my_admin_collections,
    my_collections=my_collections,
    )
    
################################
####notifications###############
################################
def notifications():
    return dict()   
             
################################
####promoted####################
################################
def promoted():
    ##get promoted threads
    #get a random one
    test=''
    return dict(
    test=test
    )
 
################################
####privacy#####################
################################ 
def privacy():
    return dict() 
    
################################
####search######################
################################
def search():
    return dict() 
     
################################
####service#####################
################################ 
def service():
    return dict()
                  
################################
####terms#######################
################################           
def terms():
    return dict()      
    
################################
####thread######################
################################    
def thread():
    thread_by_url = db(db.thread.url_title == request.args(0)).select()    
    thread_tag = db(db.thread_tag.thread_id == thread_by_url[0]['id']).select()
    form_create_comment_root = SQLFORM(db.thread_comment)
    if form_create_comment_root.process(formname='form_create_comment_root').accepted:    
        db(db.thread_comment.id==form_create_comment_root.vars.id).update(user_id=auth.user_id)
        db(db.thread_comment.id==form_create_comment_root.vars.id).update(thread_id=thread_by_url[0]['id'])
        db(db.thread_comment.id==form_create_comment_root.vars.id).update(parent_comment_id='null') 
        session.flash = 'Commented'
        redirect(URL('/thread/' + request.args(0)))       
    elif form_create_comment_root.errors:
        session.flash = 'Error'   
        redirect(URL(''))
     
    create_comment_with_id_dict = dict()  
    thread_comments = db(db.thread_comment.thread_id == thread_by_url[0]['id']).select()
    for comment in thread_comments:  
        create_comment_with_id_dict[comment['id']] = SQLFORM(db.thread_comment)
        if create_comment_with_id_dict[comment['id']].process(formname='create_comment_with_id_dict' + str(comment['id'])).accepted:  
            db(db.thread_comment.id==form_create_comment_root.vars.id).update(user_id=auth.user_id)
            db(db.thread_comment.id==form_create_comment_root.vars.id).update(thread_id=thread_by_url[0]['id'])
            db(db.thread_comment.id==form_create_comment_root.vars.id).update(parent_comment_id=comment['id'])
            session.flash = 'Commented'
            redirect(URL('/thread/' + request.args(0)))
                
        elif create_comment_with_id_dict[comment['id']].errors:
            session.flash = 'Error'   
            redirect(URL(''))
        
    return dict(
    create_comment_with_id_dict=create_comment_with_id_dict,
    form_create_comment_root=form_create_comment_root,
    thread_by_url=thread_by_url,
    thread_tag=thread_tag,
    )
     
################################
####transparency################
################################ 
def transparency():
    return dict()
                      
################################################################
####services####################################################
################################################################
                                                                                                                       
@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()

@auth.requires_signature()
def data():
    return dict(form=crud())

################################################################
####form_validation#############################################
################################################################

def validate_create_thread():
    return dict()  

################################################################
####url_helpers#################################################
################################################################

def c():
    return collection()
def m():
    return member()
    
################################################################
####ajax########################################################
################################################################

################################
####ajax_like_thread############
################################ 
def ajax_like_thread(): 
    thread_id = request.vars.itervalues()
    for x in thread_id:
        thread_id_trim = int(x)
    db.thread_like.insert(thread_id = thread_id_trim, vote_location = str(request.args(1)), user_ip=request.env.http_host, user_id=auth.user_id)     
    #check if already disliked
    thread_dislike = db((db.thread_dislike.thread_id == thread_id_trim) & (db.thread_dislike.user_id == auth.user_id)).select()
    #update score
    #thread_likes = len(db(db.thread_dislike.thread_id == thread_id_trim).select())
    #thread_dislikes = len(db(db.thread_dislike.thread_id == thread_id_trim).select())
    #like_dislike_difference = thread_likes - thread_dislikes
    jquery=''
    if not thread_dislike:
        hi=''
    else:
        jquery += "$('#thread-item-disliked-%s').fadeToggle(100);" % thread_id_trim
        jquery += "$('#thread-item-dislike-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-item-like-%s').fadeToggle(100);" % thread_id_trim
    jquery += "$('#thread-item-liked-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-%s-score').text('+1');" % thread_id_trim
    jquery += "$('#thread-%s-score').css('color', 'rgb(100,140,100)');" % thread_id_trim

    return jquery
 
################################
####ajax_un_like_thread#########
################################        
def ajax_un_like_thread():
    thread_id = request.vars.itervalues()
    for x in thread_id:
        thread_id_trim = int(x)
    thread_like_id = db((db.thread_like.thread_id == thread_id_trim) & (db.thread_like.user_id == auth.user_id)).select()[0]['id']    
    db(db.thread_like.id == thread_like_id).delete()
    jquery = "$('#thread-item-liked-%s').fadeToggle(100);" % thread_id_trim
    jquery += "$('#thread-item-like-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-%s-score').text('0');" % thread_id_trim
    return jquery
    
################################
####ajax_dislike_thread#########
################################     
def ajax_dislike_thread():
    thread_id = request.vars.itervalues()
    for x in thread_id:
        thread_id_trim = int(x)
    db.thread_dislike.insert(thread_id = thread_id_trim, vote_location = str(request.args(1)), user_ip=request.env.http_host, user_id=auth.user_id)
    #check if already liked
    thread_like = db((db.thread_like.thread_id == thread_id_trim) & (db.thread_like.user_id == auth.user_id)).select()             
    jquery=''
    if not thread_like:
        hi=''
    else:
        jquery += "$('#thread-item-liked-%s').fadeToggle(100);" % thread_id_trim
        jquery += "$('#thread-item-like-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-item-dislike-%s').fadeToggle(100);" % thread_id_trim
    jquery += "$('#thread-item-disliked-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-%s-score').text('-1');" % thread_id_trim
    jquery += "$('#thread-%s-score').css('color', 'rgb(100,80,100)');" % thread_id_trim
    return jquery
 
################################
####ajax_un_dislike_thread######
################################        
def ajax_un_dislike_thread():
    thread_id = request.vars.itervalues()
    for x in thread_id:
        thread_id_trim = int(x)
    thread_dislike_id = db((db.thread_dislike.thread_id == thread_id_trim) & (db.thread_dislike.user_id == auth.user_id)).select()[0]['id']    
    db(db.thread_dislike.id == thread_dislike_id).delete()
         
    jquery = "$('#thread-item-disliked-%s').fadeToggle(100);" % thread_id_trim
    jquery += "$('#thread-item-dislike-%s').delay(100).fadeToggle(400);" % thread_id_trim
    jquery += "$('#thread-%s-score').text('0');" % thread_id_trim
    return jquery    

################################
####ajax_join_collection########
################################                     
def ajax_join_collection():
    collection_id = request.vars.itervalues()
    for x in collection_id:
        collection_id_trim = int(x)
        
    #LOGIC
    db.collection_member.insert(user_id = auth.user_id, collection_id = collection_id_trim, collection_usergroup_id=1)
    jquery = "jQuery('.flash').html('joined').slideDown().delay(1000).slideUp();"
    jquery += "$('#join-collection-%s').fadeToggle(100);" % collection_id_trim
    jquery += "$('#leave-collection-%s').delay(100).fadeToggle(400);" % collection_id_trim   
    return jquery      
    
################################
####ajax_leave_collection#######
################################     
def ajax_leave_collection():
    collection_id = request.vars.itervalues()
    for x in collection_id:
        collection_id_trim = int(x)
    #LOGIC
    db((db.collection_member.user_id==auth.user_id) & (db.collection_member.collection_id==collection_id_trim)).delete()
    jquery = "jQuery('.flash').html('left').slideDown().delay(1000).slideUp();"
    jquery += "$('#leave-collection-%s').fadeToggle(100);" % collection_id_trim
    jquery += "$('#join-collection-%s').delay(100).fadeToggle(400);" % collection_id_trim   
    return jquery
       
################################
####ajax_follow_member##########
################################                                         
def ajax_follow_member():
    member_id = request.vars.itervalues()
    for x in member_id:
        member_id_trim = int(x) 
    #LOGIC
    db.follower.insert(user_following_id = auth.user_id, user_followed_id = member_id_trim)
    jquery = "jQuery('.flash').html('following').slideDown().delay(1000).slideUp();"
    jquery += "$('#follow').fadeToggle(100);"
    jquery += "$('#unfollow').delay(100).fadeToggle(100);"
    return jquery
    
################################
####ajax_un_follow_member#######
################################ 
def ajax_un_follow_member():
    member_id = request.vars.itervalues()
    for x in member_id:
        member_id_trim = int(x)  
    db((db.follower.user_following_id==auth.user_id) & (db.follower.user_followed_id==member_id_trim)).delete()
    jquery = "jQuery('.flash').html('unfollowed').slideDown().delay(1000).slideUp();"
    jquery += "$('#unfollow').fadeToggle(100);"
    jquery += "$('#follow').delay(100).fadeToggle(100);"
    return jquery
              
################################
####ajax_autocomplete_thread_tag
################################              
def ajax_autocomplete_thread_tag():
    return dict()
    
################################
####ajax_autocomplete_thread_collection
################################     
def ajax_autocomplete_thread_collection():
    return dict()   
    
################################
####ajax_autocomplete_collections_tag
################################ 
def ajax_autocomplete_collections_tag():
    return dict()

################################
####ajax_add_tag_sidebar########
################################         
def ajax_add_tag_sidebar():
    tags = request.vars.sidebar_add_tag
    session.tags = tags 
    test1 = DIV(tags, XML('<b>world</b>'), _id=0, _class='well')
    jquery = "jQuery('#thread-list').html('%s');" % test1
    jquery += "jQuery('#tag-list').html('%s');" % test1
    return jquery
           
################################
####ajax_add_collection_sidebar#
################################                         
def ajax_add_collection_sidebar():
    collections = request.vars.sidebar_add_collection
    session.collections_sidebar = collections   
    collection_list = session.collections_sidebar.split(',')
    collection_thread_list = []         
    for collection in collection_list:
        collection_thread_list.append(db(db.thread.collection_name_array.contains(collection)).select())

    complete_collection_thread_list = []
    for thread_list in collection_thread_list:
        for thread in thread_list:
            complete_collection_thread_list.append(thread['url_title'])
            
    set_collection_thread_list = []    
    for title in set(complete_collection_thread_list):
        set_collection_thread_list.append(db(db.thread.url_title == title).select()[0])
    if not set_collection_thread_list:
        set_collection_thread_list = db(db.thread).select()
    
    title_array = [] 
    collections_thread_array = [] 
    the_collections_thread_array = []
    for count, thread in enumerate(set_collection_thread_list):
        title_array.append(
            TABLE(
                   TR(
                       TD(
                       A(
                       IMG( _src='/lealr/static/images/lealrlogo.png' ,_class='img-polaroid', _style='height:48px;'), _href='/thread/' + thread['url_title'], _style='float:left;')
                       ,_style='padding-left:15px;padding-top:5px;'),
                       TD(
                           DIV(
                                DIV(H5(A(thread['title'], _style='margin-top:15px;margin-left:15px;', _href='/thread/' + thread['url_title']),_style='display:inline-block') ,_style='float:left;'),
                                DIV('by', A('user_name', _style='margin-left:5px;'),_style='float:left;margin-left:5px;margin-top:10px'),
                                DIV(A('x comments', _style='margin-left:15px;margin-top:10px'), _id='thread-views'),
                                DIV(A('x views', _style='margin-left:15px;margin-top:10px;'), _id='thread-views')
                            
                            )
                            ,_style='width:100%'
                        ),
                        TD( 
                            H5(
                                A('like', _style='margin-left:15px;'),
                                A('dislike', _style='margin-left:15px;'),
                                A('score', _style='margin-left:15px;'),_style='margin-right:15px;'
                            ),
                            H5(A('share'), _style='float:right;margin-right:15px;')
                        )
                    ),
                    TR(TD(H5(A('collections')+A('tags'))))
               ,_style='table-layout: fixed;')
           )
        collections_thread_array.append(thread['collection_name_array'])
        for collection in collections_thread_array[count]:
            the_collections_thread_array.append(collection)    
    test = BR() + HR()
    test1 = DIV()
    for title in title_array:
        test += DIV(title, XML(''), _id='thread-list-item', style='width:100%') + HR()
    for collection in set(the_collections_thread_array):
        test1 += DIV(A(collection, _href='/collection/'+ collection), A(the_collections_thread_array.count(collection), _href='/collection/'+ collection), XML(''), _id='test') + HR()
        

    jquery = "jQuery('#thread-list').html('%s');" % test
    jquery += "jQuery('#collection-list').html('%s');" % test1
    return jquery
      
################################
####ajax_add_tag_thread#########
################################                      
def ajax_add_tag_thread():
    tags = request.vars.thread_add_tag_form
    session.tag_thread = tags 
    jquery = "jQuery('.flash').html('%s').slideDown().delay(1000).slideUp();" % session.tag_thread
    return jquery
        
################################
####ajax_add_collection_thread##
################################             
def ajax_add_collection_thread():
    collections = request.vars.thread_add_collection_form
    session.collection_thread = collections 
    jquery = "jQuery('.flash').html('%s').slideDown().delay(1000).slideUp();" % session.collection_thread
    return jquery
        
################################
####ajax_add_tag_collection#####
################################     
def ajax_add_tag_collection():
    tags = request.vars.collection_add_tag_form
    session.collection_tag = tags 
    jquery = "jQuery('.flash').html('%s').slideDown().delay(1000).slideUp();" % session.collection_tag
    return jquery
            
################################
####ajax_reset_collection_tags_session_thread
################################     
def ajax_reset_collection_tags_session_thread():
   session.collection_thread = '' 
   session.tag_thread = ''
   return dict()
