import logging

from .runners import RunMode

LOGGER = logging.getLogger(__name__)

class Surround:
    def __init__(self, runners, assemblies):
        self.runners = runners
        self.assemblies = assemblies

    def run(self, runner_key, assembler_key, mode):
        runner = self.__get_runner(runner_key)

        if not runner:
            LOGGER.error("Failed to find runner '%s'", runner_key)
            return

        assembler = self.__get_assembler(assembler_key)

        if not assembler:
            LOGGER.error("Failed to find assembler '%s'", assembler_key)
            return

        if mode == "batch":
            mode = RunMode.BATCH_PREDICT
        else:
            mode = RunMode.TRAIN

        runner.set_assembler(assembler)
        runner.run(mode)

        return runner

    def list_assemblies(self):
        for i, assembler in enumerate(self.assemblies):
            print("%i. %s" % (i, assembler.assembler_name))

    def list_runners(self):
        for i, runner in enumerate(self.runners):
            print("%i. %s" % (i, runner.name))

    def __get_assembler(self, key):
        assembler = None

        # Try and get the assembler via index
        try:
            index = int(key)

            if 0 <= index < len(self.assemblies):
                assembler = self.assemblies[index]
        except Exception:
            pass

        # Try and get the assember via key (name)
        if not assembler:
            assembler = next((x for x in self.assemblies if x.assembler_name.lower() == key.lower()), None)

        return assembler

    def __get_runner(self, key):
        runner = None

        # Try and get the assembler via index
        try:
            index = int(key)

            if 0 <= index < len(self.runners):
                runner = self.runners[index]
        except Exception:
            pass

        # Try and get the assember via key (name)
        if not runner:
            runner = next((x for x in self.runners if x.name.lower() == key.lower()), None)

        return runner
