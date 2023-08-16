import requests
import json
import urllib.parse

PAGINATION = 12
cookie = "" ## add your cookie personal of LinkedIn
domain = "" # add domain of the organization
urlOrganization = "" # add url of linkedIn of the organization

users = []
mails = []

def getOrganizationId(organization):
  url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(universalName:{organization})&&queryId=voyagerOrganizationDashCompanies.66b63095f5bc90a4972aaa61dd2ea70b"
  payload = {}
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/vnd.linkedin.normalized+json+2.1',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-li-lang': 'en_US',
    'x-li-track': '{"clientVersion":"1.12.3686","mpVersion":"1.12.3686","osName":"web","timezoneOffset":-5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":3440,"displayHeight":1440}',
    'x-li-page-instance': 'urn:li:page:d_flagship3_company;k3tjqPhCRaWaUn0Y4UKsJA==',
    'csrf-token': csrf-token,
    'x-restli-protocol-version': '2.0.0',
    'x-li-pem-metadata': 'Voyager - Organization - Member=organization-people-card',
    'Connection': 'keep-alive',
    'Referer': f"{urlOrganization}people/",
    'Cookie': cookie,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  return response.json()["data"]["data"]["organizationDashCompaniesByUniversalName"]["*elements"][0].split(":")[3]

def addToFile(items, fileName):
  with open(fileName, "w") as f:
    for item in items:
      f.write(f"{item}\n")
  f.close()

def getInitInfoPage(page):
  idOrganization = getOrganizationId(urlOrganization.split("/")[4])
  url = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-187&count={PAGINATION}&origin=FACETED_SEARCH&q=all&query=(flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:(currentCompany:List({idOrganization}),resultType:List(ORGANIZATION_ALUMNI)),includeFiltersInResponse:true)&start={page}"
  payload = {}
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/vnd.linkedin.normalized+json+2.1',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-li-lang': 'en_US',
    'x-li-track': '{"clientVersion":"1.12.3686","mpVersion":"1.12.3686","osName":"web","timezoneOffset":-5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":3440,"displayHeight":1440}',
    'x-li-page-instance': 'urn:li:page:d_flagship3_company;k3tjqPhCRaWaUn0Y4UKsJA==',
    'csrf-token': csrf-token,
    'x-restli-protocol-version': '2.0.0',
    'x-li-pem-metadata': 'Voyager - Organization - Member=organization-people-card',
    'Connection': 'keep-alive',
    'Referer': urlOrganization,
    'Cookie': cookie,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  data = response.json()["included"]

  for item in data:
    if "trackingUrn" in item and "urn:li:member:" in item["trackingUrn"]:
      publicName = item["title"]["text"]
      sp = publicName.split()
      users.append(f"{sp[0].lower()}.{sp[1].lower()}")
      users.append(f"{sp[0].lower()}.{sp[2].lower()}")
      users.append(f"{sp[1].lower()}.{sp[2].lower()}")
      users.append(f"{sp[0].lower()[0]}{sp[1].lower()}")
      users.append(f"{sp[0].lower()[0]}{sp[2].lower()}")
      users.append(f"{sp[1].lower()[0]}{sp[2].lower()}")

      mails.append(f"{sp[0].lower()}.{sp[1].lower()}@{domain}")
      mails.append(f"{sp[0].lower()}.{sp[2].lower()}@{domain}")
      mails.append(f"{sp[1].lower()}.{sp[2].lower()}@{domain}")
      mails.append(f"{sp[0].lower()[0]}{sp[1].lower()}@{domain}")
      mails.append(f"{sp[0].lower()[0]}{sp[2].lower()}@{domain}")
      mails.append(f"{sp[1].lower()[0]}{sp[2].lower()}@{domain}")

      addToFile(users, "users.txt")
      addToFile(mails, "mails.txt")

if __name__ == "__main__":
  for i in range(0, 100):
    try:
      getInitInfoPage(i*PAGINATION)
    except Exception as e:
      pass

