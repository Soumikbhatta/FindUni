from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
from api.college_probability import CollegeProb
from api.apply_college_list import predictListCollege
from api.mail_server import send_mail
from api.india import colleges_list_exam_india
from api.india import complete_detail
# import pickle
# Create your views here.


@api_view(["POST"])
def collegeProbability(request):
    try:
        # print(request.data)
        colName = request.data['collegeName']
        gpa = request.data['gpa']
        verbal = request.data['verbal']
        quants = request.data['quants']
        writing = request.data['writing']
        scores = ""+str(gpa)+" "+str(verbal)+" "+str(quants)+" "+str(writing)
        # print("Data:",colName,scores)

        # maxTire, scores = CollegeProb('Virginia Tech','4 160 160 4.5')
        neededTire, maxTire, scores, neededGPA, neededVerbal, neededQuants, neededWriting = CollegeProb(
            colName, scores)
        # print("Return:",neededGPA,neededVerbal, neededQuants, neededWriting)
        resp = {"neededTire": neededTire,
                "attainableTire": maxTire,
                "neededTireProb": scores[neededTire],
                "attainableTireProb": scores[maxTire],
                "neededGPA": neededGPA,
                "neededVerbal": neededVerbal,
                "neededQuants": neededQuants,
                "neededWriting": neededWriting,
                }
        return JsonResponse(resp, safe=False)
        # return JsonResponse(str(resp), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def collegeApplyList(request):
    try:
        # print(request.data)
        gpa = request.data['gpa']
        verbal = request.data['verbal']
        quants = request.data['quants']
        writing = request.data['writing']
        scores = ""+str(gpa)+" "+str(verbal)+" "+str(quants)+" "+str(writing)
        # print("Data:",colName,scores)

        # print("scores",scores)
        # print()

        colList = predictListCollege(scores)
        # print()
        # print("HIIIIIII")
        # print()
        return JsonResponse(colList, safe=False)
        # return JsonResponse(str(colList), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response("Bad Request")


@api_view(["POST"])
def ind_exam(request):
    try:
        exam_name = (request.data['Exam_name'])

        colList = colleges_list_exam_india(exam_name)

        return JsonResponse(colList, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response("Bad Request")


@api_view(["POST"])
def ind_coll(request):
    try:
        college_name = (request.data['college_name'])

        col_List = complete_detail(college_name)

        return JsonResponse(col_List, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response("Bad Request")


@api_view(["POST"])
def contact_us(request):
    try:
        name = request.data['name']
        email = request.data['email']
        subject = request.data['subject']
        message = request.data['message']
        print(name, email, subject, message)
        to_send_message = f"""
        Name:{name}
        Email:{email}
        Subject:{subject}
        Message:{message}"""
        send_mail(to_send_message)

        return JsonResponse({"status": "ok", "DATA": "Message Sent Successfully"}, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response("Bad Request")
