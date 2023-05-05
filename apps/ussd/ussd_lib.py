     
import json
import requests
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from json import dumps
import urllib.parse as urlparse


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
                url     = self.session.output_url
                payload =   {
                    'channel':  'USSD',
                    'contact':  self.msisdn,
                    'contents': json.dumps(dict(urlparse.parse_qsl(self.session.data)))
                }
                
                print(payload)

                res = requests.request("POST", url, data=payload)
                print(res.text)
                if res.ok:
                    response['msg'] = 'Asante'
                else:
                    response['msg'] = 'Service is not available right now'
                
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
                self.session    = Session.objects.create(session_id=self.session_id,msisdn=self.msisdn,current_tree=menu.init_tree,output_url=menu.output_url,data='msisdn='+self.msisdn)
                return {"status":0,"msg":self.session.current_tree.argument}

        else:
            if session[0].active == False:
                return {"status":4,"msg":"Session has expired"}
            else: 
                self.session    = session[0]
                ns              = True
                msg             = self.msg
                while ns:
                    next_step   = self.match_response(msg)
                    if next_step == 2:
                        ns      = False
                        return {"status":1,"msg":"Too many input errors"}
                    
                    r1  = self.next_response()
                    if r1['status'] == 100:
                        ns      = True
                        msg     = r1['msg']
                    else:
                        ns      = False
                        
                return r1
                    
        

    def next_response(self):
        
        state   = self.session.current_tree 
        if state.show_text:
            res = state.argument
            if self.session.error_count > 0:
                res = state.error_msg+res
            return {"status":0,"msg":res}
        else:
            # call the function
            # print(state.argument+'?'+state.var_name+'='+self.msg+'&'+self.session.data)
            ret     = requests.get(state.argument+'?'+state.var_name+'='+self.msg+'&'+self.session.data)
            msg     = ret.json()
            return {"status":100,"msg":msg}
          
    def match_response(self, user_response):
         
        state       = self.session.current_tree
        next_state  = 0 # remain at current state
        
        for node in state.nodes.all():
            if node.response == user_response or node.response == 'ANY':
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
                next_state  = 1 # next state engaged
                
        if next_state == 0:
            # did not find valid option 
            ## update error counter and repeat previous msg
            self.session.error_count += 1
            self.session.save()
            if self.session.error_count > 3:
                next_state  = 2 # too many errors
       
        return next_state
            
    def has_nodes(self):
        return Node.objects.filter(tree=self.session.current_tree).count()
    
    def cancel_session(self,session_id):
        session     = Session.objects.filter(Q(session_id=session_id))[0]
        session.active = False
        session.save()
        