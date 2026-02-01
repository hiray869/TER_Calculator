import streamlit as st
import TER_functions as ter

st.title('TER Calculator')

# --- user-inputs ---
st.header('Input parameters')

# --- Life stage ---
life_stage = st.radio('Compute for: ', ['Infant', 'Child/Adolescent/Adult'])

# --- Input fields ---
if life_stage == 'Infant':
    age = st.number_input('Age (mo)', min_value=1, max_value=11, step=1)
    weight = st.number_input('Weight (grams)')
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
        height_cm = (height_ft * 12 + height_in) * 2.54

    weight = st.number_input('Weight (kg)')
    sex = st.selectbox('Sex', ['Male', 'Female'])
    PAL = st.selectbox('Physical Activity', ['Bed rest', 'Sedentary', 'Light', 'Moderate', 'Heavy', 'Very active/Vigorous'])

    st.write('Select method for DBW calculation.')
    DBW_method = st.selectbox('Select DBW calculation method', ['BMI-Based Formulation', "Tannhauser's Method", 'Input a value'])
    st.warning("BMI-Based Formulation and Tannhauser's Method only apply to adults.")

    given_DBW = None
    if DBW_method == 'Input a value':
        given_DBW = st.number_input('DBW (kg)')

# --- Initialize session_state ---
if 'TER_results' not in st.session_state:
    st.session_state.TER_results = None
if 'CPF_method' not in st.session_state:
    st.session_state.CPF_method = None
if 'CPF_percentages' not in st.session_state:
    st.session_state.CPF_percentages = {}

# --- TER Calculation ---
if st.button("Calculate TER"):
    # --- Infant ---
    if life_stage == 'Infant':
        DBW_method1 = ter.DBW_infant1(weight, age)
        DBW_method2 = ter.DBW_infant2(age)
        TER_method1 = ter.TER_infant(age, DBW_method1)
        TER_method2 = ter.TER_infant(age, DBW_method2)

        st.subheader('Method 1')
        if age <= 6:
            st.write(f'DBW = {weight: .2f} grams + ({age} x 600) = {DBW_method1*1000: .2f} g = {DBW_method1: .2f} kg')
            st.write(f'TER = {DBW_method1: .2f} kg x 95 kcal/kg = {TER_method1: .2f} kcal')
        else:
            st.write(f'DBW = {weight: .2f} grams + ({age} x 500) = {DBW_method1*1000: .2f} g = {DBW_method1: .2f} kg')
            st.write(f'TER = {DBW_method1: .2f} kg x 80 kcal/kg = {TER_method1: .2f} kcal')

        st.subheader('Method 2')
        st.write(f'DBW = {age}/2 + 3 = {DBW_method2} kg')
        if age <= 6:
            st.write(f'TER = {DBW_method2: .2f} kg x 95 kcal/kg = {TER_method2} kcal')
        else:
            st.write(f'TER = {DBW_method2: .2f} kg x 80 kcal/kg = {TER_method2} kcal')

        st.session_state.TER_results = {'Method 1': TER_method1, 'Method 2': TER_method2}

    # --- Non-infant (children/adults) ---
    else:
        # Adults
        if age >= 18:
            DBW_values = {'BMI-Based Formulation': ter.DBW_adults_BMI(height_cm),
                          "Tannhauser's Method": ter.DBW_adults_Tannhauser(height_cm),
                          'Input a value': given_DBW}
            DBW = DBW_values[DBW_method]

            # --- Call TER functions ---
            TER_adults_Cooper, BMR_Cooper, PA_Cooper, BMR_factor_Cooper, PAL_factor_Cooper = ter.TER_adults_Cooper(DBW, PAL, sex)
            TER_adults_Krause, PAL_factor_Krause = ter.TER_adults_Krause(DBW, PAL)
            TER_adults_PAGAC, PAL_factor_PAGAC = ter.TER_adults_PAGAC(DBW, PAL)
            TER_adults_MifflinStJeor, BMR_MifflinStJeor, PAL_factor_MifflinStJeor = ter.TER_adults_MifflinStJeor(age, weight, height_cm, sex, PAL)
            TER_adults_Oxford, BMR_Oxford, PAL_factor_Oxford, a, b = ter.TER_adults_Oxford(age, weight, sex, PAL)
            TER_adults_HarrisBenedict, BMR_HarrisBenedict, PAL_factor_HarrisBenedict = ter.TER_adults_HarrisBenedict(age, weight, height_cm, sex, PAL)

            st.session_state.TER_results = {
                "Cooper": TER_adults_Cooper,
                "Krause": TER_adults_Krause,
                "PAGAC": TER_adults_PAGAC,
                "Mifflin-St Jeor": TER_adults_MifflinStJeor,
                "Oxford": TER_adults_Oxford,
                "Harris-Benedict": TER_adults_HarrisBenedict
            }

        # Adolescents and children
        elif age > 10:
            TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, given_DBW)
            TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, given_DBW, sex)
            st.session_state.TER_results = {'CBMRG': TER_children_adolescents_CBMRG,
                                            'PDRI': TER_children_adolescents_PDRI}
        else:
            DBW = ter.DBW_children(age)
            TER_children_NarinsWeil = ter.TER_children_NarinsWeil(age)
            TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, DBW)
            TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, DBW, sex)
            st.session_state.TER_results = {
                'Narins and Weil': TER_children_NarinsWeil,
                'CBMRG': TER_children_adolescents_CBMRG,
                'PDRI': TER_children_adolescents_PDRI
            }

# --- CPF distribution ---
if st.session_state.TER_results is not None:
    st.header('CPF Distribution')

    # --- Method selection ---
    method = st.selectbox('Select TER method for CPF distribution', list(st.session_state.TER_results.keys()))
    st.session_state.CPF_method = method
    TER_selected = st.session_state.TER_results[method]

    st.write(f"Selected TER: {TER_selected} kcal using {method} method")

    # --- Sliders for percentages ---
    st.subheader('Enter CPF Percentages')
    components = ['Carbohydrates', 'Protein', 'Fat']
    for comp in components:
        if comp not in st.session_state.CPF_percentages:
            st.session_state.CPF_percentages[comp] = 0
        st.session_state.CPF_percentages[comp] = st.slider(f'{comp} %', 0, 100, st.session_state.CPF_percentages[comp])

    total_percent = sum(st.session_state.CPF_percentages.values())
    if total_percent != 100:
        st.warning(f'Total CPF percentages = {total_percent}%. It should sum to 100%.')

    # --- Compute kcal for each component ---
    if total_percent == 100:
        st.subheader('Energy Distribution')
        for comp, pct in st.session_state.CPF_percentages.items():
            kcal = TER_selected * pct / 100
            st.write(f'{comp}: {kcal:.2f} kcal ({pct}%)')
