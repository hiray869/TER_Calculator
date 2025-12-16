import TER_functions as ter

# --- DBW ----
x = ter.DBW_adults_BMI(160)
print(x)

x = ter.DBW_adults_Tannhauser(160)
print(x)

# --- TER --- 

x = ter.TER_infant(10,13)
print(x)

x = ter.TER_children_NarinsWeil(6)
print(x)

x = ter.TER_children_adolescents_CBMRG(6, 20)
print(x)

x = ter.TER_children_adolescents_PDRI(6, 20, "Male")
print(x)

x = ter.TER_adults_Cooper(50, "Moderate", "Male")
print(x)

x = ter.TER_adults_PAGAC(50, "Moderate")
print(x)

x = ter.TER_adults_Oxford(30, 50, "Male", "Moderate")
y = ter.TER_adults_HarrisBenedict(30, 50, 155, "Male", "Moderate")
z = ter.TER_adults_MifflinStJeor(30, 50, 155, "Male", "Moderate")

print("")
print(x)
print(y)
print(z)

x = ter.TER_adults(30, 50, "Male", "Moderate")
print(x)