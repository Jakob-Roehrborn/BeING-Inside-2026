def berechne_stromkosten_nach_14a_dynamisch(df, df_prices):
    import numpy as np
    import pandas as pd
    csv_path_zusatz = "material/zusatzkosten_gesamt_2025_sachsennetze_sachsenenergie_stunden.csv"
    df_zusatz = pd.read_csv(csv_path_zusatz)
    df_module = pd.DataFrame()

    # 1. Stündliche Aufteilung des Netzbezugs
    heat_pump_val = df.get('heat_pump', 0)
    ecar_val = df.get('ecar', 0)
    
    fraction_steuerbar = (heat_pump_val + ecar_val) / df['total_consumption']
    fraction_steuerbar = fraction_steuerbar.fillna(0)
    
    # Stündliche Vektoren (Arrays) für den Netzbezug
    netz_bezug_steuerbar_std = df['netz_bezug'] * fraction_steuerbar
    netz_bezug_haushalt_std = df['netz_bezug'] * (1 - fraction_steuerbar)
    
    # Echter stündlicher Bruttopreis in €/kWh (aus Ihrer CSV)
    ap_standard_brutto_std = df_prices['customer_price_gross_ct_per_kwh_konzession_1_32'] / 100
    # --- PREISE (SachsenEnergie Preisblatt 01/2026) ---
    mwst = 1.19
    ap_netz_slp = 9.29 # Arbeitspreis Netznutzung in ct/kWh (netto)
    
    # Fixe Kosten (netto in €/Jahr)
    basisgrundpreis = 70.44  
    grundpreis_netz = 30.00  
    messstelle_imsys = 42.02 
    
    # --- BERECHNUNG MODUL 1 (Gemeinsamer Zähler) ---
    fixkosten_modul1_brutto = (basisgrundpreis + grundpreis_netz + messstelle_imsys) * mwst
    rabatt_modul1_brutto = 80.00 + (3750 * ap_netz_slp * 0.2) / 100
    anteil_fixkosten_std_m1 = (fixkosten_modul1_brutto - rabatt_modul1_brutto) / 8760
    
    # Stündliche Verbrauchskosten aufsummieren
    verbrauchskosten_gesamt = (df['netz_bezug'] * ap_standard_brutto_std).sum()
    kosten_modul1 = fixkosten_modul1_brutto + verbrauchskosten_gesamt - rabatt_modul1_brutto
    
    # --- BERECHNUNG MODUL 2 (Separater Zähler) ---
    # Haushaltsstromkosten
    rabatt_netzentgelt_m2_euro = (ap_netz_slp * 0.6 * mwst) / 100 
    ap_anlage_brutto_std = ap_standard_brutto_std - rabatt_netzentgelt_m2_euro
    fixkosten_anlage_brutto = (basisgrundpreis + messstelle_imsys) * mwst

    # --- BERECHNUNG MODUL 3 (Zeitvariable Netzentgelte + Modul 1) ---
    # Variable Kosten (brutto): Spotpreis + Summe aller stündlichen Nebenkosten (inkl. zeitabhängigem Netzentgelt)
    ap_modul3_brutto_std_ct = (df_prices['spot_price_ct_per_kwh'] * mwst) + df_zusatz['summe_variable_nebenkosten_ohne_boersenpreis_ct_per_kwh']
    
    # Fixkosten (brutto): Die pre-kalkulierten stündlichen Fixkosten (inkl. Modul 1 Rabatt)
    fixkosten_modul3_brutto_std = df_zusatz['summe_fixkosten_eur_per_hour_ohne_optionale_einmalkosten'] * mwst
    

    df_module["Modul1"] = (df['netz_bezug'] * ap_standard_brutto_std) + anteil_fixkosten_std_m1
    kosten_modul1_gesamt = df_module['Modul1'].sum()-(0.0778*df['netz_einspeisung'].sum())
    df_module["Modul2"] = ((netz_bezug_haushalt_std * ap_standard_brutto_std) + (fixkosten_modul1_brutto / 8760)) + \
                          ((netz_bezug_steuerbar_std * ap_anlage_brutto_std) + (fixkosten_anlage_brutto / 8760))
    kosten_modul2_gesamt = df_module['Modul2'].sum()-(0.0778*df['netz_einspeisung'].sum())

    
    # NEU: Eigene Spalte für Modul 3 pro Stunde
    df_module["Modul3"] = (df['netz_bezug'] * ap_modul3_brutto_std_ct / 100) + fixkosten_modul3_brutto_std

    kosten_modul3_gesamt = df_module['Modul3'].sum()-(0.0778*df['netz_einspeisung'].sum())

    # --- AUSGABE ---
    print(f"\n--- DYNAMISCHER STROMKOSTENVERGLEICH (INKL. MODUL 3) ---")
    print(f"Netzbezug Gesamt:        {df['netz_bezug'].sum():.2f} kWh")
    print(f"  davon Haushalt:        {netz_bezug_haushalt_std.sum():.2f} kWh")
    print(f"  davon Steuerbar:       {netz_bezug_steuerbar_std.sum():.2f} kWh")
    print("-" * 60)
    print(f"Kosten Modul 1 (Pauschale):          {kosten_modul1_gesamt:.2f} €/Jahr")
    print(f"Kosten Modul 2 (Prozentual, 2 Zähler):{kosten_modul2_gesamt:.2f} €/Jahr")
    print(f"Kosten Modul 3 (Zeitvariabel):       {kosten_modul3_gesamt:.2f} €/Jahr")
    print("-" * 60)
    
    guenstigstes = min(kosten_modul1_gesamt, kosten_modul2_gesamt, kosten_modul3_gesamt)
    if guenstigstes == kosten_modul1_gesamt:
        guenstig_m = 1
        ersparnis = kosten_modul2_gesamt - kosten_modul1_gesamt
    elif guenstigstes == kosten_modul2_gesamt:
        ersparnis = kosten_modul1_gesamt - kosten_modul2_gesamt
        guenstig_m = 2
    else:
        ersparnis = kosten_modul1_gesamt - kosten_modul3_gesamt
        guenstig_m = 3
    df_module.to_csv('model.csv', index=False)
    return df_module, netz_bezug_steuerbar_std.sum(), guenstig_m, ersparnis
