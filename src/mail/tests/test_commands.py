import pytest
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from menu_cards.tests.conftest import test_users

pytestmark = pytest.mark.django_db


class SendEmailCommandTest(TestCase):
    logger = "mail.management.commands.send_email"

    def test_send_email_command_successful_run(self):
        with self.assertLogs(self.logger, level="INFO") as caplog:
            call_command("send_email")
            self.assertIn("Emails successfully sent", caplog.output[-1])


def test_email_has_correct_recipients_list(test_users):
    call_command("send_email")
    recipients_list = [user.email for user in test_users]
    assert len(set(mail.outbox[0].to) - set(recipients_list)) == 0
