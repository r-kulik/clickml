import datetime


class NoRunningGPUMachineException(Exception):
    def __str__(self):
        return f"""
        At the moment of request ({datetime.datetime.now()}) there is no running GPU machine to handle your task.
        Your task is not saved, so, please, try once more time later.
        """


class WrongFileFormatException(Exception):
    def __str__(self) -> str:
        return f""" It seems that the file you are trying to upload has an extension that differs from ".csv" or \
        is corrupted.
        Please, recheck the file extension and decoding format (it must be UTF-8)
        """