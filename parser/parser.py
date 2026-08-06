from engine.command import Command
class Parser:
    def parse(self,text):
        tokens=text.split()
        cmd=tokens[0]
        arguments=tokens[1:]
        command=Command(
            cmd,
            arguments
        )
        return command