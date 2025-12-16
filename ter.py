import streamlit as st
import TER_functions as ter

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

    if age >= 18:

        is_given_DBW = st.radio('Is DBW given? ', ['Yes', 'No'])

        if is_given_DBW == 'No':

            DBW_method = st.radio('Select DBW calculation method', ['BMI-Based Formulation', 'Tannhauser\'s Method', 'N/A'])
            st.warning('Select \'N/A\' if DBW is not required for the calculations.')
            
    
        else: # check if DBW is given
            
            given_DBW = st.number_input('DBW (kg)')
        
# -- caluclation of ter --- 
if st.button("Calculate TER"):

    if life_stage == 'Infant': # if infant

        DBW_method1 = ter.DBW_infant1(weight,age) 
        DBW_method2 = ter.DBW_infant2(age)
        TER_method1 = ter.TER_infant(age,DBW_method1)
        TER_method2 = ter.TER_infant(age,DBW_method2)

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


    else: # if non-infant

        if age >= 18: #adults

            use_DBW = False

            if is_given_DBW == 'Yes':
                
                DBW = given_DBW
                use_DBW = True
                
            if is_given_DBW == 'No' and DBW_method != 'N/A': 

                DBW_values = {'BMI-Based Formulation': ter.DBW_adults_BMI(height_cm),
                       'Tannhauser\'s Method': ter.DBW_adults_Tannhauser(height_cm)}
                
                DBW = DBW_values[DBW_method]
                use_DBW = True

            if use_DBW:

                TER_adults_Cooper, BMR_Cooper, PA_Cooper, BMR_factor_Cooper, PAL_factor_Cooper = ter.TER_adults_Cooper(DBW, PAL, sex)
                TER_adults_Krause, PAL_factor_Krause = ter.TER_adults_Krause(DBW, PAL)
                TER_adults_PAGAC, PAL_factor_PAGAC = ter.TER_adults_PAGAC(DBW, PAL)

                if is_given_DBW == 'No':

                    st.header('Calculation of DBW')

                    if DBW_method == 'BMI-Based Formulation':
                        
                        st.write('Using BMI-Based Formulation')
                        st.write(f'Normal BMI = 22 kg/m^2')
                        st.write(f'DBW = 22 kg/m^2 x ({height_cm/100: .2f} m)^2 = {DBW: .2f} kg')

                    else:

                        st.subheader('Using Tannhauser\'s Formula')
                        st.write(f'DBW = ({height_cm: .2f} - 100) - 0.1({height_cm: .2f}) = {DBW: .2f} kg')

                st.divider()

                st.header('Calculation of TER')

                st.subheader('Using Cooper\'s method')
                st.write(f'BMR = {BMR_factor_Cooper: .2f} kcal//kg/hr x {DBW: .2f} kg x 24 hrs = {BMR_Cooper: .2f} kcal')
                st.write(f'PA = {BMR_Cooper: .2f} x {PAL_factor_Cooper: .2f} = {PA_Cooper: .2f} kcal')
                st.write(f'TER = {BMR_Cooper: .2f} + {PA_Cooper: .2f} kcal = {TER_adults_Cooper: .2f} kcal')

                st.subheader('Using Krause\'s method')
                st.write(f'TER = {DBW: .2f} kg x {PAL_factor_Krause: .2f} kcal/kg = {TER_adults_Krause: .2f} kcal')

                st.subheader('Using PAGAC method')
                st.write(f'TER = {DBW: .2f} kg x {PAL_factor_PAGAC: .2f} kcal/kg = {TER_adults_PAGAC: .2f} kcal')
            
            if not use_DBW:

                st.write('Since no DBW was given, the Cooper, Krause, and PAGAC methods will not apply.')

            TER_adults_MifflinStJeor, BMR_MifflinStJeor, PAL_factor_MifflinStJeor = ter.TER_adults_MifflinStJeor(age, weight, height_cm, sex, PAL)
            TER_adults_Oxford, BMR_Oxford, PAL_factor_Oxford, a, b = ter.TER_adults_Oxford(age, weight, sex, PAL)
            TER_adults_HarrisBenedict, BMR_HarrisBenedict, PAL_factor_HarrisBenedict = ter.TER_adults_HarrisBenedict(age, weight, height_cm, sex, PAL)

            if sex == 'Male':

                st.subheader('Using Mifflin-St Jeor Equation')
                st.write(f'BMR = (9.99 x {weight: .2f} kg) + (6.25 x {height_cm: .2f} cm) - (4.92 x {age}) + 5 = {BMR_MifflinStJeor: .2f} kcal')
                st.write(f'TER = {BMR_MifflinStJeor: .2f} kcal x {PAL_factor_MifflinStJeor: .2f} = {TER_adults_MifflinStJeor: .2f} kcal')

                
                st.subheader('Using Harris-Benedict Equation')
                st.write(f'BMR = 66.47 + 13.75({weight: .2f} kg) + 5.0({height_cm: .2f} cm) - 6.75{age} = {BMR_HarrisBenedict: .2f} kcal')
                st.write(f'TER = {BMR_HarrisBenedict: .2f} kcal x {PAL_factor_HarrisBenedict} = {TER_adults_HarrisBenedict: .2f} kcal') 

            else: # if female
                
                st.header('Using Mifflin-St Jeor Equation')
                st.write(f'BMR = (9.99 x {weight: .2f} kg) + (6.25 x {height_cm: .2f} cm) - (4.92 x {age}) - 161 = {BMR_MifflinStJeor: .2f} kcal')
                st.write(f'TER = {BMR_MifflinStJeor: .2f} kcal x {PAL_factor_MifflinStJeor: .2f} = {TER_adults_MifflinStJeor: .2f} kcal')
                
                st.subheader('Using Harris-Benedict Equation')
                st.write(f'BMR = 655.1 + 9.56({weight: .2f} kg) + 1.85({height_cm: .2f} cm) - 4.67 x {age} = {BMR_HarrisBenedict: .2f} kcal')
                st.write(f'TER = {BMR_HarrisBenedict: .2f} kcal x {PAL_factor_HarrisBenedict} = {TER_adults_HarrisBenedict: .2f} kcal') 


            st.subheader('Using Oxford Equations')
            st.write(f'BMR = ({a: .2f} x {weight: .2f} kg) + {b} = {BMR_Oxford: .2f} kcal')
            st.write(f'TER = {BMR_Oxford: .2f} kcal x {PAL_factor_Oxford: .2f} = {TER_adults_Oxford: .2f} kcal')

        elif age > 10: #adolescence

            if is_given_DBW == 'No':

                st.write('No given DBW. TER calculation for adoloscents requires DBW value.')

            else: # if DBW is given

                TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, given_DBW)
                TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, given_DBW, sex)

                st.subheader('Using CBMRG formula')
                st.write(f'TER = {given_DBW: .2f} x {k_CBMRG: .2f} kcal/kg = {TER_children_adolescents_CBMRG: .2f} kcal')

                st.write(f'\nUsing PDRI method, TER = {TER_children_adolescents_PDRI} kcal.')
                st.write(f'TER = {given_DBW: .2f} x {k_PDRI: .2f} kcal/kg = {TER_children_adolescents_PDRI: .2f} kcal')

        else: # children 

            DBW = ter.DBW_children(age)

            TER_children_NarinsWeil = ter.TER_children_NarinsWeil(age)
            TER_children_adolescents_CBMRG, k_CBMRG = ter.TER_children_adolescents_CBMRG(age, DBW)
            TER_children_adolescents_PDRI, k_PDRI = ter.TER_children_adolescents_PDRI(age, DBW, sex)

            st.header('Calculation of DBW')
            st.write(f'DBW = {age} x 2 + 8 = {DBW: .2f} kg')

            st.divider()

            st.header('Calculation of TER')

            st.subheader('Using Narins and Weil formula')
            st.write(f'TER = 1000 + 100 x {age} = {TER_children_NarinsWeil: .2f} kcal.')

            st.subheader('Using CBMRG formula')
            st.write(f'TER = {DBW: .2f} x {k_CBMRG: .2f} kcal/kg = {TER_children_adolescents_CBMRG: .2f} kcal')

            st.subheader('Using PDRI method')
            st.write(f'TER = {DBW: .2f} x {k_PDRI: .2f} kcal/kg = {TER_children_adolescents_PDRI: .2f} kcal')