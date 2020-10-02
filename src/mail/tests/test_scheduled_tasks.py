import freezegun
import pytest
from django.test import TestCase
from django.utils import timezone

from mail import tasks

pytestmark = pytest.mark.django_db

TIMESTAMP = timezone.datetime(2020, 1, 1, 17, 20, 59, tzinfo=timezone.utc)


class SendEmailCommandTest(TestCase):
    logger = "mail.tasks"

    @freezegun.freeze_time(TIMESTAMP)
    def test_send_email_command_successful_run(self):
        with self.assertLogs(self.logger, level="INFO") as caplog:
            assert tasks.send_emails.run()
            self.assertIn(
                f"Send emails task initiated : {TIMESTAMP}", caplog.output[-1]
            )
