from unittest.mock import patch


def test_connect(ftsmanager):
    print(ftsmanager)


# This one requires the certificate of the server...
# def test_whoami(search, ftsmanager):
#    print(ftsmanager.whoami())


def test_archive(ftsmanager):
    FAKE_ID = "1244"

    def fake_get_job_status(context, job):
        print("FAKING THE STATUS OF THE TRANSFERS")
        print(job)
        if job == FAKE_ID:
            return "DONE"
        return None

    with patch("fts3.rest.client.easy.submit", lambda a, b: FAKE_ID):
        ftsmanager.archive("/tmp/dd", "/tmp/dest")
        print("The transfer has been submitted")
        with patch("fts3.rest.client.easy.get_job_status", fake_get_job_status):
            status = ftsmanager.transfer_status(FAKE_ID)
            assert status == "DONE"
            print("The transfer finished")
