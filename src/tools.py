import logging as log

class Logger:
    def __init__(self, name: str) -> None:
        """
        Create logger for feedback.
        :param name: String. logger name.
        """
        self.logger = log.getLogger(name)
        self.logger.setLevel(log.DEBUG)

        # create console for debugging
        ch = log.StreamHandler()
        ch.setLevel(log.DEBUG)

        # create formatter
        formatter = log.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to console
        ch.setFormatter(formatter)

        # add console to logger
        self.logger.addHandler(ch)


# create logger
logger = Logger('SQL Querier').logger