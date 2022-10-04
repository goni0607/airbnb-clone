from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    # accuracy = forms.IntegerField(max_value=5, min_value=1)
    review = forms.CharField(widget=forms.Textarea)
    accuracy = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )
    communication = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )
    cleanliness = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )
    location = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )
    check_in = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )
    value = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "radio-button"}),
    )

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(False)
        return review
