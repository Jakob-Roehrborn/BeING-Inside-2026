def berechne_stromkosten_nach_14a(df):
    import numpy as np
    
    # Prüfen, ob Wärmepumpe/E-Auto überhaupt in der Tabelle existieren
    heat_pump_val = df['heat_pump'] if 'heat_pump' in df.columns else 0
    ecar_val = df['ecar'] if 'ecar' in df.columns else 0
    
    # Anteil der steuerbaren Verbraucher am stündlichen Gesamtverbrauch berechnen
    # .fillna(0) fängt den Fehler ab, falls der Gesamtverbrauch in einer Stunde 0 ist
    fraction_steuerbar = (heat_pump_val + ecar_val) / df['total_consumption']
    fraction_steuerbar = fraction_steuerbar.fillna(0)
    
    # Tatsächlichen Netzbezug aufteilen
    netz_bezug_steuerbar = (df['netz_bezug'] * fraction_steuerbar).sum()
    netz_bezug_haushalt = (df['netz_bezug'] * (1 - fraction_steuerbar)).sum()
    verbrauch_gesamt = df['netz_bezug'].sum()

    # --- GRUNDLAGEN & PREISE (SachsenEnergie Preisblatt 01/2026) ---
    mwst = 1.19
    boersenpreis_netto = 9.77  # Informatorischer Annahmewert für dynamischen Tarif in ct/kWh
    
    # Fixe Kostenbestandteile (netto in €/Jahr)
    basisgrundpreis = 70.44  
    grundpreis_netz = 30.00  
    messstelle_imsys = 42.02 # iMSys mit steuerbarer Einrichtung
    
    # Variable Kostenbestandteile (netto in ct/kWh)
    basisverbrauchspreis = 2.50 
    ap_netz_slp = 9.29          # Arbeitspreis Netznutzung
    konzession = 1.32           # Annahme: Gemeinde bis 25.000 Einwohner
    kwkg_umlage = 0.446         
    aufschlag_netz = 1.559      
    offshore = 0.941            
    stromsteuer = 2.05          
    
    # Summe der staatlichen Umlagen, Abgaben und Steuern (netto)
    umlagen_summe_ct = basisverbrauchspreis + konzession + kwkg_umlage + aufschlag_netz + offshore + stromsteuer
    
    # Regulärer Arbeitspreis (brutto in €/kWh)
    ap_standard_netto = umlagen_summe_ct + ap_netz_slp + boersenpreis_netto
    ap_standard_brutto = (ap_standard_netto * mwst) / 100
    
    # --- BERECHNUNG MODUL 1 (Gemeinsamer Zähler) ---
    fixkosten_modul1_brutto = (basisgrundpreis + grundpreis_netz + messstelle_imsys) * mwst
    rabatt_modul1_brutto = 80.00 + (3750 * ap_netz_slp * 0.2) / 100
    
    kosten_modul1 = fixkosten_modul1_brutto + (verbrauch_gesamt * ap_standard_brutto) - rabatt_modul1_brutto
    
    # --- BERECHNUNG MODUL 2 (Separater Zähler) ---
    # Haushaltsstrom (Standardtarif, über Haushaltszähler)
    kosten_haushalt_m2 = fixkosten_modul1_brutto + (netz_bezug_haushalt * ap_standard_brutto)
    
    # Anlagenstrom (Zweiter Zähler: kein Netz-Grundpreis, aber eigener Messstellen- und Basisgrundpreis)
    fixkosten_anlage_brutto = (basisgrundpreis + messstelle_imsys) * mwst
    ap_netz_reduziert = ap_netz_slp * 0.4  # AP Netznutzung auf 40% reduziert
    ap_anlage_netto = umlagen_summe_ct + ap_netz_reduziert + boersenpreis_netto
    ap_anlage_brutto = (ap_anlage_netto * mwst) / 100
    
    kosten_anlage_m2 = fixkosten_anlage_brutto + (netz_bezug_steuerbar * ap_anlage_brutto)
    
    kosten_modul2 = kosten_haushalt_m2 + kosten_anlage_m2
    
    # --- AUSGABE ---
    print(f"\n--- STROMKOSTENVERGLEICH §14a EnWG (basierend auf Simulation) ---")
    print(f"Netzbezug Gesamt:        {verbrauch_gesamt:.2f} kWh")
    print(f"  davon Haushalt:        {netz_bezug_haushalt:.2f} kWh")
    print(f"  davon Steuerbar:       {netz_bezug_steuerbar:.2f} kWh")
    print("-" * 65)
    print(f"Kosten Modul 1 (Pauschale, 1 Zähler): {kosten_modul1:.2f} €/Jahr")
    print(f"  Davon abgesetzter Rabatt:          -{rabatt_modul1_brutto:.2f} €")
    print(f"Kosten Modul 2 (Prozentual, 2 Zähler):{kosten_modul2:.2f} €/Jahr")
    print("-" * 65)
    
    if kosten_modul1 < kosten_modul2:
        differenz = kosten_modul2 - kosten_modul1
        print(f"=> Modul 1 ist um {differenz:.2f} € günstiger.")
    else:
        differenz = kosten_modul1 - kosten_modul2
        print(f"=> Modul 2 ist um {differenz:.2f} € günstiger.")

    return kosten_modul1, kosten_modul2

# ---------------------------------------------------------
# Fügen Sie diesen Aufruf ganz unten an Ihre main.py an:
