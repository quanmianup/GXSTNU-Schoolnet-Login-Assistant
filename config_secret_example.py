# 校园网登录凭证
USERNAME = 'your_username_here'  # 替换为你的实际账号
PASSWORD = 'your_password_here'  # 替换为你的实际密码


def update_credentials(username, password):
    """更新配置文件中的账号密码"""
    with open(__file__, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('USERNAME ='):
            lines[i] = f"USERNAME = '{username}'  # 替换为你的实际账号\n"
        elif line.strip().startswith('PASSWORD ='):
            lines[i] = f"PASSWORD = '{password}'  # 替换为你的实际密码\n"

    with open(__file__, 'w', encoding='utf-8') as f:
        f.writelines(lines)
