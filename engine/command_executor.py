from objects.redis_object import RedisObject
class Command_executor:
    def __init__(Self,database):
        Self.db=database
    def execute(Self,command):
        cmd=command.command
        if cmd=='GET':
            key=command.arguments[0]
            val=Self.db.get(key)
            return val
        elif cmd=='SET':
            key=command.arguments[0]
            obj=RedisObject(
                'STRING', #type
                command.arguments[1] #value
                )
            Self.db.set(key,obj)
            return 'OK'
        elif cmd=='DEL':
            key=command.arguments[0]
            msg=Self.db.delete(key)
            return msg


