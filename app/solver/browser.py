import subprocess

async def load_page(url: str) -> str:
    """
    Loads JS-rendered page using Node Playwright.
    Forces UTF-8 decoding to avoid Windows cp1252 Unicode errors.
    """
    try:
        result = subprocess.run(
            ["node", "browser.js", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",  
            errors="replace",  
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            err = result.stderr if result.stderr else "Unknown Node error"
            raise Exception(err)

        return result.stdout

    except Exception as e:
        raise Exception(f"Node-based Playwright error: {e}")
