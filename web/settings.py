from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/kilskil2"
ALLOW_UNKNOWN = True

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    # Описываем ресурс `/users`
    'users': {
        #'type'   : 'list',
        'schema' : {
            'username'   : {
                'type': 'string',
                'unique': True,
                'required': True
            },
            # 'uid'        : { 'type': 'integer'},
            'chat_id'    : {'type': 'integer'},
            'ref'        : {
                'type'   : 'dict',
                'schema' : {
                    '_uid': {'type': 'objectid'},
                    '_sid': {'type': 'objectid'},
                }
            },
            'date'       : {
                'type'   : 'dict',
                'schema' : {
                    'updated': {
                        'type'    :'datetime',
                    },
                    'created' : {
                        'type'    :'datetime'
                    }
                }
            },
            'about'     : {
                'type'   : 'dict',
                'schema' : {
                    'moto'   :  { 'type' : 'string' },
                    'bio'    :  { 'type' : 'string' }
                }
            },
            'links'    : {
                'type'   : 'dict',
                'schema' : {
                    'telegram_id' : {'type': 'integer'}
                }
            },
            'timezone' : {
                'type': 'integer',
                'default': 0
            },
            'active': {
                'type': 'boolean',
                'default': True
            },
            'public': {
                'type': 'integer',
                'default': 0
            },
            'flag': {
                'type': 'string',
                'default': 'real'
            },
            'code': {
                'type': 'string',
            }
        }
    },
    'skills': {
        #'type': 'list',
        'schema': {
            '_id'          : {'type': 'objectid'},
            'short'        : {'type': 'string', 'default':""},
            'title'        : {'type': 'string', "required": True},
            'desc'         : {'type': 'string'},
            'materials'    : {
                'type'     : 'dict',
                'schema'   : {
                    'logo' : {'type': 'string'},
                    'text' : {'type': 'list'}
                }
            },
            'tags'         : {'type': 'list'},
            'freq'         : {'type': 'string',  "required": True},
            'count'        : {'type': 'integer', "required": True},
            'ref'          : {
                'type'     : 'dict',
                'schema'   : {
                    '_uid'    : {'type': 'objectid'},
                    '_sid'    : {'type': 'objectid'},
                    '_ouid'   : {'type': 'objectid'},
                    '_osid'   : {'type': 'objectid'}
                }
            },
            'date'       : {
                'type'   : 'dict',
                'schema' : {
                    'updated' : {
                        'type'    :'datetime',
                    },
                    'created' : {
                        'type'    :'datetime'
                    }
                }
            },
            'active': {
                'type': 'boolean',
                'default': True
            },
            'public': {
                'type': 'integer',
                'default': 0
            },
            'flag': {
                'type': 'string',
                'default': 'real'
            },
            'createmode': {
                'type': 'string',
                'default': 'dialog'
            },
            'code': {
                'type': 'string',
            }
        }
    },
    'progress' : {
        #'type': 'list',
        'schema': {
            '_id'          : {'type': 'objectid'},
            'ref'          : {
                'type'     : 'dict',
                'schema'   : {
                    '_uid'    : {'type': 'objectid'},
                    '_sid'    : {'type': 'objectid'},
                }
            },
            'num'          : {
                'type'   : 'integer',
                'default': 0
            },
            "notify" : {
                "type"   : "dict",
                "schema" : {
                    "last_date" : {"type" : "datetime"}
                }
            },
            'trial'       : {
                'type'    : 'list',
                'default' : [],
                "required": True,
                'schema'  : {
                    'type'    : 'dict',
                    'schema'  : {
                        'date' : {'type': 'datetime'},
                        'note' : {'type': 'string'},
                    }
                }
            },
            'active': {
                'type': 'boolean',
                'default': True
            },
            'public': {
                'type': 'integer',
                'default': 0
            },
            'flag': {
                'type'    : 'string',
                'default' : 'real'
            },
            'code': {
                'type': 'string',
            }
        }
    },
    'userSkills':{},
    'skillProgress':{},
    'userSkillProgress':{}

}

#add history progress
