def speicher_laden(saldo, speicher_kap, speicher_letzt):
    ueberschuss = -saldo
    freier_platz = speicher_kap - speicher_letzt

    if ueberschuss * 0.98 <= freier_platz:
        return speicher_letzt + ueberschuss * 0.98, 0, 0

    return speicher_kap, ueberschuss - freier_platz / 0.98, 0


def speicher_entladen(saldo, speicher_kap, speicher_letzt):
    mindeststand = speicher_kap * 0.1
    nutzbar = max(0, speicher_letzt - mindeststand)

    if saldo <= nutzbar:
        return speicher_letzt - saldo, 0, 0

    return speicher_letzt - nutzbar, 0, saldo - nutzbar


def speicher(saldo, speicher_kap, speicher_letzt):
    if saldo > 0:
        return speicher_entladen(saldo, speicher_kap, speicher_letzt)
    elif saldo < 0:
        return speicher_laden(saldo, speicher_kap, speicher_letzt)
    return speicher_letzt, 0, 0

