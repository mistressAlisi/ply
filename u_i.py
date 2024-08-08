import requests


re = requests.get("https://app.furrydelphia.org/app/registrar/api/v1/registrants-glimpse/?conIsStaff=true&conCheckedIn=true", headers={"Authorization": "Token ad6a4a0471dfc5d9c1bff90abb10b2bc01d758a6"})

ld = re.json()
new = []
for x in ld:
    new.append({
        "name": x['conBadgeName'],
        "email": x['conEmail'],
        "badge": x['conBadgeNumber'],
    })

for n in new:
    c = requests.post("https://hooks.jouleworks.net/api/w/jouleworks/jobs/run/f/f/furrydelphia/add_user_to_clock?token=1xTtIEW5fsdENEFkVZg7qOBMk69NqdE4",
                  json={
                      "email": n['email'],
                      "badge": n['badge'],
                      "name": n['name']
                  })
    print(c.status_code, c.content)

print(len(new), len(ld))