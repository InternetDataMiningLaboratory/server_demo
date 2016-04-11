# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月16日 星期三 20时36分43秒
#
'''
    Define and load frontend modules.

    Modules
    ----------------------------
    Automatically load frontend modules according to ``options.ui_modules``
    
    Example
    
        'test' -> modules.test.TestModule

    .. note::
        The name of module follow the name rule of python variables.
    
    .. note::
        The import error will raise if the module name is not correct.

    Once the module list is updated, restart the server.
'''

_MODULE_ROOT = 'module'


def name_rule_translation(name):
    '''
        Translate the name to camel rule.  
        :returns: a new name in camel rule
    '''
    # First letter of each word capitalize
    return ''.join(
        word[0].upper() + word[1:]
        for word in name.split('_') if word
    )


def get_ui_modules(module_list=None):
    '''
        Return the generated ui_modules

        :returns: ``ui_modules``, a list variable for options
    '''
    if module_list is None:
        module_list = []

    # Try to import module from module dir
    # An example may explain how we achieve this
    # Like your ui_modules in config file is ``['test']``
    # In here the function returns ``['test', module.test.TestModule]``
    return dict(
        [
            (
                mod,
                getattr(getattr(
                    __import__(
                        '.'.join((
                            _MODULE_ROOT,
                            mod,
                        ))
                    ),
                    mod),
                    name_rule_translation(mod)+'Module',
               )
            ) for mod in module_list
        ]
    )
