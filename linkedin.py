import pandas as pd
import requests
import re
from collections import Counter
from linkedin_api import Linkedin

api = Linkedin("email", "password")

# data = api.search_jobs(job_title=["backend","back end","back-end", "software", "front-end", "frontend", "front end", "mobile"],location_name="United States")
# data = api.search_jobs(job_title=["backend","back end","back-end", "software", "front-end", "frontend", "front end", "mobile"],location_name="Brazil")
# data = api.search_jobs(job_title=["backend","back end","back-end", "software", "front-end", "frontend", "front end", "mobile"],location_name="Canada")
data = api.search_jobs(job_title=["full-stack", "fullstack", "full stack"],location_name="Brazil")
# data = api.search_jobs(job_title=["full-stack", "fullstack", "full stack"],location_name="United States")

df = pd.DataFrame(data)

df['job_id'] = df['trackingUrn'].str.split(':').str[-1]
 
keywords = ["golang", "nest", "nestjs", "nest.js", "node","nodejs","node js", "node.js", "spring","spring boot", "flask", "django", "ruby","ruby on rails","ruby-on-rails",".net", ".net core", "dot net", "dotnet", "phyton", "c#", "java", "aspnet", "asp.net", "asp .net", "graphql", "php", "laravel", "react", "react.js","angular","vue","reactjs","react js","vuejs","vue js","vue.js","svelte","react native","react-native","flutter", "next", "nextjs", "next.js", "senior", "junior", "pleno", "mid"]

keyword_counts = Counter()

def fetch_job_details(job_id):
    try:
        response = api.get_job(job_id)
    except KeyError:
        return {}
    if 'message' in response:
        return response
    return response

for job_id in df['job_id']:
    details = fetch_job_details(job_id)
    if not details:
        continue
    description_text = details.get("description", {}).get("text", "").lower()
    for keyword in keywords:
        keyword_counts[keyword] += len(re.findall(fr'\b{keyword.lower()}\b', description_text))

keyword_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Count']).sort_values(by='Count', ascending=False)
print(keyword_df)
