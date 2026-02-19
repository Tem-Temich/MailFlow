from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from mailings.models import Mailing, Attempt


class Command(BaseCommand):
    help = "Отправка рассылки по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR("Рассылка не найдена"))
            return

        # Проверка активности
        if not mailing.is_active:
            self.stdout.write(self.style.ERROR("Рассылка отключена"))
            return

        now = timezone.now()

        if not (mailing.start_time <= now <= mailing.end_time):
            self.stdout.write(self.style.ERROR("Рассылка сейчас недоступна"))
            return

        recipients = mailing.recipients.all()
        success_count = 0

        for client in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                Attempt.objects.create(
                    mailing=mailing,
                    status="succeeded",
                    server_response="OK",
                )

                success_count += 1

            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    status="failed",
                    server_response=str(e),
                )

        self.stdout.write(
            self.style.SUCCESS(f"Отправлено писем: {success_count}")
        )
