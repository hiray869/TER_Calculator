import streamlit as st
import TER_functions as ter

if "outputs" not in st.session_state:
    st.session_state.outputs = []

# --- output wrapper functions ----
def out_header(text):
    st.session_state.outputs.append(("header", text))

def out_subheader(text):
    st.session_state.outputs.append(("subheader", text))

def out_write(text):
    st.session_state.outputs.append(("write", text))

def out_divider():
    st.session_state.outputs.append(("divider", None))

def clear_results():
    st.session_state.outputs = []

st.title('TER Calculator')

# --- user-inputs ---
st.header('Input parameters')

life_stage = st.radio('Compute for: ', ['Infant', 'Child/Adolescent/Adult'])

if life_stage == 'Infant':

    age = st.number_input('Age (mo)', min_value = 1, max_value = 11, step = 1) 
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
        
        height_cm = (height_ft*12 + height_in)*2.54

    weight = st.number_input('Weight (kg)')
    sex = st.selectbox('Sex', ['Male', 'Female'])
    PAL = st.selectbox('Physical Activity', ['Bed rest', 'Sedentary', 'Light', 'Moderate', 'Heavy', 'Very active/Vigorous'])

    st.write('Select method for DBW calculation.')
    DBW_method = st.selectbox('Select DBW calculation method', ['BMI-Based Formulation', 'Tannhauser\'s Method', 'Input a value'])
    st.warning('BMI-Based Formulation and Tannhauser\'s Method only apply to adults.')

    given_DBW = None
    if DBW_method == 'Input a value':

        given_DBW = st.number_input('DBW (kg)')
    
# -- caluclation of ter --- 
if st.button("Calculate TER"):

    clear_results()

    if life_stage == 'Infant': # if infant

        DBW_method1 = ter.DBW_infant1(weight,age) 
        DBW_method2 = ter.DBW_infant2(age)
        TER_method1 = ter.TER_infant(age,DBW_method1)
        TER_method2 = ter.TER_infant(age,DBW_method2)

        out_subheader('Method 1')

        if age <= 6:

            out_write(f'DBW = {weight: .2f} grams + ({age} x 600) = {DBW_method1*1000: .2f} g = {DBW_method1: .2f} kg')
            out_write(f'TER = {DBW_method1: .2f} kg x 95 kcal/kg = {TER_method1: .2f} kcal')
        
        else:

            out_write(f'DBW = {weight: .2f} grams + ({age} x 500) = {DBW_method1*1000: .2f} g = {DBW_method1: .2f} kg')
            out_write(f'TER = {DBW_method1: .2f} kg x 80 kcal/kg = {TER_method1: .2f} kcal')

        TER_results = {'Method 1': TER_method1,
                       'Method 2': TER_method2
                       }

        out_subheader('Method 2')

        out_write(f'DBW = {age}/2 + 3 = {DBW_method2} kg')
        
        if age <= 6:

            out_write(f'TER = {DBW_method2: .2f} kg x 95 kcal/kg = {TER_method2} kcal')

        else:

            out_write(f'TER = {DBW_method2: .2f} kg x 80 kcal/kg = {TER_method2} kcal')
    
    else: # if non-infant

        if age >= 18: # adults

            DBW_values = {'BMI-Based Formulation': ter.DBW_adults_BMI(height_cm),
                    'Tannhauser\'s Method': ter.DBW_adults_Tannhauser(height_cm),
                    'Input a value': given_DBW}
            
            DBW = DBW_values[DBW_method]
            
            # call ter functions
            TER_adults_Cooper, BMR_Cooper, PA_Cooper, BMR_factor_Cooper, PAL_factor_Cooper = ter.TER_adults_Cooper(DBW, PAL, sex)
            TER_adults_Krause, PAL_factor_Krause = ter.TER_adults_Krause(DBW, PAL)
            TER_adults_PAGAC, PAL_factor_PAGAC = ter.TER_adults_PAGAC(DBW, PAL)
            TER_adults_MifflinStJeor, BMR_MifflinStJeor, PAL_factor_MifflinStJeor = ter.TER_adults_MifflinStJeor(age, weight, height_cm, sex, PAL)
            TER_adults_Oxford, BMR_Oxford, PAL_factor_Oxford, a, b = ter.TER_adults_Oxford(age, weight, sex, PAL)
            TER_adults_HarrisBenedict, BMR_HarrisBenedict, PAL_factor_HarrisBenedict = ter.TER_adults_HarrisBenedict(age, weight, height_cm, sex, PAL)

            TER_results = {
                            "Cooper": TER_adults_Cooper,
                            "Krause": TER_adults_Krause,
                            "PAGAC": TER_adults_PAGAC,
                            "Mifflin-St Jeor": TER_adults_MifflinStJeor,
                            "Oxford": TER_adults_Oxford,
                            "Harris-Benedict": TER_adults_HarrisBenedict
                        }

            # sample computations
            if DBW_method == 'BMI-Based Formulation' or DBW_method == 'Tannhauser\'s Method': 

                out_header('Calculation of DBW')

                if DBW_method == 'BMI-Based Formulation':
                    
                    out_write('Using BMI-Based Formulation')
                    out_write(f'Normal BMI = 22 kg/m^2')
                    out_write(f'DBW = 22 kg/m^2 x ({height_cm/100: .2f} m)^2 = {DBW: .2f} kg')

                else:

                    out_subheader('Using Tannhauser\'s Formula')
                    out_write(f'DBW = ({height_cm: .2f} - 100) - 0.1({height_cm: .2f}) = {DBW: .2f} kg')

            out_divider()

            out_header('Calculation of TER')

            out_subheader('Using Cooper\'s method')
            out_write(f'BMR = {BMR_factor_Cooper: .2f} kcal//kg/hr x {DBW: .2f} kg x 24 hrs = {BMR_Cooper: .2f} kcal')
            out_write(f'PA = {BMR_Cooper: .2f} x {PAL_factor_Cooper: .2f} = {PA_Cooper: .2f} kcal')
            out_write(f'TER = {BMR_Cooper: .2f} + {PA_Cooper: .2f} kcal = {TER_adults_Cooper: .2f} kcal')

            out_subheader('Using Krause\'s method')
            out_write(f'TER = {DBW: .2f} kg x {PAL_factor_Krause: .2f} kcal/kg = {TER_adults_Krause: .2f} kcal')

            out_subheader('Using PAGAC method')
            out_write(f'TER = {DBW: .2f} kg x {PAL_factor_PAGAC: .2f} kcal/kg = {TER_adults_PAGAC: .2f} kcal')

            if sex == 'Male':

                out_subheader('Using Mifflin-St Jeor Equation')
                out_write(f'BMR = (9.99 x {weight: .2f} kg) + (6.25 x {height_cm: .2f} cm) - (4.92 x {age}) + 5 = {BMR_MifflinStJeor: .2f} kcal')
                out_write(f'TER = {BMR_MifflinStJeor: .2f} kcal x {PAL_factor_MifflinStJeor: .2f} = {TER_adults_MifflinStJeor: .2f} kcal')

                
                out_subheader('Using Harris-Benedict Equation')
                out_write(f'BMR = 66.47 + 13.75({weight: .2f} kg) + 5.0({height_cm: .2f} cm) - 6.75{age} = {BMR_HarrisBenedict: .2f} kcal')
                out_write(f'TER = {BMR_HarrisBenedict: .2f} kcal x {PAL_factor_HarrisBenedict} = {TER_adults_HarrisBenedict: .2f} kcal') 

            else: # if female
                
                out_header('Using Mifflin-St Jeor Equation')
                out_write(f'BMR = (9.99 x {weight: .2f} kg) + (6.25 x {height_cm: .2f} cm) - (4.92 x {age}) - 161 = {BMR_MifflinStJeor: .2f} kcal')
                out_write(f'TER = {BMR_MifflinStJeor: .2f} kcal x {PAL_factor_MifflinStJeor: .2f} = {TER_adults_MifflinStJeor: .2f} kcal')
                
                out_subheader('Using Harris-Benedict Equation')
                out_write(f'BMR = 655.1 + 9.56({weight: .2f} kg) + 1.85({height_cm: .2f} cm) - 4.67 x {age} = {BMR_HarrisBenedict: .2f} kcal')
                out_write(f'TER = {BMR_HarrisBenedict: .2f} kcal x {PAL_factor_HarrisBenedict} = {TER_adults_HarrisBenedict: .2f} kcal') 


            out_subheader('Using Oxford Equations')
            out_write(f'BMR = ({a: .2f} x {weight: .2f} kg) + {b} = {BMR_Oxford: .2f} kcal')
            out_write(f'TER = {BMR_Oxford: .2f} kcal x {PAL_factor_Oxford: .2f} = {TER_adults_Oxford: .2f} kcal')

        elif age > 10: #adolescence

            TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, given_DBW)
            TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, given_DBW, sex)

            TER_results = {'CBMRG': TER_children_adolescents_CBMRG,
                           'PDRI': TER_children_adolescents_PDRI
                        }
            
            out_subheader('Using CBMRG formula')
            out_write(f'TER = {given_DBW: .2f} x {k_CBMRG: .2f} kcal/kg = {TER_children_adolescents_CBMRG: .2f} kcal')

            out_subheader('Using PDRI method')
            out_write(f'TER = {given_DBW: .2f} x {k_PDRI: .2f} kcal/kg = {TER_children_adolescents_PDRI: .2f} kcal')

        else: # children 

            DBW = ter.DBW_children(age)

            TER_children_NarinsWeil = ter.TER_children_NarinsWeil(age)
            TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, DBW)
            TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, DBW, sex)

            TER_results = {'Narins and Weil': TER_children_NarinsWeil,
                           'CBMRG': TER_children_adolescents_CBMRG,
                           'PDRI': TER_children_adolescents_PDRI
                          }
    
            out_header('Calculation of DBW')
            out_write(f'DBW = {age} x 2 + 8 = {DBW: .2f} kg')

            out_divider()

            out_header('Calculation of TER')

            out_subheader('Using Narins and Weil formula')
            out_write(f'TER = 1000 + 100 x {age} = {TER_children_NarinsWeil: .2f} kcal.')

            out_subheader('Using CBMRG formula')
            out_write(f'TER = {DBW: .2f} x {k_CBMRG: .2f} kcal/kg = {TER_children_adolescents_CBMRG: .2f} kcal')

            out_subheader('Using PDRI method')
            out_write(f'TER = {DBW: .2f} x {k_PDRI: .2f} kcal/kg = {TER_children_adolescents_PDRI: .2f} kcal')
    
# --- render all outputs --- 

st.divider()
st.header("Computed Results")

for kind, content in st.session_state.outputs:
    if kind == "header":
        st.header(content)
    elif kind == "subheader":
        st.subheader(content)
    elif kind == "write":
        st.write(content)
    elif kind == "divider":
        st.divider()