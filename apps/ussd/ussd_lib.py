     
import json
import requests
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

class ussd_session:
    
    session     = ''
    
    def __init__(self,session_id,msisdn,msg):
        self.session_id = session_id
        self.msisdn     = msisdn
        self.msg        = msg
    
    
    def get_response(self):
        
        response    = self.transverse()
        status      = response['status']
        
        # status 0 = success
        # status 2 = not valid shortcode
        # status 1 = system error
        # status 3 = last message
        # status 4 = expired session
        
        if status   == 0:
            if self.has_nodes() == 0:
                response['status']  = 3
                self.cancel_session(self.session_id)
                
                ## call final function
                ret = requests.get(self.session.data)
                if ret.json() == 0:
                    response['msg'] = "something went wrong, please try again later"
                ## if fails send corresponding error back
                
        elif status == 2:
            # not a valid menu
            pass
        else:
            self.cancel_session(self.session_id)
            
        return response
        
        
    def transverse(self):
        
        # check if ongoing session
        session         = Session.objects.filter(Q(session_id=self.session_id) & Q(msisdn=self.msisdn))
        if not session:
            # check if is initial session
            menu        = Menu.objects.filter(Q(code=self.msg) & (Q(active=True) | Q(test_numbers__contains=self.msisdn)) )
            if not menu:
                # not valid session or menu return error response
                return {"status":2,"msg":"Shortcode not available"}
            else:
                menu    = menu[0]
                # valid menu create new session
                self.session    = Session.objects.create(session_id=self.session_id,msisdn=self.msisdn,current_tree=menu.init_tree,data=menu.output_url+'?msisdn='+self.msisdn)
                return {"status":0,"msg":self.session.current_tree.argument}

        else:
            if session[0].active == False:
                return {"status":4,"msg":"Session has expired"}
            else: 
                self.session    = session[0]
                
        
        # call tree function
        state   = self.session.current_tree
        # validate msg
        
        # match msg to possible values
        ## get possible values
        
        next_state  = 0
        for node in state.nodes.all():
            if node.response == self.msg:
                # matched response
                ## update current state
                
                ### prepare new data
                n_data = '&'+self.session.current_tree.var_name+'='+self.msg
                self.session.data = str(self.session.data)+n_data
                
                ### reset error count
                self.session.error_count    = 0
                
                ### transverse tree
                self.session.current_tree   = node.next_id
                self.session.save()
                next_state  = 1
                
        if next_state == 0:
            # did not find valid option 
            ## update error counter and repeat previous msg
            self.session.error_count += 1
            self.session.save()
            if self.session.error_count > 4:
                return {"status":1,"msg":"Too many input errors"}
            
        # get current state
        state   = self.session.current_tree 
        if state.show_text:
            res = state.argument
            if self.session.error_count > 0:
                res = 'Invalid input<br>'+res
            return {"status":0,"msg":res}
        else:
            # call the function
            msg = '1' # returned from func
            
            # check if valid response
            next_state  = 0
            for node in state.nodes.all():
                if node.response == msg:
                    # matched response
                    ## update current state
                    ### prepare new data
                    n_data = '&'+self.session.current_tree.var_name+'='+self.msg
                    self.session.data = str(self.session.data)+n_data
                    
                    ### reset error count
                    self.session.error_count    = 0
                    
                    ### Transverse tree
                    self.session.current_tree = node.next_id
                    self.session.save()
                    next_state = 1
                    
            if next_state == 0:
                return {"status":1,"msg":"something wrong with system"}
            
            state   = self.session.current_tree 
            if state.show_text:
                return state.argument
            else:
                return {"status":1,"msg":"circular function recal"}
            
    def has_nodes(self):
        return Node.objects.filter(tree=self.session.current_tree).count()
    
    def cancel_session():
        session     = Session.objects.filter(Q(session_id=self.session_id))[0]
        session.active = False
        session.save()
        