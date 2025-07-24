from django.core.management.base import BaseCommand
from pantry.models import PantryItem
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Send email reminders for pantry items expiring in 2 days'

    def handle(self, *args, **kwargs):
        reminder_date = date.today() + timedelta(days=2)
        users = User.objects.all()

        for user in users:
            items = PantryItem.objects.filter(user=user, expiration_date=reminder_date, used=False)
            if items.exists() and user.email:
                item_list = "\n".join([
                    f"- {item.name} (expires on {item.expiration_date})" for item in items
                ])
                message = (
                    f"Hi {user.username},\n\n"
                    f"The following pantry items will expire soon:\n\n"
                    f"{item_list}\n\n"
                    f"Please consider using them to reduce waste!\n\n"
                    f"— Zero Waste Kitchen"
                )
                send_mail(
                    subject='⏰ Reminder: Pantry Items Expiring Soon',
                    message=message,
                    from_email='noreply@zerowastekitchen.com',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                self.stdout.write(f"✅ Sent reminder to {user.email}")
            else:
                self.stdout.write(f"ℹ️ No items or email for user: {user.username}")
