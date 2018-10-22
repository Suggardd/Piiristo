import cmath
import math
import ikkunasto as ik
import piiristo as psto

PI = 3.142
kertoimet = ["y", "z", "a", "f", "p", "n", "u", "m", " ", "k", "M", "G", "T", "P", "E", "Z", "Y"]
muuntimet = {
'y':10**(-24), 
'z':10**(-21), 
'a':10**(-18), 
'f':10**(-15), 
'p':10**(-12), 
'n':10**(-9),
'u':10**(-6),
'm':10**(-3),
'k':10**3,
'M':10**6,
'G':10**9,
'T':10**12,
'P':10**15,
'E':10**18,
'Z':10**21,
'Y':10**24,}

tila = {
    "syote": None,
    "laatikko": None,
    "piiri": None,
    "komponentit": [],
    "impedanssit": [],
    "reaktanssit": [],
    "sarja": 0,
    "reaktanssi": 0,
    "tyyppi": None,
    "jannite": 0,
    "taajuus": 0,
}
def luo_haara():
    ik.avaa_viesti_ikkuna("VIRHE!", "Ei saatu tätä toimimaan", True)
def muuta_osoitinmuotoon(impedanssi):
    """
    Lukee kompleksiluvun syötekentästä ja muuttaa sen osoitinmuotoon,
    jossa osoittimen kulma on esitetty asteina. 
    Kompleksiluku sekä sen osoitinmuoto tulostetaan käyttöliittymässä olevaan tekstilaatikkoon.
    """

    try:
        if isinstance(impedanssi, complex):
            osoitinmuoto = cmath.polar(impedanssi)
            r, phi = osoitinmuoto
            asteet = math.degrees(phi)
            osoitinmuoto = "{eka:.3f} > {toka:.3f}".format(eka=r, toka=asteet)
            tuloste = "Piirin kokonaisimpedanssi on: {}".format(osoitinmuoto)
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], tuloste)
        else:
            ik.avaa_viesti_ikkuna("VIRHE", "Syöte ei ollut kelvollinen kompleksiluku", True)
    except ValueError:
        ik.avaa_viesti_ikkuna("VIRHE", "Syöte ei ollut kelvollinen kompleksiluku", True)

def laske_reaktanssi():
    """
    Laskee piiriin sarjaankytkettyjen kelojen ja kondensaattoreiden kokonaisreaktanssin
    
    """
    tila["reaktanssi"] = sum(float(i) for i in tila["reaktanssit"])
    ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Sarjaankytkennän reaktanssi on {} ohmia.".format(tila["reaktanssi"]))

def laske_impedanssi():
    """
    Muuntaa piirin impedanssin kompleksimuotoon, kutsuu muuta_ositinmuotoon funktiota joka tulostaa kok.impedanssin osoitinmuodossa
    
    """
    impedanssi = complex(tila["sarja"], tila["reaktanssi"])
    muuta_osoitinmuotoon(impedanssi)

def laske_sarja():
    """
    Laskee piirin komponenttien sarjaankytkennän kok.resistanssin
    
    """
    tila["sarja"] = sum(float(i) for i in tila["impedanssit"])
    ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Sarjaankytkennän resistanssi on {} ohmia.".format(tila["sarja"]))

def laske_rinnan():
    """
    Laskee piirin komponenttien rintaankytkennän kok.resistanssin
    
    """
    kaanteisarvot = []
    arvot_pituus = len(tila["impedanssit"])
    try:
        for i in range(arvot_pituus):
            kaanteinen = (1/float(tila["impedanssit"[i-1]]))
            kaanteisarvot.append(kaanteinen)
        rinnan = 1/sum(float(i) for i in kaanteisarvot)
        return rinnan
    except ZeroDivisionError:
        print("Komponentin arvon on oltava nollaa suurempi luku")

def piirra_piiri():
    """
    Piirtää annettujen tietojen pohjalta piirin
    """
    psto.tyhjaa_piiri(tila["piiri"])
    psto.piirra_jannitelahde(tila["piiri"], tila["jannite"], tila["taajuus"])
    psto.piirra_haara(tila["piiri"], tila["komponentit"], 3, 2)
    psto.piirra_piiri(tila["piiri"])
    laske_sarja()
    laske_reaktanssi()
    laske_impedanssi()
    

def tallenna_tyyppi(tyyppi):
    """
    Tallentaa syötetyn komponenttityypin sanakirjan tyyppi-muuttujaan impedanssilaskuja varten
    """
    if tyyppi == 'r':
        ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Komponentin tyyppi on vastus")
        tila["tyyppi"] = 'r'
    elif tyyppi == 'l':
        ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Komponentin tyyppi on kela")
        tila["tyyppi"] = 'l'
    elif tyyppi == 'c':
        ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Komponentin tyyppi on kondensaattori")
        tila["tyyppi"] = 'c'
        
def laske_arvo():
    """
    Laskee impedanssin eri komponenttityypeille, tallentaa ne sanakirjan komponentit-listaan
    ja kutsuu piirtämisfunktiota
    """
    try:
        arvo = float(ik.lue_kentan_sisalto(tila["syote"]))
        tyyppi = tila["tyyppi"]
        ik.tyhjaa_kentan_sisalto(tila["syote"])
        if tyyppi == 'r':
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Vastuksen impedanssi on {ohmi:.2f} ohmia.".format(ohmi=arvo))
            tila["komponentit"].append((tyyppi, arvo))
            tila["impedanssit"].append(arvo)
            piirra_piiri()
        elif tila["tyyppi"] == 'l':
            impedanssi = 2 * PI * tila["taajuus"] * arvo
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Kelan induktanssi taajuudella {hertsi:.2f} Hz on {ohmi:.3f} ohmia.".format(hertsi=tila["taajuus"], ohmi=impedanssi))
            tila["komponentit"].append((tyyppi, impedanssi))
            tila["reaktanssit"].append(impedanssi)
            piirra_piiri()
        elif tila["tyyppi"] == 'c':
            impedanssi = 1 / (2 * PI * float(tila["taajuus"]) * arvo)
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Kondensaattorin kapasitanssi taajuudella {hertsi:.2f} Hz on {ohmi:.3f} ohmia.".format(hertsi=tila["taajuus"], ohmi=impedanssi))
            tila["komponentit"].append((tyyppi, impedanssi))
            tila["reaktanssit"].append(impedanssi)
            piirra_piiri()
    except ValueError:
        ik.avaa_viesti_ikkuna("VIRHE", "Syötä liukuluku!", True)
    
def aseta_jannite():
    """
    Lukee liukulukuarvon syötekentästä ja asettaa sen piirin jännitelähteen jännitteeksi.
    """
    try:
        tila["jannite"] = ik.lue_kentan_sisalto(tila["syote"])
        if tila["jannite"][-1].isdigit():
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Jännite: {} V".format(float(tila["jannite"])))
        else:
            tila["jannite"] = muuta_kerrannaisyksikko(tila["jannite"])
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Jännite: {} V".format(float(tila["jannite"])))
    except TypeError:
        ik.avaa_viesti_ikkuna("VIRHE", "Syöte ei ollut kelvollinen", True)
    ik.tyhjaa_kentan_sisalto(tila["syote"])

def aseta_taajuus():
    """
    Lukee liukulukuarvon syötekentästä ja asettaa sen piirin jännitelähteen taajuudeksi.
    """
    try:
        tila["taajuus"] = ik.lue_kentan_sisalto(tila["syote"])
        if tila["taajuus"][-1].isdigit():
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Taajuus: {} Hz".format(float(tila["taajuus"])))
        else:
            tila["taajuus"] = muuta_kerrannaisyksikko(tila["taajuus"])
            ik.kirjoita_tekstilaatikkoon(tila["laatikko"], "Taajuus: {} Hz".format(float(tila["taajuus"])))
    except TypeError:
        ik.avaa_viesti_ikkuna("VIRHE", "Syöte ei ollut kelvollinen", True)
    ik.tyhjaa_kentan_sisalto(tila["syote"])
    
def valitse_tyyppi():
    """
    Tarkastaa syötteestä, mitä tyyppiä komponentti on
    """
    tyyppi = ik.lue_kentan_sisalto(tila["syote"])
    ik.tyhjaa_kentan_sisalto(tila["syote"])
    if tyyppi.isdigit():
        ik.avaa_viesti_ikkuna("VIRHE", "Komponentti voi olla vastus(r), kela(l) tai kondensaattori(c)!", True)
    elif len(tyyppi) > 1:
        if tyyppi == 'aasisvengaa':
            ik.avaa_viesti_ikkuna("Vanha vitsi!", "Aasi ei svengaa.", True)
        ik.avaa_viesti_ikkuna("VIRHE", "Komponentti voi olla vastus(r), kela(l) tai kondensaattori(c)!", True)
    elif tyyppi == 'r' or 'l' or 'c':
        tallenna_tyyppi(tyyppi)
    else:
        ik.avaa_viesti_ikkuna("VIRHE", "Komponentti voi olla vastus(r), kela(l) tai kondensaattori(c)!", True)
        
def muuta_kerrannaisyksikko(muutettava):
    """
    Muuttaa annetun luvun ja mahdollisen kerrannaisyksikön vastaavaksi liukuluvuksi.
    """
    kerroin_pituus = len(kertoimet)
    try:
        arvo = float(muutettava[0:-1])
        yksikko = muutettava[-1]
        for i in range(kerroin_pituus):
            if yksikko in kertoimet:
                muunnettu = arvo*muuntimet[yksikko]
                if muunnettu is None:
                    print("Arvo ei ole kelvollinen")
                else:
                    return muunnettu 
    except ValueError:
        print("Arvo ei ole kelvollinen")
    
    
def main():
    """
    Luo käyttöliittymäikkunan, jossa on vasemmalla puolella syötekenttä numeroarvoille, 
    neljä nappia ja tekstilaatikko. Oikealla puolella on piirikaaviokuva.
    """
    ikkuna = ik.luo_ikkuna("Piiri pieni pyörii")
    vasen_kehys = ik.luo_kehys(ikkuna, ik.VASEN)
    oikea_kehys = ik.luo_kehys(ikkuna, ik.OIKEA)
    tk_otsikko = ik.luo_tekstirivi(vasen_kehys, "arvo:")
    tila["syote"] = ik.luo_tekstikentta(vasen_kehys)
    jannitenappi = ik.luo_nappi(vasen_kehys, "aseta jännite", aseta_jannite)
    taajuusnappi = ik.luo_nappi(vasen_kehys, "aseta taajuus", aseta_taajuus)
    haaranappi = ik.luo_nappi(vasen_kehys, "luo uusi haara", luo_haara)
    komponenttinappi = ik.luo_nappi(vasen_kehys, "anna komponentin tyyppi", valitse_tyyppi)
    arvonappi = ik.luo_nappi(vasen_kehys, "anna komponentin arvo", laske_arvo)
    lopetusnappi = ik.luo_nappi(vasen_kehys, "quit", ik.lopeta)
    tila["laatikko"] = ik.luo_tekstilaatikko(vasen_kehys, 50, 40)
    tila["piiri"] = psto.luo_piiri(oikea_kehys, 700, 700, 10)
    ik.kaynnista()
    
if __name__ == "__main__":
    main()