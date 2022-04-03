

class CmdException(Exception):
    def __init__(self, error: str):
        self.message = 'Aborting, error in commands communicated:\n{0}'.format(error)
        super().__init__(self.message)


class SettingsException(Exception):
    def __init__(self, error: str):
        self.message = 'Settings file is inconsistent:\n{0}'.format(error)
        super().__init__(self.message)