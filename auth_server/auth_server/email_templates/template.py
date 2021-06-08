# переделать
def simple_template_for_email(token: str):
    return f"""
<html>
<body>
<p>Hi This test mail
<br>{token}</p>
</body>
</html>
"""
