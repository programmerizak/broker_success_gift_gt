from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CopyTrader
import sweetify

@login_required
def copy_trader(request):
    context = {'page_title': 'Copy Trader'}
    copy_traders = CopyTrader.objects.all()
    context['copy_traders'] = copy_traders
    if request.method == "POST":
        expert_id = request.POST.get("expert_id")
        trader_selected = get_object_or_404(CopyTrader, id=expert_id)
        # Add the current user to the copiers of the selected CopyTrader
        trader_selected.copiers.add(request.user)
        # messages.success(request, "You are now copying this trader.")
        sweetify.success(
            request,
            "Successfully",
            text=f"You are now copying this trader.",
            persistent="Close",
        )
        return redirect('copy_trader:copy_trader')
    return render(request, "copy_trader/copy_trader.html", context)
