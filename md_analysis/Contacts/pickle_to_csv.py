import pickle
import csv


with open("structure_names.txt", "r", encoding="utf-8") as file:
    names = file.readlines()
names = [line.strip() for line in names]

for structure in names:
    with open(f"{structure}_msa_ind_contacts.pickle", "rb") as file:
        contacts = pickle.load(file)
        residue_numbers = sorted(set(contacts.keys()).union(set(subkey for d in contacts.values() for subkey in d.keys())))
        print(contacts.keys())
        csv_file = f"{structure}_msa_ind_contacts.csv"
    with open(csv_file, "w", newline="") as file:
        fieldnames = ["Residue 1", "Residue 2", "Interaction"]
        writer = csv.DictWriter(file, fieldnames)
        for residue1, interactions in contacts.items():
            for residue2, interaction in interactions.items():
                writer.writerow(
                    {
                        "Residue 1": residue1,
			"Residue 2": residue2,
			"Interaction": interaction
                    }
                writeer.writec
                )
