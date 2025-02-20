import json
import os
import numpy as np
import pandas as pd
from flask import Blueprint, current_app, jsonify, request
from backend.services.chain_trace import CONFIG, process_time_and_date, filter_trade_method, select_and_rename_all_columns
from backend.services.chain_trace import trace_trade_chains, trace_trade_chains_bidirection  # 导入你写好的追踪函数

trace_bp = Blueprint('trace', __name__)

@trace_bp.route('/upload', methods=['POST'])
def upload_data():
    """
    上传交易数据的接口。
    """
    global TRADE_DATA
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        TRADE_DATA = pd.read_csv(file)
        # 预处理数据
        TRADE_DATA = process_time_and_date(TRADE_DATA)
        TRADE_DATA = filter_trade_method(TRADE_DATA)
        TRADE_DATA = select_and_rename_all_columns(TRADE_DATA)
        return jsonify({"message": "Data uploaded and processed successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trace_bp.route('/oneway', methods=['POST'])
def trace_oneway():
    """
    单向追踪接口。
    """
    if TRADE_DATA is None:
        return jsonify({"error": "No data available. Please upload data first."}), 400

    try:
        data = request.json
        direction = data.get("direction")
        institution = data.get("institution")
        max_depth = data.get("max_depth", 5)

        if direction not in ["forward", "backward"]:
            return jsonify({"error": "Invalid direction. Use 'forward' or 'backward'."}), 400

        path, path_ids = trace_trade_chains(TRADE_DATA, current_inst=institution, direction=direction, max_depth=max_depth)
        return jsonify({"path": path, "path_ids": path_ids}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trace_bp.route('/bidirectional', methods=['POST'])
def trace_bidirectional():
    """
    双向追踪接口。
    """
    if TRADE_DATA is None:
        return jsonify({"error": "No data available. Please upload data first."}), 400

    try:
        data = request.json
        institution = data.get("institution")
        max_depth = data.get("max_depth", 5)

        result = trace_trade_chains_bidirection(TRADE_DATA, start_inst=institution, max_depth=max_depth)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
