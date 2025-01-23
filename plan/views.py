from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


from .models import Plan, UserPlan
from .forms import DepositForm


@login_required
def plan_list(request):
    """View to list all plans."""
    context = {'page_title':'Plans'}
    context['plans'] = Plan.objects.all()
    user_plans = (
        UserPlan.objects.filter(user=request.user)
        if request.user.is_authenticated
        else []
    )
    user_plan_ids = {up.plan_id for up in user_plans}
    context.update({'user_plans':user_plans,'user_plan_ids':user_plan_ids})
    return render(request,'plans/plan_list.html',context)


# @login_required
# def plan_detail(request, plan_id):
#     """View to display a specific plan."""
#     plan = get_object_or_404(Plan, id=plan_id)
#     return render(request, 'plans/plan_detail.html', {'plan': plan})



# @login_required
# def subscribe_plan(request):
#     if request.method == "POST":
#         plan_id = request.POST.get("plan_id")
#         plan = Plan.objects.get(id=plan_id)
#         UserPlan.objects.create(user=request.user, plan=plan, amount_invested=plan.minimum)
#         return redirect("plan_list")


def deposit_on_plan(request, plan_name):
    """View to deposit into a specific plan."""
    plan = get_object_or_404(Plan, plan_name=plan_name)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            user_plan = form.save(commit=False)
            user_plan.user = request.user
            user_plan.plan = plan
            user_plan.start_date = timezone.now()
            user_plan.end_date = user_plan.start_date + timedelta(days=plan.duration)
            user_plan.save()
            messages.success(request, 'Your deposit was successful!')
            return redirect(reverse('plans:deposit_on_plan', args=[plan.plan_name]))
    else:
        form = DepositForm()
    return render(request, 'plans/plan_detail.html', {'plan': plan, 'form': form})







