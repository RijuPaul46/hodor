from parser.parser import Parser
from engine.command_executor import Command_executor
from storage.database import Database
db=Database()
text="SET name RIJU"
text2='GET name'
text3="SET age 20"
text4 ='GET age'
ls=[text,text2,text3,text4]
parser=Parser()
executor=Command_executor(db)
for text in ls:
    command=parser.parse(text)

    result=executor.execute(command)
    print(result)
for pr in db.store:
    print(pr)
    print(db.store[pr].value)
