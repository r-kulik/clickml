import datetime


class NoRunningGPUMachineException(Exception):
    def __str__(self):
        return f"""
        To the moment of request ({datetime.datetime.now()}) there is no running GPU machine to handle your task.
        Your task is not saved, so, please, try once more time later.
        """