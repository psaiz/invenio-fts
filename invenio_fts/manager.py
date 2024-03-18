import fts3.rest.client.easy as fts3

from .persistency import Persistency


class TransferManager:
    def __init__(self, endpoint, ucert, ukey):
        self._context = fts3.Context(endpoint, ucert, ukey, verify=True)
        self._persistency = Persistency()

    def _submit(self, job):
        job_id = fts3.submit(self._context, job)
        self._persistency.insert_transfer(job_id)
        return job_id

    def _basic_job(self, source, dest):
        return {"files": [{"sources": [source], "destinations": [dest]}]}

    def stage(self, source, dest):
        job = self._basic_job(source, dest)

        job["params"] = {"bring_online": 604800, "copy_pin_lifetime": 64000}
        return self._submit(job)

    def archive(self, source, dest):
        job = self._basic_job(source, dest)
        job["params"] = {"archive_timeout": 86400, "copy_pin_lifetime": 64000}

        return self._submit(job)

    def all_transfers_status(self):
        ids = self._persistency.get_transfers()

        return fts3.get_jobs_statuses(self._context, ids)

    def ack_transfer(self, transfer_id):
        self._persistency.ack_transfer(transfer_id)

    def transfer_status(self, transfer_id):
        return fts3.get_job_status(self._context, transfer_id)

    def get_endpoint_info(self):
        return self._context.get_endpoint_info()

    def whoami(self):
        return fts3.whoami(self._context)
