# -- DBW functions --- 

# infants
def DBW_infant1(weight, age):
    if age <= 6:
        DBW = weight + age*600
    else:
        DBW = weight + age*500
    return DBW/1000

def DBW_infant2(age):
    return 0.5*age + 3

# children
def DBW_children(age):
    return age*2 + 8

# adults
def DBW_adults_BMI(height):
    return 22*((height/100)**2)

def DBW_adults_Tannhauser(height): 
    return round(0.9*(height - 100))

'''
def DBW_adults_adopted(height_ft, height_in):
    total_height_in = height_ft*12 + height_in
    return 106 + 5*(total_height_in - 60)
        
def DBW_adults_Hamwi(height_ft, height_in, sex):
    total_height_in = height_ft*12 + height_in
    if sex == 'Male':
        return 106 + 6*(total_height_in - 60)
    if sex == 'Female':
        return 100 + 5*(total_height_in - 60)
''' # check if these methods are commonly used.

# --- TER functions ---

# infants (This method is based on REI, PDRI (2015))
def TER_infant(age, DBW): # age in months
    if age <= 6:
        return DBW*95
    else:
        return DBW*80

# children and adoloescents
def TER_children_NarinsWeil(age):
    return 1000 + 100*age

def TER_children_adolescents_CBMRG(age, DBW):
    constants = [
    (15, 50),
    (12, 60),
    (9,  70),
    (6,  80),
    (3,  90),
    (0, 100)
    ]
    for min_age, k in constants:
        if age > min_age:
            TER = DBW * k
    return TER, k

def TER_children_adolescents_PDRI(age, DBW, sex):
    constants = {
    "Male": [
        (15, 51),
        (12, 56),
        (9,  62),
        (5,  70),
        (2,  77),
        (0,  83),
    ],
    "Female": [
        (15, 44),
        (12, 74),
        (9,  65),
        (5,  55),
        (2,  47),
        (0,  44),
    ]
    }
    for min_age, k in constants[sex]:
        if age > min_age:
            TER = DBW*k
    return TER, k

# adults
def TER_adults_Cooper(DBW, PAL, sex):
    PAL_factor = {"Bed rest": .10,
        "Sedentary": .30,
        "Light": .50,
        "Moderate": .75,
        "Heavy": 1.00,
        "Very active/Vigorous": 1.00 # assumed
    }
    BMR_factor = {"Male": 1.0, "Female": 0.9}
    BMR = BMR_factor.get(sex, 1.0) * DBW * 24
    PA = PAL_factor.get(PAL, .10)*BMR
    TER = BMR + PA
    return TER, BMR, PA, BMR_factor.get(sex), PAL_factor.get(PAL)

def TER_adults_Krause(DBW, PAL):
    PAL_factor = {"Bed rest": 27.5,
        "Sedentary": 30,
        "Light": 35,
        "Moderate": 40,
        "Heavy": 45,
        'Very active/Vigorous': 45 # assumed
    }
    return DBW * PAL_factor.get(PAL, 30), PAL_factor.get(PAL)

def TER_adults_PAGAC(DBW, PAL):
    PAL_factor = {"Sedentary": 30,
        "Light": 35,
        "Moderate": 40,
        "Heavy": 42.5, # assumed 
        "Very active/Vigorous": 45
    }
    return DBW * PAL_factor.get(PAL, 30), PAL_factor.get(PAL)


# PAL factors for the following methods
PAL_factors_male = {"Sedentary": 1.3,
                        "Light": 1.58,
                        "Moderate": 1.67,
                        "Heavy": 1.88,
                        "Very active/Vigorous": 1.88 # assumed
}

PAL_factors_female = {"Sedentary": 1.3,
                        "Light": 1.45,
                        "Moderate": 1.55,
                        "Heavy": 1.75, 
                        "Very active/Vigorous": 1.75 #assumed
}

def TER_adults_HarrisBenedict(age, weight, height, sex, PAL):
    if sex == "Male":
        BMR = 66.47 + 13.75*weight + 5*height - 6.75*age
        PAL_factor = PAL_factors_male.get(PAL)
    if sex == "Female":
        BMR = 655.1 + 9.56*weight + 1.85*height - 4.67*age
        PAL_factor = PAL_factors_female.get(PAL)
    TER = BMR*PAL_factor
    return TER, BMR, PAL_factor
    
def TER_adults_MifflinStJeor(age, weight, height, sex, PAL):
    if sex == "Male":
        BMR = 9.99*weight + 6.25*height -4.92*age + 5
        PAL_factor = PAL_factors_male.get(PAL)
    if sex == "Female":
        BMR = 9.99*weight + 6.25*height -4.92*age - 161
        PAL_factor = PAL_factors_female.get(PAL)
    TER = BMR*PAL_factor
    return TER, BMR, PAL_factor

def TER_adults_Oxford(age, weight, sex, PAL):
    constants = {
    "Male": [
        (69, 13.7, 481),
        (59, 13.0, 567),
        (30, 14.2, 593),
        (0,  16.0, 545),
    ],
    "Female": [
        (69, 10.0, 577),
        (59, 10.2, 572),
        (30, 9.74, 694),
        (0,  13.1, 558),
    ]
}
    for min_age, a, b in constants[sex]:
        if age > min_age:
            BMR = a * weight + b
            break
    if sex == "Male":
        PAL_factor = PAL_factors_male.get(PAL, 1.3)
    else:
        PAL_factor = PAL_factors_female.get(PAL, 1.3)
    TER = BMR * PAL_factor
    return TER, BMR, PAL_factor, a, b


