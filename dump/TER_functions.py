# -- DBW functions --- 
def DBW_infant1(weight, age):
    if age <= 6:
        DBW = weight + age*600
    else:
        DBW = weight + age*500
    return DBW/1000

def DBW_infant2(age):
    return 0.5*age + 3

def DBW_children(age):
    return age*2 + 8

def DBW_adults_BMI(height):
    return 22*((height/100)**2)

def DBW_adults_Tannhauser(height): 
    return round(0.9*(height - 100))

''' def DBW_adults_adopted(height_ft, height_in):
    total_height_in = height_ft*12 + height_in
    return 106 + 5*(total_height_in - 60)
        
def DBW_adults_Hamwi(height_ft, height_in, sex):
    total_height_in = height_ft*12 + height_in
    if sex == 'Male':
        return 106 + 6*(total_height_in - 60)
    if sex == 'Female':
        return 100 + 5*(total_height_in - 60)''' # check if these methods are commonly used.

# --- TER functions ---

def TER_infant(age, DBW):
    if age <= 6:
        return DBW*95
    else:
        return DBW*80

def TER_children_NarinsWeil(age):
    return 1000 + 100*age

def TER_children_adolescents_CBMRG(age, DBW):
    if age > 15:
        return DBW*50
    elif age > 12:
        return DBW*60
    elif age > 9:
        return DBW*70
    elif age > 6:
        return DBW*80
    elif age > 3:
        return DBW*90
    else:
        return DBW*100
    
def TER_children_adolescents_PDRI(age, DBW, sex):
    if sex == "Male":
        if age > 15:
            return DBW*51
        elif age > 12:
            return DBW*56
        elif age > 9:
            return DBW*62
        elif age > 5:
            return DBW*70
        elif age > 2:
            return DBW*77
        else:
            return DBW*83
        
    if sex == "Female":
        if age > 15:
            return DBW*44
        elif age > 12:
            return DBW*74
        elif age > 9:
            return DBW*65
        elif age > 5:
            return DBW*55
        elif age > 2:
            return DBW*47
        else:
            return DBW*44

def TER_adults_Cooper(DBW, PAL, sex):
    PAL_factor = {"Bed rest": .10,
        "Sedentary": .30,
        "Light": .50,
        "Moderate": .75,
        "Heavy": 1.00
    }
    BMN_factor = {"Male": 1.0, "Female": 0.9}
    BMN = BMN_factor.get(sex, 1.0) * DBW * 24
    return BMN + PAL_factor.get(PAL, 10)*BMN

def TER_adults_Krause(DBW, PAL):
    PAL_factor = {"Bed rest": 27.5,
        "Sedentary": 30,
        "Light": 35,
        "Moderate": 40,
        "Heavy": 45
    }
    return DBW * PAL_factor.get(PAL, 30)

def TER_adults_PAGAC(DBW, PAL):
    PAL_factor = {"Sedentary": 30,
        "Light": 35,
        "Moderate": 40,
        "Very active/Vigorous": 45
    }
    return DBW * PAL_factor.get(PAL, 30)

def TER_adults_HarrisBenedict(age, weight, height, sex):
    if sex == "Male":
        return 66.47 + 13.75*weight + 5*height - 6.75*age
    if sex == "Female":
        return 655.1 + 9.56*weight + 1.85*height - 4.67*age
    
def TER_adults_MifflinStJeor(age, weight, height, sex):
    if sex == "Male":
        return 9.99*weight + 6.25*height -4.92*age + 5
    if sex == "Female":
        return 9.99*weight + 6.25*height -4.92*age - 161

def TER_adults_Oxford(age, weight, sex, PAL):
    if sex == "Male":
        if age > 69:
            BMR = 13.7*weight + 481
        elif age > 59:
            BMR = 13*weight + 567 
        elif age > 30:
            BMR = 14.2*weight + 593
        else:
            BMR = 16*weight + 545
    if sex == "Female":
        if age > 69:
            BMR = 10*weight + 577
        elif age > 59:
            BMR = 10.2*weight + 572 
        elif age > 30:
            BMR = 9.74*weight + 694
        else:
            BMR = 13.1*weight + 558
        
    PAL_factors_male = {"Sedentary": 1.3,
                         "Light": 1.58,
                         "Moderate": 1.67,
                         "Heavy": 1.88
    }

    PAL_factors_female = {"Sedentary": 1.3,
                         "Light": 1.45,
                         "Moderate": 1.55,
                         "Heavy": 1.75
    }

    if sex == "Male":
        return BMR * PAL_factors_male.get(PAL, 1.3)
    if sex == "Female":
        return BMR * PAL_factors_female.get(PAL, 1.3)



