from flask import Flask, render_template, url_for, flash, redirect, request, current_app
# from flask_wtf.csrf import CSRFProtect
from forms import AnswerForm, ImageForm
from werkzeug.utils import secure_filename

import os 
from datetime import datetime

application = Flask(__name__, static_url_path='/static', static_folder='static')
application.config['SECRET_KEY'] = 'RUBENSSPEL'
application.config['UPLOAD_DIR'] = '/static/uploads'
application.config['ALLOWED_UPLOAD_EXT'] = {'jpeg', 'png', 'jpg'}

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
    
class Game: 

    def __init__(self, current_game, next_game, t0=datetime.now().timestamp()): 

        self.t0 = t0
        self.current_game = current_game
        self.next_game = next_game
        self.qa = VRAGEN_DICT[current_game]

        self.form = AnswerForm()
    
    def save_image(self): 
        # get ext 
        _, ext = os.path.splitext(self.form.picture.data.filename)
        # add to t0
        picture_path = os.path.join(current_app.root_path, 'static', 'uploads', self.current_game, self.t0+ext)
        # save
        self.form.picture.data.save(picture_path)

    def play(self, upload_image=False): 

        if upload_image: 
            self.form = ImageForm() 
            if self.form.validate_on_submit():
                if self.form.picture.data: 
                    self.save_image()
                    return redirect(url_for(self.next_game, t0=self.t0))
                else: 
                    return redirect(url_for(self.current_game, t0=self.t0))

        if self.form.validate_on_submit():
            if self.check_answer():
                return redirect(url_for(self.next_game, t0=self.t0))
            else: 
                return redirect(url_for(self.current_game, t0=self.t0))
        return render_template('page.html', form=self.form, vraag=self.qa['q'], title=self.current_game.title())

    def check_answer(self): 

        if self.form.answer.data == "geenidee":
            return True

        if type(self.qa['a']) == int: 
            return int(self.form.answer.data) in range(self.qa['a']-51, self.qa['a']+51)
        elif self.qa['a'] == "":
            return True
        elif self.qa['a'] == 'vijfinsectennodig':
            return len(self.form.answer.data.split(',')) >= 5

        return self.form.answer.data.lower() == self.qa['a'].lower()
        
    def __repr__(self): 
        return f'From {self.current_game} to {self.next_game}'

@application.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@application.route('/', methods=['GET', 'POST'])
@application.route('/intro', methods=['GET', 'POST'])
def intro(): 
    return Game('intro', 'wandeling').play()

@application.route('/wandeling/<t0>', methods=['GET', 'POST'])
def wandeling(t0): 
    return Game('wandeling', 'morse').play()

@application.route('/morse/<t0>', methods=['GET', 'POST'])
def morse(t0): 
    return Game('morse', 'knooppunt51', t0=t0).play()

@application.route('/knooppunt51/<t0>', methods=['GET', 'POST'])
def knooppunt51(t0): 
    return Game('knooppunt51', 'klimmen', t0=t0).play()

@application.route('/klimmen/<t0>', methods=['GET', 'POST'])
def klimmen(t0): 
    return Game('klimmen', 'knooppunt52', t0=t0).play()

@application.route('/knooppunt52/<t0>', methods=['GET', 'POST'])
def knooppunt52(t0): 
    return Game('knooppunt52', 'stappentellen', t0=t0).play()

@application.route('/stappentellen/<t0>', methods=['GET', 'POST'])
def stappentellen(t0): 
    return Game('stappentellen', 'knooppunt41', t0=t0).play()

@application.route('/knooppunt41/<t0>', methods=['GET', 'POST'])
def knooppunt41(t0): 
    return Game('knooppunt41', 'ksjtaal', t0=t0).play(upload_image=True)

@application.route('/ksjtaal/<t0>', methods=['GET', 'POST'])
def ksjtaal(t0): 
    return Game('ksjtaal', 'knooppunt54', t0=t0).play()

@application.route('/knooppunt54/<t0>', methods=['GET', 'POST'])
def knooppunt54(t0): 
    return Game('knooppunt54', 'insecten', t0=t0).play()

@application.route('/insecten/<t0>', methods=['GET', 'POST'])
def insecten(t0): 
    return Game('insecten', 'knooppunt53', t0=t0).play()

@application.route('/knooppunt53/<t0>', methods=['GET', 'POST'])
def knooppunt53(t0): 
    return Game('knooppunt53', 'puzzel', t0=t0).play()

@application.route('/puzzel/<t0>', methods=['GET', 'POST'])
def puzzel(t0): 
    return Game('puzzel', 'knooppunt57', t0=t0).play()

@application.route('/knooppunt57/<t0>', methods=['GET', 'POST'])
def knooppunt57(t0): 
    return Game('knooppunt57', 'magneet', t0=t0).play()

@application.route('/magneet/<t0>', methods=['GET', 'POST'])
def magneet(t0): 
    return Game('magneet', 'knooppunt58', t0=t0).play()

@application.route('/knooppunt58/<t0>', methods=['GET', 'POST'])
def knooppunt58(t0): 
    return Game('knooppunt58', 'raadsel', t0=t0).play()

@application.route('/raadsel/<t0>', methods=['GET', 'POST'])
def raadsel(t0): 
    return Game('raadsel', 'knooppunt59', t0=t0).play()

@application.route('/knooppunt59/<t0>', methods=['GET', 'POST'])
def knooppunt59(t0): 
    return Game('knooppunt59', 'finish', t0=t0).play(upload_image=True)

@application.route('/finish/<t0>', methods=['GET', 'POST'])
def finish(t0):
    
    dt = datetime.now() - datetime.fromtimestamp((float(t0)))

    # get all content of the kooppunt59 folder    
    all_ims = os.listdir(os.path.join(current_app.root_path, 'static', 'uploads', 'knooppunt59'))
    all_ims.remove('.keep')

    # should only return one entry, so taking element zero is effectively removing the list object
    imname = [im for im in all_ims if t0 in im][0]

    # save this thing in some other file
    with open(os.path.join(current_app.root_path, 'static', 'hall_of_fame', t0+'.txt'), 'w') as f: 
        f.write(f'{t0}\n')
        f.write(f'{dt}\n')
        f.write(f'{imname}\n')
    
    all_finishers_files = sorted(os.listdir(os.path.join(current_app.root_path, 'static', 'hall_of_fame')))
    all_finishers_files.remove('.keep')

    your_rank = all_finishers_files.index(t0+'.txt')

    return render_template('finish.html', imname=imname, dt=str(dt), rank=your_rank)


@application.route('/hall_of_fame', methods=['GET'])
def hall_of_fame(): 

    all_finishers_files = sorted(os.listdir(os.path.join(current_app.root_path, 'static', 'hall_of_fame')))
    all_finishers_files.remove('.keep')

    t0_list = []
    dt_list = []
    imname_list = []
    ranking_list = []
    for ranking, fname in enumerate(all_finishers_files): 
        with open(os.path.join(current_app.root_path, 'static', 'hall_of_fame', fname), 'r') as f:
            t0 = f.readline() 
            dt = f.readline()
            imname = f.readline() 

            t0_list.append(t0)
            dt_list.append(dt)
            imname_list.append(imname)
            ranking_list.append(ranking)

    return render_template('hall_of_fame.html', data_list=zip(ranking_list, t0_list, dt_list, imname_list))

if __name__ == "__main__":
    application.run(host='0.0.0.0')