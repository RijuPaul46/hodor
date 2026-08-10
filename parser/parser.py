from engine.command import Command


class Parser:

    def parse(self, text):

        tokens = text.split()

        if not tokens:
            return None

        cmd = tokens[0].upper()

        arguments = tokens[1:]

        return Command(
            cmd,
            arguments
        )