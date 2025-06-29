import streamlit as st
import requests
import time

st.title("NYC Studio Apartment Finder")

def fetch_listings():
    ACTOR_TASK_ID = "memo23/apify-streeteasy-cheerio"
    APIFY_API_BASE = "https://api.apify.com/v2"
    token = st.secrets["APIFY_TOKEN"]

    # Trigger actor run
    run_response = requests.post(
        f"{APIFY_API_BASE}/actor-tasks/{ACTOR_TASK_ID}/runs",
        params={"token": token},
        json={"startUrls": ["https://streeteasy.com/for-rent/queens/studio?price_min=1500&price_max=2100"]}
    )
    run_response.raise_for_status()
    run_data = run_response.json()
    run_id = run_data["data"]["id"]

    # Poll run status
    for _ in range(30):  # max ~150 sec
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
        st.error(f"Apify run failed with status: {status}")
        return []

    # Fetch results
    results_response = requests.get(
        f"{APIFY_API_BASE}/actor-runs/{run_id}/dataset/items",
        params={"token": token, "clean": "true"}
    )
    results_response.raise_for_status()
    listings = results_response.json()

    return listings

if st.button("Search"):
    with st.spinner("Fetching listings, please wait..."):
        listings = fetch_listings()
        if not listings:
            st.info("No listings found or an error occurred.")
        else:
            st.success(f"Found {len(listings)} listings!")
            for i, listing in enumerate(listings, 1):
                st.markdown(f"### Listing {i}")
                st.write(listing)
