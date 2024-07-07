from ply import settings
def profile_pfp_and_post_date(profile,date):
    return_str = ""
    return_str += f'<img src="{settings.PLY_AVATAR_FILE_URL_BASE_URL}/{profile.avatar}" alt="{profile.name[0:2]}" class="rounded-circle me-2 avatar" width="45" height="45"/>'
    return_str += f'<div style="display: inline-block;"><p class="h4"><i class="fa-regular fa-user"></i> {profile.name}</p><p class="h6"><i class="fa-solid fa-calendar-check"></i> {date}</p></div>'
    return return_str