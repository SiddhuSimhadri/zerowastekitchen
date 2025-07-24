from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from .models import WasteItem
from django.db.models import Count

@login_required
def waste_stats(request):
    today = date.today()
    last_30_days = today - timedelta(days=30)
    wastes = WasteItem.objects.filter(user=request.user, wasted_on__gte=last_30_days)

    # Count wasted items grouped by day
    stats = wastes.values('wasted_on').annotate(count=Count('id')).order_by('wasted_on')

    # Prepare data for Chart.js
    labels = [entry['wasted_on'].strftime('%Y-%m-%d') for entry in stats]
    counts = [entry['count'] for entry in stats]

    context = {
        'labels': labels,
        'counts': counts,
    }
    return render(request, 'waste/stats.html', context)
