from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()



class Plan(models.Model):
	plan_name = models.CharField(max_length=100, unique=True)  # Name of the plan
	minimum = models.DecimalField(max_digits=12, decimal_places=8)  # Minimum investment
	maximum = models.DecimalField(max_digits=12, decimal_places=8)  # Maximum investment
	duration = models.PositiveIntegerField(help_text="Duration in days ")  # Duration in days
	roi = models.DecimalField(max_digits=5, decimal_places=8, help_text="ROI Percentage")  # ROI percentage

	def __str__(self):
		return self.plan_name

	def get_absolute_url(self):
		return reverse("plans:deposit_on_plan",
			kwargs={"plan_name": self.plan_name})


class UserPlan(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans')  # Link to User
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plans_user')  # Link to Plan
	amount_invested = models.DecimalField(max_digits=12, decimal_places=8)  # Amount user invested
	start_date = models.DateTimeField(auto_now_add=True)  # Date the plan started
	end_date = models.DateTimeField()  # Calculated based on start_date and plan duration
	status = models.CharField(
		max_length=20,
		choices=[('active', 'Active'), ('completed', 'Completed')],
		default='active'
	)  # Status of the user's plan

	def calculate_end_date(self):
		"""Calculate the end date based on the plan's duration."""
		from datetime import timedelta
		return self.start_date + timedelta(days=self.plan.duration)

	def save(self, *args, **kwargs):
		"""Override save to calculate end_date."""
		if not self.end_date:
			self.end_date = self.calculate_end_date()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.user.username} - {self.plan.plan_name}"









