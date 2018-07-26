from django import forms
from .models import Case

# ward_choice = (
# ('RJ14W01','Mansarovar'),
# ('RJ14W02','Jagatpura'),
# ('RJ14W03','Sanganer'),
# ('RJ14W04','Kachi Basti'),
# ('RJ14W05','Malviya Nagar'),
# ('RJ14W06','Bani Park'),
# ('RJ14W07','Sitapura'),
# ('RJ14W08','Raja Park'),
# ('RJ14W09','Triveni Nagar'),
# ('RJ14W10','Badi Chopat'),
# ('RJ14W11','Chandpole'),

# )




class case_form(forms.ModelForm):
    # ward_id=forms.ChoiceField(ward_choice)
    incident_time=forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Case
        fields="__all__"
        exclude = ['cyber_case_categories','approved','updated','timestamp','solved']

    def __init__(self, *args, **kwargs):
        super(case_form, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            "name":"title"})
        self.fields['case_categories'].widget.attrs.update({
            'class': 'form-control',
            "name":"case_categories"})

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            "name":"description"})
        self.fields['reg_from_loc'].widget.attrs.update({
            'class': 'form-control',
            "name":"reg_from_loc"})
        self.fields['ward_id'].widget.attrs.update({
            'class': 'form-control',
            "name":"ward_id"})
        self.fields['incident_time'].widget.attrs.update({
            'class': 'form-control',
            "name":"incident_time"})



class cyber_case_form(forms.ModelForm):
    # ward_id=forms.ChoiceField(ward_choice)
    incident_time=forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Case
        fields="__all__"
        exclude = ['case_categories','approved','updated','timestamp','solved']

    def __init__(self, *args, **kwargs):
        super(cyber_case_form, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            "name":"title"})
        self.fields['cyber_case_categories'].widget.attrs.update({
            'class': 'form-control',
            "name":"case_categories"})

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            "name":"description"})
        self.fields['reg_from_loc'].widget.attrs.update({
            'class': 'form-control',
            "name":"reg_from_loc"})
        self.fields['ward_id'].widget.attrs.update({
            'class': 'form-control',
            "name":"ward_id"})
        self.fields['incident_time'].widget.attrs.update({
            'class': 'form-control',
            "name":"incident_time"})
















    # title = models.CharField(max_length=80, blank=False)
    # case_categories = models.ForeignKey(CaseCategory,null=True,blank=True)
    # cyber_case_categories = models.ForeignKey(CyberCaseCategories,null=True,blank=True)
    # description = models.TextField()
    # reg_from_loc = models.CharField(max_length=255, blank=False)
    # userid = models.ForeignKey(Citizen)
    # ward_id = models.CharField(max_length=255, blank=False)
    # incident_time = models.DateTimeField()
    # approved=models.BooleanField()
    # solved=models.BooleanField()
    
    # timestamp = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)