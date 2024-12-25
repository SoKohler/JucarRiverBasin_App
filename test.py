import openpyxl

# Charger le fichier Excel
workbook = openpyxl.load_workbook("data_initial.xlsx")

# Sélectionner la feuille sur laquelle travailler
sheet = workbook["Demandas"]

# Spécifiez le nom de la colonne
column_name = "QecolAlar"  # Remplacez par le nom de votre colonne

# Rechercher la colonne correspondant au nom (ligne 2)
column_letter = None
for col in sheet.iter_cols(min_row=2, max_row=2):  # Itérer sur la ligne 2
    if col[0].value == column_name:  # Si la valeur correspond au nom de la colonne
        column_letter = col[0].column_letter  # Obtenir la lettre de la colonne
        break

if column_letter is None:
    print(f"Colonne avec le nom '{column_name}' non trouvée.")
else:
    # Modifier les valeurs en dessous de la ligne 2
    for row in range(3, sheet.max_row + 1):  # Commence à la ligne 3
        cell = sheet[f"{column_letter}{row}"]
        cell.value = 2  # Remplacez par la valeur souhaitée

    # Enregistrer les modifications dans un nouveau fichier
    workbook.save("data.xlsx")
    print("Les valeurs ont été mises à jour.")
