"""
piiristo - yksinkertainen RLC-piirilaajennus ikkunasto:lle

@author Mika Oja, Oulun yliopisto

Kirjasto on laajennus yksinkertaiselle ikkunasto-nimiselle kÃ¤yttÃ¶liittymÃ¤-
kirjastolle. SisÃ¤ltÃ¤Ã¤ uuden kÃ¤yttÃ¶liittymÃ¤komponentin (rajoitettujen) 
piirikaavioiden piirtÃ¤miseen. Piirikaavioelementin luomista ja siihen 
piirtÃ¤mistÃ¤ varten on omat funktionsa. Yksinkertaisen kÃ¤yttÃ¶esimerkin lÃ¶ydÃ¤t
tÃ¤mÃ¤n kirjaston pÃ¤Ã¤ohjelmasta. 

Kirjasto kÃ¤yttÃ¤Ã¤ SchemDraw-kirjastoa

https://cdelker.bitbucket.io/SchemDraw/SchemDraw.html

sekÃ¤ SchemCanvas-laajennusta, joka lisÃ¤Ã¤ kirjastoon tuen 
kÃ¤yttÃ¶liittymÃ¤elementtiin piirtÃ¤miseen (SchemDraw.py). Laajennustiedosto tulee
laittaa samaan kansioon tÃ¤mÃ¤n kirjaston ja sitÃ¤ kÃ¤yttÃ¤vÃ¤n ohjelman kanssa. 
"""

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
matplotlib.use("TkAgg")

from tkinter import *
from tkinter.ttk import *

import SchemDraw as scm
import SchemDraw.elements as e
from SchemCanvas import CanvasDrawing

piirtoikkuna = {
    "kuvaaja": None,
    "piirtoalue": None,
    "akselit": None,
}

def _piirra_komponentti(piiri, komponentti, arvo, pituusyksikko):
    """
    PiirtÃ¤Ã¤ piirii yhden komponentin piirtokursorin nykyiseen sijaintiin ja 
    pÃ¤ivittÃ¤Ã¤ piirtokursorin sijainnin. Funktio on tarkoitettu tÃ¤mÃ¤n kirjaston
    sisÃ¤iseen kÃ¤yttÃ¶Ã¶n, ja tarvit sitÃ¤ ainoastaan jos haluat 
    uudelleenkirjoittaa piirin asettelualgoritmin. 
    
    :param str komponentti: komponentin tyyppi (R, L tai C)
    :param str arvo: komponentin arvo, voi sisÃ¤ltÃ¤Ã¤ kerrannaisyksikÃ¶n
    :param float pituusyksikko: piirin asettelussa kÃ¤ytettÃ¤vÃ¤ pituuskerroin
    """
    
    if komponentti[0].lower() == "r":
        piiri.add(e.RES, d="down", label="{}$\Omega$".format(arvo), l=3*pituusyksikko)
    elif komponentti[0].lower() == "c":
        piiri.add(e.CAP, d="down", label="{}F".format(arvo), l=3*pituusyksikko)
    elif komponentti[0].lower() == "l":
        piiri.add(e.INDUCTOR2, d="down", label="{}H".format(arvo), l=3*pituusyksikko)

def _piirra_pariton_rinnankytkenta(piiri, komponentit, pituusyksikko):
    """
    PiirtÃ¤Ã¤ rinnankytkennÃ¤n, jossa on pariton mÃ¤Ã¤rÃ¤ komponentteja. KytkentÃ¤ 
    piirretÃ¤Ã¤n piirtokursorin nykyiseen sijaintiin, ja piirron pÃ¤Ã¤tteeks 
    kursorin sijainti pÃ¤ivitetÃ¤Ã¤n. Funktio on tarkoitettu tÃ¤mÃ¤n kirjaston 
    sisÃ¤isen kÃ¤yttÃ¶Ã¶n, ja tarvit sitÃ¤ ainoastaan jos haluat uudelleenkirjoittaa
    piirin asettelualgoritmin.
    
    PiirtÃ¤Ã¤ komponentit keskilinjasta ulospÃ¤in molempiin suuntiin. 
    
    :param object piiri: piiriobjekti, johon piiri piirretÃ¤Ã¤n
    :param list komponentit: lista rinnankytkennÃ¤n komponenteista
    :param float pituusyksikko: piiri asettelussa kÃ¤ytettÃ¤vÃ¤ pituuskerroin    
    """
    
    # Jaetaan komponentit kahteen puoliskoon ja keskikomponenttiin
    keski = len(komponentit) // 2
    vasen = komponentit[:keski]
    oikea = komponentit[keski+1:]
    piiri.add(e.DOT)
    
    # tallennetaan keskilinjan sijainti
    piiri.push()
    
    # piirretÃ¤Ã¤n vasemman puolen komponentit
    for i, komp in enumerate(vasen[::-1]):
        piiri.add(e.LINE, d="left", l=1)
        
        # reunimmaiseen liittymÃ¤Ã¤n ei tule tÃ¤ppÃ¤Ã¤
        if i != len(vasen) - 1:
            piiri.add(e.DOT)
            
        # talletetaan piirtokursorin sijainti ja piirretÃ¤Ã¤n komponentti
        # sekÃ¤ kytketÃ¤Ã¤n se edelliseen / keskilinjaan
        piiri.push()
        _piirra_komponentti(piiri, komp[0], komp[1], pituusyksikko)
        if i != len(vasen) - 1:
            piiri.add(e.DOT)
        piiri.add(e.LINE, d="right", l=1)
        
        # palautetaan piirtokursori seuraavaa komponenttia varten
        piiri.pop()
    
    # palataan keskilinjaan ja tallennetaan se uudestaan
    piiri.pop()    
    piiri.push()
    
    # piirretÃ¤Ã¤n oikean puolen komponentit
    for i, komp in enumerate(oikea):
        piiri.add(e.LINE, d="right", l=1)
        
        # reunimmiaseen liittymÃ¤Ã¤n ei tule tÃ¤ppÃ¤Ã¤
        if i != len(oikea) - 1:
            piiri.add(e.DOT)
                        
        # talletetaan piirtokursorin sijainti ja piirretÃ¤Ã¤n komponentti
        # sekÃ¤ kytketÃ¤Ã¤n se edelliseen / keskilinjaan
        piiri.push()
        _piirra_komponentti(piiri, komp[0], komp[1], pituusyksikko)
        if i != len(oikea) - 1:
            piiri.add(e.DOT)
        piiri.add(e.LINE, d="left", l=1)
        piiri.pop()

    # palataan keskilinjaan ja piirretÃ¤Ã¤n keskikomponentti
    piiri.pop()
    _piirra_komponentti(piiri, komponentit[keski][0], komponentit[keski][1], pituusyksikko)
    piiri.add(e.DOT)
    

def _piirra_parillinen_rinnankytkenta(piiri, komponentit, pituusyksikko):
    """
    PiirtÃ¤Ã¤ rinnankytkennÃ¤n, jossa on parillinen mÃ¤Ã¤rÃ¤ komponentteja. KytkentÃ¤ 
    piirretÃ¤Ã¤n piirtokursorin nykyiseen sijaintiin, ja piirron pÃ¤Ã¤tteeks 
    kursorin sijainti pÃ¤ivitetÃ¤Ã¤n. Funktio on tarkoitettu tÃ¤mÃ¤n kirjaston 
    sisÃ¤isen kÃ¤yttÃ¶Ã¶n, ja tarvit sitÃ¤ ainoastaan jos haluat uudelleenkirjoittaa
    piirin asettelualgoritmin.
    
    PiirtÃ¤Ã¤ komponentit keskilinjasta ulospÃ¤in molempiin suuntiin siten, ettÃ¤ 
    keskelle ei tule komponenttia, ja komponenttien vÃ¤li on aina saman 
    pituinen.
    
    :param object piiri: piiriobjekti, johon piiri piirretÃ¤Ã¤n
    :param list komponentit: lista rinnankytkennÃ¤n komponenteista
    :param float pituusyksikko: piiri asettelussa kÃ¤ytettÃ¤vÃ¤ pituuskerroin    
    """
    
    # Jaetaan komponentit kahteen puoliskoon
    keski = len(komponentit) // 2
    vasen = komponentit[:keski]
    oikea = komponentit[keski:]
    piiri.add(e.DOT)
    
    # tallennetaan keskilinjan sijainti
    piiri.push()
    
    # piirretÃ¤Ã¤n vasemman puolen komponentit
    for i, komp in enumerate(vasen[::-1]):
        
        # ensimmÃ¤inen johdin on puolet lyhyempi
        if i == 0:            
            piiri.add(e.LINE, d="left", l=0.5)
        else:
            piiri.add(e.LINE, d="left", l=1)
            
        # reunimmaiseen liittymÃ¤Ã¤n ei tule tÃ¤ppÃ¤Ã¤            
        if i != len(vasen) - 1:
            piiri.add(e.DOT)
        
        # talletetaan piirtokursorin sijainti ja piirretÃ¤Ã¤n komponentti
        # sekÃ¤ kytketÃ¤Ã¤n se edelliseen / keskilinjaan
        piiri.push()
        _piirra_komponentti(piiri, komp[0], komp[1], pituusyksikko)
        if i != len(vasen) - 1:
            piiri.add(e.DOT)

        if i == 0:
            piiri.add(e.LINE, d="right", l=0.5)
        else:            
            piiri.add(e.LINE, d="right", l=1)
            
        # palautetaan piirtokursori seuraavaa komponenttia varten
        piiri.pop()
        
    # palataan keskilinjaan        
    piiri.pop()
    
    # piirretÃ¤Ã¤n oikean puolen komponentit
    for i, komp in enumerate(oikea):

        # ensimmÃ¤inen johdin on puolet lyhyempi
        if i == 0:
            piiri.add(e.LINE, d="right", l=0.5)
        else:
            piiri.add(e.LINE, d="right", l=1)

        # reunimmaiseen liittymÃ¤Ã¤n ei tule tÃ¤ppÃ¤Ã¤            
        if i != len(oikea) - 1:
            piiri.add(e.DOT)

        # talletetaan piirtokursorin sijainti ja piirretÃ¤Ã¤n komponentti
        # sekÃ¤ kytketÃ¤Ã¤n se edelliseen / keskilinjaan
        piiri.push()
        _piirra_komponentti(piiri, komp[0], komp[1], pituusyksikko)
        if i != len(oikea) - 1:
            piiri.add(e.DOT)
        if i == 0:
            piiri.add(e.LINE, d="left", l=0.5)
            
            # tallennetaan erikseen kohta, jossa oikea puoli liittyy 
            # keskilinjaan
            piiri._state.insert(1, (piiri.here, piiri.theta))
        else:
            piiri.add(e.LINE, d="left", l=1)

        # palautetaan piirtokursori seuraavaa komponenttia varten
        piiri.pop()
    
    # palautetaan keskilinjan sijainti
    piiri.pop()
    piiri.add(e.DOT)



def luo_piiri(kehys, leveys=600, korkeus=400, fonttikoko=16):
    """
    Luo piirikaavion, sekÃ¤ siihen liittyvÃ¤n matplotlib-kuvaajan, akselit sekÃ¤
    piirtoalueen kÃ¤yttÃ¶liittymÃ¤n sisÃ¤llÃ¤. Piirtoalueelle mÃ¤Ã¤ritetÃ¤Ã¤n kiinteÃ¤t
    leveys ja korkeus pikseleinÃ¤ antamalla niitÃ¤ vastaavat argumentit. Piiri 
    skaalautuu piirtoalueen koon mukaan, mutta tekstit eivÃ¤t, joten fonttikoko
    on syytÃ¤ sovittaa piirtoalueen kokoon. Palauttaa piiri-objektin, jota 
    tarvitaan myÃ¶hemmin haarojen ja komponenttien piirtÃ¤miseen.
    
    :param object kehys: kehys, johon piirtoalue sijoitetaan
    :param int leveys: piirtoalueen leveys pikseleinÃ¤
    :param int korkeus: piirtoalueen korkeus pikseleinÃ¤
    :param int fonttikoko: teksteissÃ¤ kÃ¤ytettÃ¤vÃ¤ fonttikoko
    
    :return: piirikaavio-objekti.
    """
    
    piiri = CanvasDrawing(fontsize=fonttikoko)
    kuvaaja = Figure(figsize=(leveys / 100, korkeus / 100), dpi=100)
    akselit = kuvaaja.add_axes((0.0, 0.0, 1.0, 1.0))
    akselit.axis("equal")
    piirtoalue = FigureCanvasTkAgg(kuvaaja, master=kehys)
    piirtoalue.get_tk_widget().pack(side=TOP)
    piirtoikkuna["kuvaaja"] = kuvaaja
    piirtoikkuna["akselit"] = akselit
    piirtoikkuna["piirtoalue"] = piirtoalue
    return piiri

def tyhjaa_piiri(piiri):
    """
    Pyyhkii edellisen piirin pois piirtoikkunasta. KÃ¤ytettÃ¤vÃ¤ aina ennen uuden 
    piirin aloittamista.
    
    :param object piiri: piiriobjekti, johon liittyvÃ¤ piirtoalue tyhjÃ¤tÃ¤Ã¤n
    """
    
    piiri.clear()
    piirtoikkuna["akselit"].clear()

def piirra_piiri(piiri):
    """
    PiirtÃ¤Ã¤ rakennetun piirin nÃ¤kyviin piirtoalueelle. 
    
    :param object piiri: piiriobjekti, joka piirretÃ¤Ã¤n
    """
    
    piiri.draw(piirtoikkuna["piirtoalue"], piirtoikkuna["kuvaaja"], piirtoikkuna["akselit"])        

def piirra_jannitelahde(piiri, jannite, taajuus, v_asetteluvali=2):
    """
    PiirtÃ¤Ã¤ piirin jÃ¤nnitelÃ¤hteen. Koska kirjasto on optimoitu juuri piiriloppu-
    tyÃ¶n tekemiseen, usean jÃ¤nnitelÃ¤hteen lisÃ¤Ã¤minen saattaa aiheuttaa outoja
    kaavioita. Asiaan voi vaikuttaa v_asetteluvali-parametrilla. Molemmat 
    numeroarvot annetaan merkkijonoina, joten niissÃ¤ voi olla kerrannaisyksikkÃ¶ 
    mukana. YksikÃ¶t sen sijaan sisÃ¤llytetÃ¤Ã¤n mukaan automaattisesti. 
    
    Normaalisti oletusarvo 2 v_asetteluvali-parametrille toimii hyvin, mutta
    jos piiri nÃ¤yttÃ¤Ã¤ pystysuunnassa huonolta, voi tÃ¤tÃ¤ parametria koittaa 
    sÃ¤Ã¤tÃ¤Ã¤.
    
    :param object piiri: piiriobjekti, jota ollaan muokkaamassa
    :param str jannite: lÃ¤hteen jÃ¤nnite merkkijonona
    :param str taajuus: lÃ¤hteen jÃ¤nnite merkkijonona
    :param float v_asetteluvali: komponenttien asetteluun liittyvÃ¤ kerroin
    """
    
    piiri.add(e.LINE, d="right", l=0.5, move_cur=False)
    piiri.add(e.SOURCE_V, label="{}V\n{}Hz".format(jannite, taajuus), reverse=True, l=6*v_asetteluvali)    
    piiri.add(e.LINE, d="right", l=0.5)
    
def piirra_haara(piiri, komponentit, h_asetteluvali, v_asetteluvali=2, viimeinen=False):
    """
    PiirtÃ¤Ã¤ yhden haaran kaikki komponentit ja rinnankytkennÃ¤t. Komponentit 
    tulee antaa listana, jossa jokainen komponentti on monikko, jonka 1. arvo 
    on komponentin tyyppi ("r", "c" tai "l") ja toinen on komponentin vieressÃ¤
    nÃ¤ytettÃ¤vÃ¤ arvo merkkijonona, eli kerrannaisyksikkÃ¶ voi olla mukana. 
    RinnankytkennÃ¤t ovat listassa listoina, jotka sisÃ¤ltÃ¤vÃ¤t komponentteja em. 
    tavalla. Yksinkertainen esimerkki haarasta jossa on kolme vastusta, joista 
    kaksi rinnankytkennÃ¤ssÃ¤: 
    
    haara = [("r", "100"), [("r", "100"), ("r", "100")]]
    
    ParametreistÃ¤ v_asetteluvali vaikuttaa komponenttien asetteluun 
    pystysuunnassa (oletusarvo on yleensÃ¤ ok) ja h_asetteluvali mÃ¤Ã¤rittÃ¤Ã¤ 
    kuinka paljon tyhjÃ¤Ã¤ haaran molemmille puolille jÃ¤Ã¤. Piiri piirtyy hyvin, 
    jos tÃ¤mÃ¤n parametrin arvoksi annetaan haaran leveimmÃ¤n rinnankytkennÃ¤n 
    komponenttien lukumÃ¤Ã¤rÃ¤ 
    
    Viimeinen parametri kertoo onko kyseessÃ¤ piirin viimeinen haara, jolloin 
    ei piirretÃ¤ liittymÃ¤kohtaa, eikÃ¤ johtimia enÃ¤Ã¤ eteenpÃ¤in. 
    
    :param object piiri: piiriobjekti, jota ollaan muokkaamassa
    :param list komponentit: lista haaran komponenteista
    :param int h_asetteluvali: vaakasuunan asetteluun vaikuttava kerroin
    :param float v_asetteluvali: pystysuunnan asetteluun liittyvÃ¤ kerroin
    :param bool viimeinen: onko haara piirin viimeinen
    """
    
    piiri.pop()
    piiri.add(e.LINE, d="right", l=h_asetteluvali/2)
    if not viimeinen:
        piiri.push()        
        piiri.add(e.DOT)
        piiri.add(e.LINE, d="right", l=h_asetteluvali/2)
        piiri._state.insert(-1, (piiri.here, piiri.theta))
        piiri.pop() 
        
    parallels = sum([1 for k in komponentit if isinstance(k, list)])
    if isinstance(komponentit[0], list) and isinstance(komponentit[-1], list):
        loppujohdin = True
        pituusyksikko = v_asetteluvali / (len(komponentit) + 2) * 2  
        piiri.add(e.LINE, d="down", l=3*pituusyksikko)
    elif isinstance(komponentit[0], list):
        loppujohdin = False
        pituusyksikko = v_asetteluvali / (len(komponentit) + 1) * 2  
        piiri.add(e.LINE, d="down", l=3*pituusyksikko)
    elif isinstance(komponentit[-1], list):
        loppujohdin = True
        pituusyksikko = v_asetteluvali / (len(komponentit) + 1) * 2  
    else:
        loppujohdin = False
        pituusyksikko = v_asetteluvali / len(komponentit) * 2  
    for komponentti in komponentit:
        if isinstance(komponentti, list):
            if len(komponentti) % 2 == 0:
                _piirra_parillinen_rinnankytkenta(piiri, komponentti, pituusyksikko)
            else:
                _piirra_pariton_rinnankytkenta(piiri, komponentti, pituusyksikko)
        else:
            _piirra_komponentti(piiri, komponentti[0], komponentti[1], pituusyksikko)
    
    if loppujohdin:
        piiri.add(e.LINE, d="down", l=3*pituusyksikko)
    
    if not viimeinen:
        piiri.add(e.DOT)
        piiri.add(e.LINE, d="right", l=h_asetteluvali/2, move_cur=False)
        
    piiri.add(e.LINE, d="left", l=h_asetteluvali/2)
