==========
urlcompass
==========

   urlcompass is a simple Django app to display active trail of url visited.
   
   Detailed documentation is in the "docs" directory.
   
   Quick start
   ===========
   
      1. Add "polls" to your INSTALLED_APPS setting like this::
      
          INSTALLED_APPS = [
              ...
              'urlcompass',
          ]
      
      2. URLCOMPASS={'root_name':'name-or-root-view',
                    'start':'[&nbsp',
                    'end':'&nbsp]',
                    'sep':'&nbsp>&nbsp',
                    'html_id': 'name-of-my-app',
                    'html_class':'compass bar class',
                    'rename': lambda x: x.replace('_', ' ')
      }
      
      3. In base template add reference to compass:
      
         {% load urlcompass %}
         
          <div>
              {% urlcompass_show %}   
          </div>       
      
      
      4. urlcompass will now be shown.
      
   Example
   =======
   
   github link has and example folder for a mimimal django website using urlcompass.
   
   to use the example, activate it virtualenv and run django manager "python manager.py runserver"
   
   Links
   =====
   
   github: https://github.com/Acrisel/django-urlcompass