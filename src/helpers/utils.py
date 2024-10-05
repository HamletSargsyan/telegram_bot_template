from datetime import timedelta


from database.models import UserModel


def remove_not_allowed_symbols(text: str) -> str:
    not_allowed_symbols = ["#", "<", ">", "{", "}", '"', "'", "$", "(", ")", "@"]
    cleaned_text = "".join(char for char in text if char not in not_allowed_symbols)

    return cleaned_text


def get_time_difference_string(d: timedelta) -> str:
    days = d.days
    years, days_in_year = divmod(days, 365)
    months, days_in_month = divmod(days_in_year, 30)
    hours, remainder = divmod(d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    data = ""
    if years > 0:
        data += f"{years} г. "
    if months > 0:
        data += f"{months} мес. "
    if days_in_month > 0:
        data += f"{days_in_month} д. "
    if hours > 0:
        data += f"{hours} ч. "
    if minutes > 0:
        data += f"{minutes} м. "
    data += f"{seconds} с. "
    return data


def get_user_tag(user: UserModel):
    return f"<a href='tg://user?id={user.id}'>{user.name}</a>"
