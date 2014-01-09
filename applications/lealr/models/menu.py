################################################################
####menu########################################################
################################################################

response.logo = A(B('lealr'), _class="brand", _id="logo_text",_href="/", _style="margin-left:auto;padding-left:5px;padding-right:10px;padding-bottom:13px;font-size:25px;font-family:'Bookman Old Style', Bookman, 'Goudy Old Style', Garamond, 'Hoefler Text', 'Bitstream Charter', Georgia, serif;font-weight:400;linear-gradient(to bottom, rgb(66,70,79),rgb(65,69,78))")
                  
################################
####title#######################
################################
if request.function == 'index':
    response.title = 'lealr'
else:
    response.title = request.function

################################
####meta########################
################################        
response.meta.author = 'Trevor Overman'
response.meta.description = 'lealr'
response.meta.keywords = 'leal, organizing, information'
response.meta.generator = 'oh leal'
