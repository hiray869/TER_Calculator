import streamlit as st
import TER_functions as ter
import pandas as pd

st.title('TER Calculator')

# --- Input parameters ---
st.header('Input parameters')

life_stage = st.radio('Compute for: ', ['Infant', 'Non-infant (Child/Adolescent/Adult)'])

# --- Infant ---
if life_stage == 'Infant':
    age = st.number_input('Age (mo)', min_value=1, max_value=11, step=1)
    weight = st.number_input('Weight (grams)')
    
# --- Non-infant ---
else:
    age = st.number_input('Age (yrs)')
    height_unit = st.radio('Select height unit:', ['centimeters (cm)', 'feet inches (ft in)'])

    if height_unit == 'centimeters (cm)':
        height_cm = st.number_input('Height (cm)')
    else:
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.number_input("Feet", min_value=1, max_value=8)
        with col2:
            height_in = st.number_input("Inches", min_value=0, max_value=11)
        height_cm = height_ft * 30.48 + height_in * 2.54  # convert to cm

    weight = st.number_input('Weight (kg)')
    sex = st.selectbox('Sex', ['Male', 'Female'])
    PAL = st.selectbox('Physical Activity', ['Bed rest', 'Sedentary', 'Light', 'Moderate', 'Heavy', 'Very active/Vigorous'])

    is_given_DBW = st.radio('DBW (kg):', ['Given', 'N/A'])
    
    if is_given_DBW == 'Given':
        given_DBW = st.number_input('DBW (kg)')
    else:
        DBW_method = st.radio('Select DBW calculation method', ['BMI-Based Formulation', "Tannhauser's Method", 'N/A'])


# --- TER Calculation ---
if st.button("Calculate TER"):

    # --- Infants ---
    if life_stage == 'Infant':
        DBW1 = ter.DBW_infant1(weight, age)
        DBW2 = ter.DBW_infant2(age)
        TER1 = ter.TER_infant(age, DBW1)
        TER2 = ter.TER_infant(age, DBW2)
        
        st.subheader("Infant TER Results")
        st.write(f"Method 1 (DBW based on weight): {TER1:.2f} kcal")
        st.write(f"Method 2 (Age-based DBW): {TER2:.2f} kcal")

    # --- Non-infants ---
    else:

        results = {}  # store all TER results

        # --- Adults ---
        if age >= 18:

            # Determine DBW
            if is_given_DBW == 'Given':
                DBW = given_DBW
            elif DBW_method == 'BMI-Based Formulation':
                DBW = ter.DBW_adults_BMI(height_cm)
            elif DBW_method == "Tannhauser's Method":
                DBW = ter.DBW_adults_Tannhauser(height_cm)
            else:
                DBW = None

            # Calculate TER if DBW exists
            if DBW:
                results['Cooper'] = ter.TER_adults_Cooper(DBW, PAL, sex)
                results['Krause'] = ter.TER_adults_Krause(DBW, PAL)
                results['PAGAC'] = ter.TER_adults_PAGAC(DBW, PAL)
            else:
                st.warning("No DBW available. Cooper, Krause, and PAGAC methods will not apply.")

            # Methods that don't require DBW
            results['Mifflin-St Jeor'] = ter.TER_adults_MifflinStJeor(age, weight, height_cm, sex)
            results['Oxford'] = ter.TER_adults_Oxford(age, weight, sex, PAL)
            results['Harris-Benedict'] = ter.TER_adults_HarrisBenedict(age, weight, height_cm, sex)

        # --- Adolescents ---
        elif age > 10:
            if is_given_DBW == 'Given':
                results['CBMRG'] = ter.TER_children_adolescents_CBMRG(age, given_DBW)
                results['PDRI'] = ter.TER_children_adolescents_PDRI(age, given_DBW, sex)
            else:
                st.warning("No DBW value. Cannot calculate TER for adolescents.")

        # --- Children ---
        else:
            DBW = ter.DBW_children(age)
            results['Narins-Weil'] = ter.TER_children_NarinsWeil(age)
            results['CBMRG'] = ter.TER_children_adolescents_CBMRG(age, DBW)
            results['PDRI'] = ter.TER_children_adolescents_PDRI(age, DBW, sex)

        # --- Display TER results ---
        if results:
            st.subheader("TER Results (kcal)")
            df = pd.DataFrame(list(results.items()), columns=['Method', 'TER (kcal)'])
            st.table(df)