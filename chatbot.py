def advisor(
    rainfall,
    avg_temp,
    risk,
    forecast
):

    advice = []

    if rainfall < 20:

        advice.append(
            "Rainfall is below normal. Consider drought tolerant maize."
        )

    if avg_temp > 30:

        advice.append(
            "High temperatures expected. Monitor irrigation."
        )

    if risk == "High":

        advice.append(
            "High climate risk. Delay planting."
        )

    if forecast > 50000:

        advice.append(
            "High production expected. Plan storage facilities."
        )

    if not advice:

        advice.append(
            "Conditions look favorable."
        )

    return advice
import streamlit as st

# --- UI Code goes at the bottom of the file ---

st.title("🌽 Kenya Maize Forecast Advisor")

st.write("Enter your conditions below to get advice:")

# Create input boxes for the user
rainfall_val = st.number_input("Rainfall (mm):", value=15.0)
temp_val = st.number_input("Average Temperature (°C):", value=32.0)

# Create a button
if st.button("Get Advice"):
    # Call your function
    # Note: I'm passing dummy data for 'risk' and 'forecast' just to make it work
    results = advisor(rainfall_val, temp_val, "Medium", 60000)
    
    # Display the results on the screen
    if results:
        for tip in results:
            st.warning(tip)
    else:
        st.success("Conditions look normal. No special advice needed.")