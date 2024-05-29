import os

import httpx


async def upload(
    api: str,
    api_key: str,
    path: str,
    filename: str,
    content: bytes,
):
    target_path = os.path.join(path, filename)
    headers = {
        "Authorization": api_key,
        "file-path": target_path,
    }
    files = {"file": (filename, content, "application/octet-stream")}
    payload = {"path": path}
    async with httpx.AsyncClient() as client:
        response = await client.put(api + "/api/fs/form", files=files, headers=headers)
        response.raise_for_status()
        response = await client.post(
            api + "/api/fs/list", json=payload, headers=headers
        )
        response.raise_for_status()
    for file_info in response.json()["data"]:
        if file_info["name"] == filename:
            return f"{api}/d/{target_path}?sign={file_info['sign']}"
    raise AssertionError(f"not found {filename}: {response.json()}")
