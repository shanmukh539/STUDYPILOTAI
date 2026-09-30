import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def search_jobs(keyword, location="india", results=5):
    if not APP_ID or not APP_KEY:
        return "Adzuna credentials are missing."

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword.replace("interships", "internships"),
        "where": location,
        "results_per_page": results,
        "content-type": "application/json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        jobs = data.get("results", [])

        if not jobs:
            return []

        job_list = []

        for job in jobs:

            title = job.get(
                "title",
                "Unknown title"
            )

            company = job.get(
                "company",
                {}
            ).get(
                "display_name",
                "Unknown company"
            )

            location_name = job.get(
                "location",
                {}
            ).get(
                "display_name",
                "Unknown location"
            )

            redirect_url = job.get(
                "redirect_url",
                ""
            )

            job_list.append({
                "title": title,
                "company": company,
                "location": location_name,
                "url": redirect_url
            })

        return job_list

    except requests.RequestException as e:
        return f"Job search failed: {e}"


if __name__ == "__main__":
    print(
        search_jobs(
            "Python developer",
            "Hyderabad",
            5
        )
    )