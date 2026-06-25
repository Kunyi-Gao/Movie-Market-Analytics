def success_response(data=None, meta=None):
    payload = {"success": True, "data": data}
    if meta is not None:
        payload["meta"] = meta
    return payload


def error_response(message: str):
    return {"success": False, "error": message}
