'''
Created on Oct 2, 2015

@author: arnon
'''

from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
import logging

logger=logging.getLogger(__name__)


def compass_main(request,page=0):
    if page=='lastpage': page=4
    nextpage=int(page)+1
    nexturl='compass:'+('nextpage'+ str(nextpage) if nextpage < 4 else 'lastpage')
    html_params={'page': nextpage if int(page) < 4 else 'lastpage',
                 'pageurl': nexturl, }
    
    if nexturl != 'lastpage':
        result = render(request, 'compass/next.html', html_params) 
    else :
        result = render(request, 'compass/last.html', html_params) 
    return   result  

