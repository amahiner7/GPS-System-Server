import os
import sys
import imgkit
import datetime as dt
import socket
import json
import urllib.request

import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.conf import settings
from .singleton_object import SingletonObject

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from WebServerService.settings import MEDIA_ROOT, SEND_SMS_URL
from Commons.common import get_public_ip_address

@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(TemplateView):
    template_name = "gps_score_app/display.html"
    qeuryset = None

    def __get_gps_score_information(self, co_div, game_sid, date_time, chkin_no):
        hole_par_data_list = SingletonObject.database_service.get_hole_par_data(co_div=co_div)

        if hole_par_data_list is not None and len(hole_par_data_list) >= 2:
            hole_par_A_data_list = hole_par_data_list[0]
            hole_par_B_data_list = hole_par_data_list[1]

        gps_score_data_list = SingletonObject.database_service.get_gps_score_data(
            co_div=co_div,
            game_sid=game_sid,
            date_time=date_time,
            chkin_no=chkin_no)

        if hole_par_A_data_list is None or len(hole_par_A_data_list) == 0 or \
                hole_par_B_data_list is None or len(hole_par_B_data_list) == 0 or \
                gps_score_data_list is None or len(gps_score_data_list) == 0:
            return None, None, None, None, None, None

        total_Par_A = 0
        total_Par_B = 0

        for cnt_num in range(1, 10):
            cnt_str = "PAR_CNT_0" + str(cnt_num)
            par_cnt_A_value = int(hole_par_A_data_list[cnt_str])
            par_cnt_B_value = int(hole_par_B_data_list[cnt_str])

            total_Par_A = total_Par_A + par_cnt_A_value
            total_Par_B = total_Par_B + par_cnt_B_value

        total_Par = total_Par_A + total_Par_B

        for gps_score_data in gps_score_data_list:
            for cnt_num in range(1, 10):
                cnt_str = "PAR_CNT_0" + str(cnt_num)
                par_cnt_A_value = int(hole_par_A_data_list[cnt_str])
                par_cnt_B_value = int(hole_par_B_data_list[cnt_str])

                score_A_str = "SCORE_A" + str(cnt_num)
                score_B_str = "SCORE_B" + str(cnt_num)
                calc_score_A_str = "CALC_" + score_A_str
                calc_score_B_str = "CALC_" + score_B_str

                score_A_value = int(gps_score_data_list[0][score_A_str])
                score_B_value = int(gps_score_data_list[0][score_B_str])

                calc_score_A_value = score_A_value - par_cnt_A_value
                calc_score_B_value = score_B_value - par_cnt_B_value
                gps_score_data[calc_score_A_str] = calc_score_A_value
                gps_score_data[calc_score_B_str] = calc_score_B_value

        return hole_par_A_data_list, hole_par_B_data_list, gps_score_data_list, total_Par_A, total_Par_B, total_Par

    def __get_context(self, co_div, game_sid, date_time, chkin_no):
        try:
            hole_par_A_data_list, hole_par_B_data_list, gps_score_data_list, total_Par_A, total_Par_B, total_Par = \
                self.__get_gps_score_information(
                    co_div=co_div, game_sid=game_sid, date_time=date_time, chkin_no=chkin_no)

            if hole_par_A_data_list is None or hole_par_B_data_list is None or gps_score_data_list is None:
                return None

            course_A_Name = hole_par_A_data_list["COUR_NAME"]
            course_B_Name = hole_par_B_data_list["COUR_NAME"]
            date_time_temp = dt.datetime.strptime(date_time, "%Y%m%d")
            score_date = date_time_temp.strftime("%Y-%m-%d")
            score_time_temp = gps_score_data_list[0]["EN_TIME"]
            score_time = f"OUT {score_time_temp[0:2]}:{score_time_temp[2:4]}"
            customer_name = gps_score_data_list[0]["CUST_NM"]

            hole_par_A_data_list = [hole_par_A_data_list]
            hole_par_B_data_list = [hole_par_B_data_list]

            context = {
                'view': self.__class__.__name__,
                'hole_par_A_data_list': hole_par_A_data_list,
                'hole_par_B_data_list': hole_par_B_data_list,
                'gps_score_data_list': gps_score_data_list,
                'course_A_Name': course_A_Name,
                'course_B_Name': course_B_Name,
                'total_Par_A': str(total_Par_A),
                'total_Par_B': str(total_Par_B),
                'total_Par': str(total_Par),
                'score_date': score_date,
                'score_time': score_time,
                'customer_name': customer_name
            }

            return context

        except Exception as ex:
            print(ex)
            return None

    def __get_json_string(self, plcbizCd, scoreUrl, sendLogSno, rvtnDt, name,
                          bgnCourseId, rvtnHoleCo, mobileNo, gmberNo, rvtnSno):
        send_list = []
        send_list_item = \
            {
                "scoreUrl": scoreUrl,
                "sendLogSno": sendLogSno,
                "rvtnDt": rvtnDt,
                "name": name,
                "bgnCourseId": bgnCourseId,
                "rvtnHoleCo": rvtnHoleCo,
                "mobileNo": mobileNo,
                "gmberNo": gmberNo,
                "rvtnSno": rvtnSno,
            }

        send_list.append(send_list_item)

        result = {"sendList": send_list, "plcbizCd": plcbizCd}

        return result

    def __update_gps_score_sms_send(self, co_div, game_dt, game_sid, chkin_no, sms_send):
        SingletonObject.database_service.update_gps_score_sms_send(
            co_div=co_div, game_dt=game_dt, game_sid=game_sid, chkin_no=chkin_no, sms_send=sms_send)

    def get(self, request, *args, **kwargs):
        if kwargs["param"] == "display":
            try:
                if request.GET.get("co_div"):
                    co_div = request.GET["co_div"]

                if request.GET.get("game_sid"):
                    game_sid = request.GET["game_sid"]

                if request.GET.get("datetime"):
                    date_time = request.GET["datetime"]
                else:
                    date_time = dt.datetime.now().strftime("%Y%m%d")

                if request.GET.get("chkin_no"):
                    chkin_no = request.GET["chkin_no"]
                else:
                    chkin_no = None

                context = self.__get_context(co_div=co_div, game_sid=game_sid, date_time=date_time, chkin_no=chkin_no)
                if context is None:
                    result = {'rCode': 500, 'rMessage': "Empty data."}
                    return JsonResponse(result, safe=False)

                return render(
                    request, 'gps_score_app/display.html', context)

            except Exception as ex:
                print(ex)
                result = {'rCode': 500, 'rMessage': str(ex)}
                return JsonResponse(result, safe=False)

        elif kwargs["param"] == "screen-shot":
            try:
                if request.GET.get("co_div"):
                    co_div = request.GET["co_div"]

                if request.GET.get("game_sid"):
                    game_sid = request.GET["game_sid"]

                if request.GET.get("datetime"):
                    date_time = request.GET["datetime"]
                else:
                    date_time = dt.datetime.now().strftime("%Y%m%d")

                if request.GET.get("mobile_no"):
                    mobile_no = request.GET["mobile_no"]

                if request.GET.get("chkin_no"):
                    chkin_no = request.GET["chkin_no"]
                else:
                    chkin_no = None

                context = self.__get_context(co_div=co_div, game_sid=game_sid, date_time=date_time, chkin_no=chkin_no)
                if context is None:
                    result = {'rCode': 500, 'rMessage': "Empty data."}
                    return JsonResponse(result, safe=False)

                template_path = "gps_score_app/display.html"
                template = get_template(template_path)
                html = template.render(context)

                wkhtml_to_image = os.path.join(
                    settings.BASE_DIR, "gps_score_app/wkhtmltoimage.exe")

                config = imgkit.config(wkhtmltoimage=wkhtml_to_image, xvfb='/opt/bin/xvfb-run')

                image = imgkit.from_string(html, False, config=config)

                file_path = dt.datetime.now().strftime("%H%M%S%f") + ".jpg"
                save_dir_path = os.path.join(MEDIA_ROOT, co_div, game_sid, date_time)
                file_full_path = os.path.join(save_dir_path, file_path)

                if not os.path.exists(save_dir_path):
                    os.makedirs(save_dir_path)

                ip_address = get_public_ip_address()
                file_url = \
                    f"http://{ip_address}:8080/image/" \
                    f"{co_div}/{game_sid}/{date_time}/{file_path}"

                with open(file_full_path, "wb") as file:
                    file.write(image)

                json_string = self.__get_json_string(
                    plcbizCd=co_div,
                    scoreUrl=file_url,
                    sendLogSno="0001",
                    rvtnDt=date_time,
                    name=context["customer_name"],
                    bgnCourseId="0001",
                    rvtnHoleCo="0001",
                    mobileNo=mobile_no,
                    gmberNo=game_sid,
                    rvtnSno="0001")

                json_dump = json.dumps(json_string)
                request_url = SEND_SMS_URL
                response = requests.get(url=request_url, params={"data": json_dump})

                if chkin_no is not None:
                    self.__update_gps_score_sms_send(
                        co_div=co_div, game_dt=date_time, game_sid=game_sid, chkin_no=chkin_no, sms_send="Y")

                if response.status_code == 200:
                    result = {'rCode': response.status_code, 'rMessage': "Success", "Data": json_string}
                else:
                    result = {'rCode': response.status_code, 'rMessage': response.text}

                return JsonResponse(result, safe=False)

            except Exception as ex:
                print(ex)
                result = {'rCode': 500, 'rMessage': str(ex)}
                return JsonResponse(result, safe=False)
