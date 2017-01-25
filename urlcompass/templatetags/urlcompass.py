# -*- encoding: utf-8 -*-
##############################################################################
#
#    Acrisel, Open Source Management Solution    
#    Copyright (C) 2008- Acrisel (acrisel.com) . All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
'''
Created on Aug 12, 2015

@author: Arnon Sela
'''

''' urlcompass template tags

    Overview
    --------
    Defines two tags that are used in conjunction with url_paf utility.
    
    1. urlcompass_show: return html string that shows url path bar
    2. urlcompass_step: gets step for a specified key
    
    It adds a site path bar to each of their web site headers
    
    Definitions
    -----------
    UFL: URL Flow Location is the rout used by user to get to the web page they 
         are on
    UFS: URL Flow Step is a step on user's flow location
     
    Works
    -----
    The mechanism maintains UFL as ordered list of UFSs.  It is OrderedDict
    of view name as key and revered URL as value.
    
    In templates, 
    
        {% load urlcompass %} will load url path into template
        
        {% urlcompass_show %} will show UFL (it also adds current page to path
        
        {%  urlcompass_step view-id %} will get url for particular step
        
    Settings
    --------
    A few settings: 
    URLCOMPASS={'root_name':'spaces',
                'start':'[&nbsp',
                'end':'&nbsp]',
                'sep':'&nbsp>&nbsp',
                'html_id': ' id attribute to add  ',
                'html_class':' class attribute to add ',
    }
    
    TODO: use URLCOMPASS/session_key to record data in the session
'''


from django import template as django_template
from django.template import Context
from collections import OrderedDict

from django.conf import settings as django_settings
from django.core.urlresolvers import resolve
   
URLCOMPASS={  'root_name':'spaces',
              'start':'&gt&gt &nbsp',
              'end': '',
              'sep': '&nbsp &gt &nbsp',
              'rename': lambda x: x,
              'root_name': 'home',
              'template': None,
              'unique': 'key',
              'session_key':'_urlcompass_ufl_container',
}

URLCOMPASS.update(getattr(django_settings, "URLCOMPASS", dict()))
  
class __UrlCompassShowNode(django_template.Node):
    """
          This class is for internal use only.
          
          Its objects are the underline mechanism handling the tracking and
          presentation of compass url.
          
          Its main method :func:render is used by django.
          
      """
      
    def __init__(self, settings):
        self.settings = settings
             
    def render(self, context):
        """returns html div element representing compass url
            
            :param context: django context
            :type context: django context object
            :returns: html div element <div>Compass content</div>
            :rtype: str
            
        """  
          
        global _urlcompass_ufl_container
        request=context['request']
        current_url=request.get_full_path()
        name = resolve(request.path_info).url_name
        
        #_, _, name =current_url.rpartition('/')
        
        if name:
            display_name=self.settings['rename'](name)
        else:
            display_name=self.settings['root_name']
        
        
        try:
            _urlcompass_ufl_container=request.session['_urlcompass_ufl_container']
        except KeyError:
            _urlcompass_ufl_container=[]
        
        
        # TODO: make it flexible to work on the key or value
        #       if key: only one name allow on flow
        #       if value: only one url (with it content is allows
        unique=self.settings['unique']
        url_value=(display_name, current_url)
        if unique:
            if unique=='url':
                try:
                    key_index=list(OrderedDict(_urlcompass_ufl_container).values()).index(url_value)
                except ValueError:
                    pass
                else:
                    # key already in dict, it needs to get new value
                    # entries later than key needs to be truncated.     
                    _urlcompass_ufl_container=_urlcompass_ufl_container[:key_index]
            elif unique=='key':
                try:
                    key_index=list(OrderedDict(_urlcompass_ufl_container).keys()).index(name)
                except ValueError:
                    pass
                else:
                    # key already in dict, it needs to get new value
                    # entries later than key needs to be truncated.     
                    _urlcompass_ufl_container=_urlcompass_ufl_container[:key_index]
            else:
                raise django_template.TemplateSyntaxError("Unknown unique identifier {}; allow only: url or key".format(unique))
            
        _urlcompass_ufl_container.append((name,url_value))
        request.session['_urlcompass_ufl_container']=_urlcompass_ufl_container
        
        template=self.settings['template']
                
        if template:
            t = context.template.engine.get_template(template)
            self.tvars['path': list(_urlcompass_ufl_container.items())]
            result=t.render(Context(self.settings, autoescape=context.autoescape))
        else:
            sep = self.settings['sep']
            root_name=self.settings['root_name']
            html_class=self.settings['html_class']
            bar_list=['<td><a {} href="{}" style="float:left;">{}</a></td>'\
                      .format(html_class, l, n if n else root_name) 
                      for _, (n,l) in _urlcompass_ufl_container]
            result=''
            if len(_urlcompass_ufl_container):
                start='<td><p {} style="float:left;">{}</p></td>'.format(html_class, self.settings['start'])
                end='<td><p {} style="float:left;">{}</p></td>'.format(html_class, self.settings['end'])
                middle='<td><p {} style="float:left;">{}</p></td>'.format(html_class, sep).join(bar_list)
                result= start+middle+end
                result='<nav {}><table><tr>{}</tr></table></nav>'.format(self.settings['html_id'], result)
            
        return result
  

def adopt_html_attr_value(name, value):
    value=value.strip()
    if not (value[0] in ["'", '"'] and value[-1] in ["'", '"']):
        raise django_template.TemplateSyntaxError("{} tag not in quotation".format(name))
    value=value[1:-1]
    return value

def urlcompass_show(parser, token):
    """returns object of __UrlCompassShowNode subclass of django template node object
        
        This functions analyzes settings to configure __UrlCompassShowNode object:
                
        :param parser: django parser object
        :param token: django token object
        :returns: __UrlCompassShowNode
        :rtype: django_template.Node
        
        :Example:
        
        {{ urlcompass_show }}
        
    """  

    
    local_settings={}
    
    local_settings['start']=URLCOMPASS.get('start',)
    local_settings['sep']=URLCOMPASS.get('sep',)
    local_settings['end']=URLCOMPASS.get('end',)
    local_settings['root_name']=URLCOMPASS.get('root_name',)
    local_settings['template']=URLCOMPASS.get('template',)
    local_settings['unique']=URLCOMPASS.get('unique',)
    html_id=local_settings['html_id']= URLCOMPASS.get('html_id', '')
    html_class=local_settings['html_class']= URLCOMPASS.get('html_class', '')
    local_settings['rename']= URLCOMPASS.get('rename', '')
    
    # analyse toekn for start and wep overrides
    parts=token.split_contents()
    if len(parts) > 0:
        parts=[part.partition('=') for part in parts if part != 'urlcompass_show']
        parts=dict([(name.strip(),adopt_html_attr_value(name, value)) for name, _, value in parts])
    else: 
        parts={}
    
    # check for extra keys
    availible_keys=set(local_settings.keys())
    received_keys=set(parts.keys())
    extra=received_keys.difference(availible_keys)
    if len(extra) >0:        
        raise django_template.TemplateSyntaxError("Unknown attributes for 'urlcompass_show': {}".format(extra))
    
    for name, value in parts.items():
        if name in ['start', 'sep', 'end', 'rename', 'root_name', 'template', 'html_id', 'html_class']:
            if name not in 'rename':
                local_settings[name]=value
            else:
                local_settings[name]=eval(value)
                
    if html_class:
        local_settings['html_class']='class="{}"'.format(html_class)
    if html_id:
        local_settings['html_id']='id="{}"'.format(html_id)
        
    return __UrlCompassShowNode(settings=local_settings)
 
 
class __UrlCompassStepNode(django_template.Node):
    """
          This class is for internal use only.
          
          Its objects are renders particular path item on compass url.
          
          Its main method :func:render is used by django.
          
      """
  
    def __init__(self, view):
        self.view = view
  
    def render(self, context):
        """returns html div element representing compass url
            
            :param context: django context
            :type context: django context object
            :returns: html div element <div>Compass content</div>
            :rtype: str
            
        """  
        global _urlcompass_ufl_container
        _urlcompass_ufl_container=context['_urlcompass_ufl_container']
        try:
            view_url=_urlcompass_ufl_container[self.view]
        except KeyError:
            raise django_template.TemplateSyntaxError("{} view-key not found in {}"\
                                               .format(self.view, 
                                                       list(_urlcompass_ufl_container.keys())))
        return view_url
  
  
def urlcompass_step(parser, token):
    """returns object of __UrlCompassStepNode subclass of django template node object
        
        This functions assumes urlcompass_show is already used in the template.
        hence, it access session data sets maintained by urlcompass_show:
                
        :param parser: django parser object
        :param token: django token object
        :returns: __UrlCompassStepNode
        :rtype: django_template.Node
        
        :Example:
        
        {% urlcompass_step <view> %}
        
    """  

    
    # analyse toekn for start and wep overrides
    parts=token.split_contents()
    if len(parts) != 1:
        raise django_template.TemplateSyntaxError("'urlcompass_step' accepts one and only one argument: {% url_compass_step <view> %}")
    
    view=parts[0].strip()
        
    return __UrlCompassStepNode(view)
  
  
register = django_template.Library()
register.tag('urlcompass_show', urlcompass_show)
register.tag('urlcompass_step', urlcompass_step)
