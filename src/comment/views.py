from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from police.models import Police
from case.models import Case
# Create your views here.

@csrf_exempt
def CreateComment(request):
    if request.method == "POST" and request.is_ajax():
        json_dict = json.loads(request.body.decode('utf-8'))
        comment = json_dict['comment']
        comment_by = json_dict['comment_by']
        case_id = json_dict['case_id']
        try:
            police_obj = Police.objects.get(id = int(comment_by))
            case_obj = Case.objects.get(id = int(case_id))
            comment = Comment.objects.create(comment = comment, user1 = police_obj, case = case_obj)
        except:
            data = {"valid": 0}
            return JsonResponse(data, content_type="application/json")
        data = {"comment": comment.comment, "timestamp": comment.timestamp}
        return JsonResponse(data, content_type="application/json")

    data = {"valid": 0}
    return JsonResponse(data, content_type="application/json")


def CommentPage(request):
    return render(request, "comment/base.html", {})

def HomePage(request):
    return render(request, "index.html", {})
