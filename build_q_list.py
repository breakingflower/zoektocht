import os
from bs4 import BeautifulSoup
from IPython import embed

BASE_DIR = "./static/vragen"

VRAGEN_DICT = {
    'intro': {
        'q': """
        <p>
            <figure class="figure">
                <img src="/static/images/image1.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
        Welkom! Op deze site staat een wandeling uitgeschreven voor de bevolking van Oosthoven en omstreken. 
        Deze wandeling bedraagt een afstand van ongeveer 6 km met onderweg verschillende opdrachten. 
        Goed om jezelf en eventueel je gezin twee uur bezig te houden. 
        Tijdens deze tijden van quarantaine is bewegen moeilijk, maar belangrijk. 
        Het enige wat je hiervoor nodig hebt is een smartphone met genoeg mobiele data. 
        Jouw tijd wordt gemeten en bijgehouden. 
        Het kan natuurlijk dat je het antwoord niet kan vinden of dat je een opdracht niet kan uitvoeren. 
        Dan kan je deze opdracht overslagen. De tijd zal dan wel een sprong maken. 
        </p>
        <p>
            <b>
            Als je het antwoord niet kan vinden of het raadsel niet kan oplossen, typ dan <i>geenidee</i> (1 woord) als antwoord. 
            Zo kan je verder naar de volgende opdacht. Vergeet ook geen handzeep / water want je moet sommige voorwerpen aanraken.
            </b>
        <p>
        Typ in het antwoordvakje OK om verder te gaan.
        </p>""",
        'a': "OK" 
    },
    'wandeling': {
        'q': """
        <p>
            Begin bij de kerk van Oosthoven en wandel richting de heischuur. 
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image2.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>
        <p>
            De tijd begint te lopen wanneer je het antwoord op de eerste vraag geeft. 
            Op de hoek tussen de straten ‘Heieinde’ en ‘Schuurhoven’ (dus ter hoogte van de heischuur) ligt een wandelknooppunt. 
            Wat is het nummer van het wandelknooppunt?
        </p>""",
        'a': '59'
    },
    'morse': {
        'q': """
        <p>
            Ok, nu kan je op weg. 
            Je volgt nu knooppunt 51, dus je gaat in de straat ‘Heieinde’. 
            Zorg dat je heel de route volgt en zoek hierbij het paaltje op de foto. 
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image3.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>
        <p>
            Achter dit paaltje bevindt zich een vraag in code. Kan jij de oplossing geven op deze vraag?
        </p>
        """,
        'a': '2360'
    },
    'knooppunt51': {
        'q': """
        <p>
            Aangekomen bij knooppunt 51. 
            Hopelijk gaat het voorlopig nog vlot en heb je de code kunnen kraken.
            Om het volgende knooppunt te weten maak je de som van alle getallen die aan de paal van knooppunt 51 hangen. 
            Dus je telt alle knooppunten die hangen aan deze paal op. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image4.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Wat is de uitkomst? 
        </p>
            
        """,
        'a': '559'
    },
    'klimmen': {
        'q': """
        <p>
            Heel goed! 
            Je gaat door naar knooppunt 52. 
            Onderweg vind je een boom. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image5.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            In deze boom hangt een sjaaltje. 
            Klim naar dit sjaaltje en lees wat erop staat. 
            Zorg dat je het sjaaltje achteraf wel terughangt.
            Wat staat er op het sjaaltje (15 letters)?
        </p>
        """,
        'a': 'bomenknuffelaar' 
    },
    'knooppunt52': {
        'q': """
        <p>
            Wanneer je aangekomen bent bij knooppunt 52, pak je een kompas erbij.
            Dit kan ook via de gsm of aan de hand van de zon. 
            Zet nu vijf grote stappen naar het noorden en vertel hier wat er daar ligt.
            Let op voor het grachtje tijdens de stappen af te leggen. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image6.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Zorg dat je achteraf het voorwerp terug legt alstublieft.
            Voorwerp (4 letters): 
        </p>
        """,
        'a': 'lego' 
    },
    'stappentellen': {
        'q': """
        <p>
            Goed gevonden! 
            Nu ga je richting knooppunt 41 en tel je de passen van het ene paaltje (knooppunt 52) tot het andere paaltje (knooppunt 41). 
            Natuurlijk is er hierbij een verschil van persoon tot persoon.
            Je mag hierbij 50 passen naast zitten. 
            Om beter in te schatten, laat ik je weten dat ik 1,92 meter groot ben.  
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image7.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Aantal passen: 
        </p>
        """,
        'a': 305
    },
    'knooppunt41': {
        'q': """
        <p>
            Dat was inderdaad geen grote afstand. 
            Rond dit knooppunt liggen veel dennenappels. 
            De bedoeling is om met deze dennenappels een boodschap te schrijven voor de volgende wandelaars.
            Maak een foto en zet deze op deze pagina.
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image8.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>
        """,
        'a': ""
    },
    'ksjtaal': {
        'q': """
        <p>
            Dankjewel, wat een mooie boodschap! 
            Je vervolgt je weg naar knooppunt 54. 
            Onderweg kom je de boom uit de foto tegen. 
            Achter deze boom bevindt zich een tekst in code. 
            Deze code bevat een vraag en de oplossing van die vraag zet je hieronder. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image9.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Oplossing (7 letters): 
        </p>
        """,
        'a': "koekoek"
    },
    'knooppunt54': {
        'q': """
        <p>
            Waarvan is dit het logo? 
            Bij knooppunt 54 vind je dit logo met de naam van de organisatie moest je het niet weten. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image10.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Oplossing (10 letters): 
        </p>
        """,
        'a': "natuurpunt"
    },
    'insecten': {
        'q': """
        <p>
            Inderdaad, heel goed! 
            Ga nu verder naar knooppunt 53. 
            Onderweg ga je door een deel van De Liereman. 
            Tijdens deze tocht kijk je uit naar insecten die je tegenkomt. 
            Een insect heeft zes gelede poten. 
        </p>

        <p>
            <figure class="figure">
                <img src="/static/images/image11.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Schrijf hieronder minstens vijf insecten die je bent tegengekomen, gespreiden door een <b>komma</b>.
        </p>
        """,
        'a': "vijfinsectennodig"
    },
    'knooppunt53': {
        'q': """
        <p>
            Beantwoord volgend raadsel:
        </p>

        <p><i>
            Dit verslind al dat men kan noemen:
        </i></p>
        <p><i>
            Dieren, beesten, bomen, bloemen;
        </i></p>
        <p><i>
            Knaagt ijzer, bijt staal en kan de hardste stenen malen;
        </i></p>
        <p><i>
           Velt koning, verwoest stad. En slaat hoge bergen plat.
        </i></p>

        <p>
            <figure class="figure">
                <img src="/static/images/image12.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Antwoord (4 letters): 
        </p>
        """,
        'a': "tijd"
    },
    'puzzel': {
        'q': """
        <p>
            Heel goed, daar hebben sommigen nu veel van over. 
            Ga nu verder naar knooppunt 57. 
            Onderweg vind je een puzzel, die verstopt ligt bij deze boom. 

        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image13.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Los deze puzzel op en geef de code op de achterkant. 
            Veel puzzelplezier!
        </p>
        """,
        'a': "531"
    },
    'knooppunt57': {
        'q': """
        <p>
            Aangekomen bij knooppunt 57 zie je daar een hek staan. 
            Dit hek wordt vaak gebruikt bij evenementen. 
            Hoeveel tralies bevat dit hek zonder het buitenste kader mee te rekenen?
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image14.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Aantal tralies?
        </p>
        """,
        'a': "17"
    },
    'magneet': {
        'q': """
        <p>
            Ok, nu kan je op weg naar knooppunt 58. 
            Onderweg kom je twee van deze paaltjes tegen.
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image15.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Je hebt beide nodig om de oplossing eruit te halen. 
            Wat kan je vinden in deze palen? (6 letters)
        </p>
        """,
        'a': "smiley"
    },
    'knooppunt58': {
        'q': """
        <p>
            Dat heb je heel goed gedaan! 
            Nu je bent aangekomen bij knooppunt 58, ben je bijna bij het eind- en beginpunt. 
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image16.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Uit welke straat ben je juist gekomen? Tip: gebruik het teken '
        </p>
        """,
        'a': "Bruno'sstraat"
    },
    'raadsel': {
        'q': """
        <p>
            Het laatste stuk is terug naar knooppunt 59. 
            Dit laatste raadsel is wat moeilijker en te vinden achter de paal bij het bord van Oosthoven. 
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image17.png" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Bekijk alles duidelijk voor je een antwoord geeft.
        </p>
        """,
        'a': "43"
    },
    'knooppunt59': {
        'q': """
        <p>
            Proficiat!!! Je bent bij het einde. 
            
        </p>
        <p>
            <figure class="figure">
                <img src="/static/images/image2.jpeg" class="figure-img img-fluid rounded" alt="Intro">
            </figure>
        </p>

        <p>
            Als laatste nog een groepsfoto/selfie bij het eindpunt en de tijd stopt. 
        </p>
        """,
        'a': ""
    }
}

for nr, question in enumerate(VRAGEN_DICT):

    soup = BeautifulSoup(VRAGEN_DICT[question]['q'], 'html.parser')
    with open(os.path.join(BASE_DIR, f'{nr}.html'), "w") as f: 
        f.write(soup.prettify())

    with open(os.path.join(BASE_DIR, 'vragen.txt'), "a") as f: 
        f.write(f'{nr},{question}\n')

    # embed()
