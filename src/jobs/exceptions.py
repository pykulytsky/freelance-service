class JobBaseException(Exception):
    def __init__(self, job, message="Erorr while creating job") -> None:
        self.job = job
        self.message = message
        super().__init__(self.message)


class JobAlreadyApproveProposal(JobBaseException):
    pass


class JobAlreadyDoneErorr(Exception):
    pass
