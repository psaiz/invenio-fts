from unittest.mock import patch


def test_connect(search, ftsmanager):
    print(ftsmanager)


# This one requires the certificate of the server...
# def test_whoami(search, ftsmanager):
#    print(ftsmanager.whoami())


def test_archive(search_clear, ftsmanager):
    def fake_get_jobs_statuses(context, jobs):
        print("FAKING THE STATUS OF THE TRANSFERS")
        print(jobs)
        if jobs:
            return {jobs[0]: "DONE"}
        return {}

    file = "/tmp/dd"
    FAKE_ID = "1244"
    with patch("fts3.rest.client.easy.submit", lambda a, b: FAKE_ID):
        ftsmanager.archive(file, "/tmp/dest")
        print("The transfer has been submitted")
        with patch("fts3.rest.client.easy.get_jobs_statuses", fake_get_jobs_statuses):
            transfers = ftsmanager.all_transfers_status()
            assert transfers == {FAKE_ID: "DONE"}
            print("The transfer finished")
            ftsmanager.ack_transfer(FAKE_ID)
            transfers = ftsmanager.all_transfers_status()
            assert transfers == {}
