import streamlit as st
import requests
import time

st.title("NYC Studio Apartment Finder")

def fetch_listings():
    ACTOR_ID = "memo23/apify-streeteasy-cheerio"
    APIFY_API_BASE = "https://api.apify.com/v2"
    token = st.secrets["APIFY_TOKEN"]

    # Start a direct actor run
    run_response = requests.post(
        f"{APIFY_API_BASE}/actors/{ACTOR_ID}/runs",
        params={"token": token},
        json={
            "startUrls": [
                {
                    "url": "https://streeteasy.com/for-rent/queens/studio?price_min=1500&price_max=2100"
                }
            ]
        }
    )

    if run_response.status_code != 201:
        st.error("Failed to start Apify run. Please check your token or actor ID.")
        st.code(run_response.text)
        return []

    run_data = run_response.json()
    run_id = run_data["data"]["id"]

    # Wait for the run to finish
    with st.spinner("Running Apify scraper... this can take up to 2 minutes."):
        for _ in range(30):
            status_response = requests.get(
                f"{APIFY_API_BASE}/actor-runs/{run_id}",
                params={"token": token}
            )
            status_response.raise_for_status()
            status = status_response.json()["data"]["status"]
            if status in ["SUCCEEDED", "FAILED", "ABORTED"]:
                break
            time.sleep(5)

    if status != "SUCCEEDED":
        st.error(f"Apify run failed or was aborted. Status: {status}")
        return []

    # Get dataset results
    results_response = requests.get(
        f"{APIFY_API_BASE}/actor-runs/{run_id}/dataset/items",
        params={"token": token, "clean": "true"}
    )
    results_response.raise_for_status()
    listings = results_response.json()

    return listings

if st.button("Search"):
    with st.spinner("Fetching listings..."):
        listings = fetch_listings()
        if not listings:
            st.info("No listings found or there was an error.")
        else:
            st.success(f"Found {len(listings)} listings!")
            for i, listing in enumerate(listings, 1):
                st.markdown(f"### Listing {i}")
                st.write(listing)
