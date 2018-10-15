"""
ikkunasto - yksinkertainen kÃ¤yttÃ¶liittymÃ¤kirjasto 

@author Mika Oja, Oulun yliopisto

TÃ¤mÃ¤ kirjasto sisÃ¤ltÃ¤Ã¤ nipun funktioita, joilla opiskelijat voivat toteuttaa
yksinkertaisen kÃ¤yttÃ¶liittymÃ¤n, jossa hyÃ¶dynnetÃ¤Ã¤n matplotlib-kirjastoa 
kuvaajien piirtÃ¤miseen. Kirjasto sisÃ¤ltÃ¤Ã¤ paljon oletusratkaisuja, jotta 
opiskelijoiden ei tarvitse opetella kokonaista kÃ¤yttÃ¶liittymÃ¤kirjastoa, eikÃ¤
paneutua sellaisen yksityiskohtiin. TÃ¤stÃ¤ syystÃ¤ kÃ¤yttÃ¶liittymien toteutuksessa
voi kuitenkin tulla rajoja vastaan. 

Kirjasto on rakennettu Pythonin mukana tulevan TkInterin pÃ¤Ã¤lle. LisÃ¤tietoa 
lÃ¶ytyy mm. tÃ¤Ã¤ltÃ¤: 

https://docs.python.org/3/library/tk.html

Erityisen huomattavaa on, ettÃ¤ Tk hoitaa pÃ¤Ã¤asiassa automaattiseti elementtien
sijoittelun (perustuen siihen missÃ¤ kehyksissÃ¤ ne ovat), mutta kuvaaja- ja 
tekstilaatikoiden koko mÃ¤Ã¤ritetÃ¤Ã¤n staattisesti - niiden ulottuvuudet siis 
sanelevat aika pitkÃ¤lti miltÃ¤ kÃ¤yttÃ¶liittymÃ¤ nÃ¤yttÃ¤Ã¤. Jos siis haluat 
siistimmÃ¤n nÃ¤kÃ¶isen kÃ¤yttÃ¶liittymÃ¤n, kannattaa kokeilla sÃ¤Ã¤tÃ¤Ã¤ nÃ¤iden kokoja.

Kirjaston pÃ¤Ã¤ohjelmasta lÃ¶ydÃ¤t pienen esimerkkikoodin, josta saat jonkinlaisen
kÃ¤sityksen siitÃ¤ miten tÃ¤tÃ¤ kirjastoa kÃ¤yttÃ¤mÃ¤llÃ¤ luodaan kÃ¤yttÃ¶liittymÃ¤n 
peruselementtejÃ¤. 
"""

import matplotlib
matplotlib.use("TkAgg")

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

VASEN = LEFT
OIKEA = RIGHT
YLA = TOP
ALA = BOTTOM

def luo_ikkuna(otsikko): 
    """
    Luo ikkunan kÃ¤yttÃ¶liittymÃ¤Ã¤ varten. Ikkuna toimii kaiken pohjana, joten 
    tÃ¤tÃ¤ funktiota pitÃ¤Ã¤ kutsua ennen kuin muita voidaan kÃ¤yttÃ¤Ã¤. 
    
    :param str otsikko: ikkunan otsikko
    :return: palauttaa luodun ikkunaobjektin
    """
    
    global ikkuna
    ikkuna = Tk()
    ikkuna.wm_title(otsikko)
    return ikkuna
    
def luo_kehys(isanta, puoli=VASEN):
    """
    Luo kehyksen, johon voidaan asetella muita elementtejÃ¤. KehyksillÃ¤ voidaan
    jakaa kÃ¤yttÃ¶liittymÃ¤ helpommin kÃ¤siteltÃ¤viin alueisiin. NiitÃ¤ tarvitaan 
    myÃ¶s, jos halutaan asetella komponentteja muutenkin kuin yhden akselin 
    suuntaisesti. 
    
    Kehykset voivat sijaita itse ikkunassa, tai toisten kehysten sisÃ¤llÃ¤. 
    Funktion ensimmÃ¤inen parametri on siis joko ikkunaobjekti tai kehysobjekti.
    Toinen parametri vaikuttaa siihen, mihin kehys sijoitetaan. Elementit 
    pakataan aina jotain seinÃ¤Ã¤ vasten - ne siis muodostavat pinon. Jos esim. 
    pakataan kaksi kehystÃ¤ ylÃ¤laitaa vasten, ensimmÃ¤isenÃ¤ pakattu kehys on 
    ylimpÃ¤nÃ¤ ja toisena pakattu kehys sen alla. 
    
    :param widget isanta: kehys tai ikkuna, jonka sisÃ¤lle kehys sijoitetaan
    :param str puoli: mitÃ¤ isÃ¤ntÃ¤elementin reunaa vasten kehys pakataan
    :return: palauttaa luodun kehysobjektin
    """
    
    kehys = Frame(isanta)
    kehys.pack(side=puoli, anchor="n")
    return kehys
    
def luo_nappi(kehys, teksti, kasittelija):
    """
    Luo napin, jota kÃ¤yttÃ¤jÃ¤ voi painaa. Napit toimivat kÃ¤sittelijÃ¤funktioiden
    kautta. Koodissasi tulee siis olla mÃ¤Ã¤riteltynÃ¤ funktio, jota kutsutaan 
    aina kun kÃ¤yttÃ¤jÃ¤ painaa nappia. TÃ¤mÃ¤ funktio ei saa lainkaan argumentteja.
    Funktio annetaan tÃ¤lle funktiokutsulle kasittelija-argumenttina. Esim.
    
    def aasi_nappi_kasittelija():
        # jotain tapahtuu
        
    luo_nappi(kehys, "aasi", aasi_nappi_kasittelija)
    
    Napit pakataan aina kehyksensÃ¤ ylÃ¤laitaa vasten, joten ne tulevat nÃ¤kyviin
    kÃ¤yttÃ¶liittymÃ¤Ã¤n alekkain. Jos haluat asetella napit jotenkin muuten, voit
    katsoa tÃ¤mÃ¤n funktion koodista mallia ja toteuttaa vastaavan 
    toiminnallisuuden omassa koodissasi. Jos laajenna-argumentiksi annetaan 
    True, nappi kÃ¤yttÃ¤Ã¤ kaiken jÃ¤ljellÃ¤ olevan tyhjÃ¤n tilan kehyksestÃ¤Ã¤n. 
    
    :param widget kehys: kehys, jonka sisÃ¤lle nappi sijoitetaan
    :param str teksti: napissa nÃ¤kyvÃ¤ teksti
    :param function kasittelija: funktio, jota kutsutaan kun nappia painetaan
    :return: palauttaa luodun nappiobjektin
    """
    
    nappi = Button(kehys, text=teksti, command=kasittelija)
    nappi.pack(side=TOP, fill=BOTH)
    return nappi

def luo_kuvaaja(kehys, hiiri_kasittelija, leveys, korkeus):
    """
    Luo kuvaajan sekÃ¤ piirtoalueen johon se sijoitetaan. TÃ¤mÃ¤n funktion avulla
    voidaan kytkeÃ¤ matplotlib ja tÃ¤llÃ¤ kirjastolla luotu graafinen 
    kÃ¤yttÃ¶liittymÃ¤ toisiinsa - erillisen piirtoikkunan sijaan kuvaaja tulee 
    nÃ¤kyviin yhtenÃ¤ paneelina kÃ¤yttÃ¶liittymÃ¤ssÃ¤. Kuvaajan kÃ¤sittelystÃ¤ lÃ¶ydÃ¤t
    lisÃ¤tietoja matplotlibin dokumentaatiosta: 
    
    http://matplotlib.org/api/figure_api.html
    
    Funktiolle mÃ¤Ã¤ritellÃ¤Ã¤n lisÃ¤ksi kÃ¤sittelijÃ¤funktio, jota kutsutaan aina kun 
    kÃ¤yttÃ¤jÃ¤ klikkaa hiirellÃ¤ kuvaajaa. TÃ¤mÃ¤ toimii samalla tavalla kuin 
    nappien kÃ¤sittelijÃ¤t, mutta funktiolla on oltava yksi parametri. TÃ¤mÃ¤ 
    parametri saa arvoksi matplotlibiltÃ¤ objektin, jossa on tiedot 
    klikkauksesta. HyÃ¶dyllisiÃ¤ ominaisuuksia tÃ¤mÃ¤n ohjelman kannalta ovat 
    ainakin xdata ja ydata, jotka kertovat kuvaajan arvot klikatussa kohdassa, 
    sekÃ¤ button, joka kertoo mitÃ¤ hiiren nappia klikattiin (1 = vasen, 2 = 
    keski, 3 = oikea). LisÃ¤tietoja
    
    http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.MouseEvent
    
    Kuvaajalle mÃ¤Ã¤ritetÃ¤Ã¤n leveys ja korkeus pikseleinÃ¤. 
    
    :param widget kehys: kehys, jonka sisÃ¤lle kuvaaja sijoitetaan
    :param function hiiri_kasittelija: funktio, jota kutsutaan klikatessa
    :param int leveys: kuvaajan leveys pikseleinÃ¤
    :param int korkeus: kuvaajan korkeus pikseleinÃ¤
    :return: piirtoalueobjekti, kuvaajaobjekti
    """
    
    kuvaaja = Figure(figsize=(leveys / 100, korkeus / 100), dpi=100)
    piirtoalue = FigureCanvasTkAgg(kuvaaja, master=kehys)
    piirtoalue.get_tk_widget().pack(side=TOP)
    piirtoalue.mpl_connect("button_press_event", hiiri_kasittelija)
    return piirtoalue, kuvaaja
    
def luo_tekstilaatikko(kehys, leveys=80, korkeus=20):
    """
    Luo tekstilaatikon, johon voidaan kirjoittaa viestejÃ¤ samaan tapaan kuin 
    printillÃ¤ komentoriviohjelmissa. Oletuksena tekstilaatikko tÃ¤yttÃ¤Ã¤ kaiken
    vapaana olevan tilan kehyksestÃ¤Ã¤n.
    
    :param widget kehys: kehys, jonka sisÃ¤lle tekstilaatikko sijoitetaan
    :param int leveys: laatikon leveys merkkeinÃ¤
    :param int korkeus: laatikon korkeus riveinÃ¤
    :return: tekstilaatikko-objekti    
    """
    
    laatikko = Text(kehys, height=korkeus, width=leveys)
    laatikko.configure(state="disabled")
    laatikko.pack(side=TOP, expand=True, fill=BOTH)
    return laatikko

def kirjoita_tekstilaatikkoon(laatikko, sisalto, tyhjaa=False):
    """
    Kirjoittaa rivin tekstiÃ¤ valittuun tekstilaatikkoon. Tarvittaessa laatikko
    voidaan myÃ¶s tyhjentÃ¤Ã¤ ennen kirjoitusta asettamalla tyhjaa-argumentin 
    arvoksi True. 
    
    :param widget laatikko: tekstilaatikko-objekti johon kirjoitetaan
    :param str sisalto: kirjoitettava teksti
    :param bool tyhjaa: tyhjÃ¤tÃ¤Ã¤nkÃ¶ laatikko ensin
    """
    
    laatikko.configure(state="normal")
    if tyhjaa:
        try:
            laatikko.delete(1.0, END)
        except TclError:
            pass
    laatikko.insert(INSERT, sisalto + "\n")
    laatikko.configure(state="disabled")

def luo_tekstirivi(kehys, teksti):
    """
    Luo pienen tekstipÃ¤tkÃ¤n, jota voi kÃ¤yttÃ¤Ã¤ tilatietojen esittÃ¤miseen, tai 
    antamaan otsikoita kÃ¤yttÃ¶liittymÃ¤n eri osille. 
    
    :param widget kehys: kehys, jonka sisÃ¤lle tekstilaatikko sijoitetaan
    :param str teksti: nÃ¤ytettÃ¤vÃ¤ teksti
    :return: tekstiriviobjekti
    """
    
    rivi = Label(kehys, text=teksti)
    rivi.pack(side=TOP, fill=BOTH)
    return rivi

def paivita_tekstirivi(rivi, teksti):
    """
    PÃ¤ivittÃ¤Ã¤ tekstirivin sisÃ¤llÃ¶n. 
    
    :param widget rivi: tekstiriviobjekti
    :param str teksti: uusi sisÃ¤ltÃ¶
    """
    
    rivi.configure(text=teksti)

def luo_tekstikentta(kehys):
    """
    Luo tekstikentÃ¤n, johon kÃ¤yttÃ¤jÃ¤ voi syÃ¶ttÃ¤Ã¤ tekstiÃ¤. TekstikentÃ¤n arvo
    voidaan lukea kutsumalla lue_kentan_sisalto-funktiota. 
    
    :param widget kehys: kehys, jonka sisÃ¤lle tekstikenttÃ¤ sijoitetaan
    :return: tekstikenttÃ¤objekti
    """
    
    kentta = Entry(kehys)
    kentta.pack(side=TOP)
    return kentta

def lue_kentan_sisalto(kentta):
    """
    Lukee mÃ¤Ã¤ritetyn syÃ¶tekentÃ¤n sisÃ¤llÃ¶n ja palauttaa sen. 
    
    :param widget kentta: syÃ¶tekenttÃ¤, jonka sisÃ¤ltÃ¶ halutaan lukea
    :return: syÃ¶tekentÃ¤n sisÃ¤ltÃ¶ merkkijonona
    """
    
    return kentta.get()

def tyhjaa_kentan_sisalto(kentta):
    """
    TyhjentÃ¤Ã¤ mÃ¤Ã¤ritetyn syÃ¶tekentÃ¤n sisÃ¤llÃ¶n.
    
    :param widget kentta: syÃ¶tekenttÃ¤, jonka sisÃ¤ltÃ¶ halutaan lukea
    """
    
    kentta.delete(0, len(kentta.get()))

def luo_vaakaerotin(kehys, marginaali=2):
    """
    Luo vaakatason erottimen, jolla voidaan esim. erottaa selkeÃ¤mmin 
    kÃ¤yttÃ¶liittymÃ¤n osia toisistaan. Funktiolle voidaan lisÃ¤ksi antaa toinen 
    argumentti, joka kertoo paljonko ylimÃ¤Ã¤rÃ¤istÃ¤ tyhjÃ¤Ã¤ laitetaan viivan 
    molemmin puolin.
    
    :param widget kehys: kehys, johon erotin sijoitetaan
    :param int marginaali: ylimÃ¤Ã¤rÃ¤isen tyhjÃ¤n mÃ¤Ã¤rÃ¤ pikseleinÃ¤
    """
    
    erotin = Separator(kehys, orient="horizontal")
    erotin.pack(side=TOP, fill=BOTH, pady=marginaali)
    
def luo_pystyerotin(kehys, marginaali=2):
    """
    Luo pystysuoran erottimen, jolla voidaan esim. erottaa selkeÃ¤mmin 
    kÃ¤yttÃ¶liittymÃ¤n osia toisistaan. Funktiolle voidaan lisÃ¤ksi antaa toinen 
    argumentti, joka kertoo paljonko ylimÃ¤Ã¤rÃ¤istÃ¤ tyhjÃ¤Ã¤ laitetaan viivan 
    molemmin puolin.
    
    :param widget kehys: kehys, johon erotin sijoitetaan
    :param int marginaali: ylimÃ¤Ã¤rÃ¤isen tyhjÃ¤n mÃ¤Ã¤rÃ¤ pikseleinÃ¤
    """

    erotin = Separator(kehys, orient="vertical")
    erotin.pack(side=TOP, fill=BOTH, pady=marginaali)

def avaa_viesti_ikkuna(otsikko, viesti, virhe=False):
    """
    Avaa ponnahdusikkunan, jossa on viesti kÃ¤yttÃ¤jÃ¤lle. Viesti-ikkuna voidaan 
    mÃ¤Ã¤ritellÃ¤ virhe-argumentilla virheikkunaksi, jolloin siinÃ¤ nÃ¤kyy eri 
    kuvake. Ikkunalle annetaan otsikko ja viesti. 
    
    :param str otsikko: ikkunan otsikko
    :param str viesti: ikkunaan kirjoitettava viesti
    :param bool virhe: totuusarvo, joka kertoo onko kyseessÃ¤ virheviesti
    """
    
    if virhe:
        messagebox.showerror(otsikko, viesti)
    else:
        messagebox.showinfo(otsikko, viesti)    

def avaa_hakemistoikkuna(otsikko, alkuhakemisto="."):
    """
    Avaa ikkunan, josta kÃ¤yttÃ¤jÃ¤ voi valita hakemiston. HyÃ¶dyllinen erityisesti
    datakansion lataamiseen. Ikkunalle tulee antaa otsikko, ja lisÃ¤ksi sille 
    voidaan mÃ¤Ã¤rittÃ¤Ã¤ mikÃ¤ hakemisto aukeaa aluksi (oletuksena se hakemisto, 
    josta ohjelma kÃ¤ynnistettiin). Funktio palauttaa polun kÃ¤yttÃ¤jÃ¤n valitsemaan
    hakemistoon merkkijonona. 
    
    :param str otsikko: hakemistoikkunan otsikko
    :param str alkuhakemisto: hakemisto, joka avautuu ikkunaan
    :return: kÃ¤yttÃ¤jÃ¤n valitseman hakemiston polku
    """
    
    polku = filedialog.askdirectory(title=otsikko, mustexist=True, initialdir=alkuhakemisto)
    return polku

def avaa_tallennusikkuna(otsikko, alkuhakemisto="."):
    """
    Avaa tallennusikkunan, jolla kÃ¤yttÃ¤jÃ¤ voi valita tallennettavalle 
    tiedostolle sijainnin ja nimen. Ikkunalle tulee antaa otsikko, ja lisÃ¤ksi 
    sille voidaan mÃ¤Ã¤rittÃ¤Ã¤ mikÃ¤ hakemisto aukeaa aluksi (oletuksena se 
    hakemisto, josta ohjelma kÃ¤ynnistettiin). Funktio palauttaa polun kÃ¤yttÃ¤jÃ¤n
    nimeÃ¤mÃ¤Ã¤n tiedostoon.
    
    :param str otsikko: tallennusikkunan otsikko
    :param str alkuhakemisto: hakemisto, joka avautuu ikkunaan
    :return: kÃ¤yttÃ¤jÃ¤n nimeÃ¤mÃ¤n tiedoston polku
    """
    
    polku = filedialog.asksaveasfilename(title=otsikko, initialdir=alkuhakemisto)
    return polku

def poista_elementti(elementti):
    """
    Poistaa mÃ¤Ã¤ritetyn elementin kÃ¤yttÃ¶liittymÃ¤stÃ¤. Tarpeen, jos haluat 
    kÃ¤yttÃ¶liittymÃ¤Ã¤n tilapÃ¤isiÃ¤ elementtejÃ¤. 
    
    :param widget elementti: poistettava elementti
    """
    
    try:
        elementti.destroy()
    except AttributeError:
        elementti.get_tk_widget().destroy()

def luo_ali_ikkuna(otsikko):
    """
    Luo ali-ikkunan, jonka sisÃ¤ltÃ¶Ã¤ voidaan muokata. Ali-ikkuna toimii samalla
    tavalla kuin kehys, eli siihen voidaan laittaa mitÃ¤ tahansa muita 
    kÃ¤yttÃ¶liittymÃ¤komponentteja. Ali-ikkuna voidaan piilottaa ja avata 
    uudestaan kÃ¤yttÃ¤mÃ¤llÃ¤ nÃ¤ytÃ¤_ali_ikkuna- ja piilota_ali_ikkuna-funktioita. 
    
    :param str otsikko: ali-ikkunan otsikko
    :return: luotu ali-ikkunaobjekti
    """    
    
    ali = Toplevel()
    ali.title(otsikko)
    return ali
    
def nayta_ali_ikkuna(ali):
    """
    NÃ¤yttÃ¤Ã¤ valitun ali-ikkunan. 
    
    :param object ali: nÃ¤ytettÃ¤vÃ¤ ali-ikkuna    
    """
    
    ali.deiconify()
    
def piilota_ali_ikkuna(ali):
    """
    Piilottaa valitun ali-ikkunan.
    
    :param object ali: piilotettava ali-ikkuna    
    """    
    
    ali.withdraw()

def kaynnista():
    """
    KÃ¤ynnistÃ¤Ã¤ ohjelman. Kutsu tÃ¤tÃ¤ kun olet mÃ¤Ã¤ritellyt kÃ¤yttÃ¶liittymÃ¤n.
    """
    
    ikkuna.mainloop()

def lopeta():
    """
    Sammuttaa ohjelman. 
    """
    
    ikkuna.destroy()

    
    
    
    