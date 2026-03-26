def debugprints(df, input_user, quatscheingabe) :
    gesamt_k_fest = ((df["netz_bezug"]).sum()*input_user.general_info.eprice)-((df["netz_einspeisung"]).sum())*0.0778
    gesamt_k_flex = -(df['ges_price']).sum()
    #speicher_nutz = (df["speicher_stand"]
    print("Haushalt: ", (df["household"]).sum())
    print("Einspeisung: ", (df["netz_einspeisung"]).sum())
    print("Netzbezug", (df["netz_bezug"]).sum())
    print("Gesamtkosten mit felxiblem Preis", gesamt_k_flex)
    print("Gesamtkosten mit Festpreis :", gesamt_k_fest)
    print("Ersparnis mit flexiblem Strompreis:",gesamt_k_fest - gesamt_k_flex)
    if quatscheingabe :
                print("sie sind dumm")
    print("Speichernutzung: ", )