import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import csv

# ---- KONFIG ----
flow_url = st.secrets["flow_url"]
launch_key = st.secrets["launch_key"]

# Samme filsti, men CSV-format
csv_path = Path(r"C:\Users\SamadIsmayilov\OneDrive - HKdirektoratet\Skrivebord\RPA prosjekt\App for triggering Flows manually\logging av trigger.csv")

st.title("Start automatisert flyt")

# Brukerinput
user_name = st.text_input("Navn")
user_key = st.text_input("Tilgangskode", type="password")

def logg_til_csv(navn: str):
    """Appender dato/klokkeslett og navn til CSV-logg."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)  # Sørg for at mappen finnes
    ny_rad = [datetime.utcnow().replace(microsecond=0).isoformat() + "Z", navn]

    fil_finnes = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not fil_finnes:
            writer.writerow(["Tidspunkt_UTC", "Navn"])
        writer.writerow(ny_rad)

# Logikk
if user_name and user_key:
    if user_key == launch_key:
        st.success("Tilgang godkjent – du kan starte flyten.")
        
        if st.button("Kjør flyt"):
            params = {
                "triggered_by": user_name,
                "trigger_time": datetime.utcnow().isoformat() + "Z",
                "source": "streamlit"
            }
            try:
                response = requests.get(flow_url, params=params)
                if response.status_code in [200, 202]:
                    st.success("Flyten ble trigget!")
                    try:
                        logg_til_csv(user_name)
                        st.info(f"Logget til: {csv_path}")
                    except Exception as e:
                        st.warning(f"Flyt trigget, men logging feilet: {e}")
                else:
                    st.error(f"Feil ved kjøring. Statuskode: {response.status_code}")
            except Exception as e:
                st.error(f"En feil oppstod: {e}")
    else:
        st.error("Feil kode. Prøv igjen.")
elif user_key:
    st.warning("Skriv inn navn for å aktivere.")
