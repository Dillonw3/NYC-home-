import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="NYC Studio Finder", layout="centered")

API_TOKEN = st.secrets["APIFY_TOKEN"]

# StreetEasy Scraper Actor details
ACTOR_ID = "memo23/apify-streeteasy-cheerio"

st.title("NYC Studio Apartment Finder")
st.markdown("Filtered live listings from StreetEasy via Apify API.")

def fetch_listings(boroughs, price_min, price_max, move_in_start, move_in_end, laundry=True, pets=False, broker_fee=False):
    # Construct Apify API query URL with filters
    base_url = f"https://api.apify.com/v2/actor-tasks/{ACTOR_ID}/runs?token={API_TOKEN}&limit=1"
    
    # Here you might trigger a run or get last run results — Apify usage details depend on actor specifics
    # For simplicity, we'll just assume results are available at a results URL

    # NOTE: This part might need custom Apify task running and fetching JSON results.
    # For a full production app, you might have to trigger the scraper run, wait, and then fetch output.
    
    st.warning("Live fetching is a complex process requiring API run trigger and polling; this is a placeholder.")

    return []

def main():
    boroughs = st.multiselect("Select boroughs", options=["Queens", "Upper Manhattan"], default=["Queens", "Upper Manhattan"])
    price_min, price_max = st.slider("Price Range ($)", 1500, 2100, (1500, 2100))
    move_in_start = st.date_input("Move-in start date", datetime(2025, 7, 1))
    move_in_end = st.date_input("Move-in end date", datetime(2025, 7, 31))
    laundry = st.checkbox("In-building laundry only", value=True)
    pets = st.checkbox("Allow pets", value=False)
    broker_fee = st.checkbox("Include broker fee listings", value=False)

    if st.button("Search"):
        listings = fetch_listings(boroughs, price_min, price_max, move_in_start, move_in_end, laundry, pets, broker_fee)
        if not listings:
            st.info("No listings found or live data fetching not implemented in this demo.")
        else:
            for listing in listings:
                st.write(listing)

if __name__ == "__main__":
    main()
