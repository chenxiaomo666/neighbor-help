from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info, voucher_check
import requests
import json

purchase_view = Blueprint("purchasr_view", __name__)


# 增加新用户，实现user_id与微信号一一绑定
@purchase_view.route("/voucher/start", methods=["GET"])
@panic()
def voucher_start():
    voucher_check()

    return success()


# 用户发布代购信息
@purchase_view.route("/purchase/release", methods=["POST"])
@panic()
def purchase_release():

    purchase_data = request.get_json()

    user_id = session.get("user_id", None)
    print(user_id)

    return success()

