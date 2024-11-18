import { chromium } from 'playwright';
import fs from 'fs';

const links = [
    //{ url: 'https://media.ebird.org/catalog?taxonCode=greani1&mediaType=photo', name: 'GarrapateroMayor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=smbani&mediaType=photo', name: 'GarrapateroPicoLiso' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=grbani&mediaType=photo', name: 'GarrapateroPijuy' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=strcuc1&mediaType=photo', name: 'CuclilloRayado' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=phecuc1&mediaType=photo', name: 'CuclilloFaisan' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=litcuc2&mediaType=photo', name: 'CucoArdillaMenor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=dwacuc1&mediaType=photo', name: 'CuclilloEnano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=squcuc1&mediaType=photo', name: 'CuclilloCanelo' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=dabcuc1&mediaType=photo', name: 'CuclilloCanela' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=yebcuc&mediaType=photo', name: 'CuclilloPicoAmarillo' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=bkbcuc&mediaType=photo', name: 'CuclilloPicoNegro' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=gyccuc&mediaType=photo', name: 'CuclilloCabecigris' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=cuckoo3&mediaType=photo', name: 'CuculidaeSp.' },

    //{ url: 'https://media.ebird.org/catalog?taxonCode=nacnig1&mediaType=photo', name: 'AnaperoNacunda' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=lesnig&mediaType=photo', name: 'ChotacabrasMenor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=comnig&mediaType=photo', name: 'ChotacabrasZumbon' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=nighth1&mediaType=photo', name: 'ChordeilesSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=rubnig1&mediaType=photo', name: 'AñaperoVentrirrufo' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=bawnig1&mediaType=photo', name: 'ChotacabrasSerrano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=compau&mediaType=photo', name: 'ChotacabrasPauraque' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=swtnig1&mediaType=photo', name: 'ChotacabrasGolondrina' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=lytnig1&mediaType=photo', name: 'ChotacabrasLira' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whtnig1&mediaType=photo', name: 'ChotacabrasColiblanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=chwwid&mediaType=photo', name: 'TapacaminosDeCarolina' },

    //{ url: 'https://media.ebird.org/catalog?taxonCode=compot1&mediaType=photo', name: 'NictibioUrutau' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=oilbir1&mediaType=photo', name: 'Guacharo' },

    //{ url: 'https://media.ebird.org/catalog?taxonCode=blkswi&mediaType=photo', name: 'VencejoNegro' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whcswi2&mediaType=photo', name: 'VencejoPechiblanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whcswi1&mediaType=photo', name: 'VencejoBarbiblanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=spfswi1&mediaType=photo', name: 'VencejoCuatroojos' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=cypsel1&mediaType=photo', name: 'CypseloidesSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=chcswi1&mediaType=photo', name: 'VencejoCuelloCastano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whcswi&mediaType=photo', name: 'VencejoCollarBlanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=strept2&mediaType=photo', name: 'StreptoprocneSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=grrswi1&mediaType=photo', name: 'VencejoCeniciento' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=barswi&mediaType=photo', name: 'VencejoLomiblanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=chiswi&mediaType=photo', name: 'VencejoDeChimenea' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=shtswi1&mediaType=photo', name: 'VencejoRabon' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=chaetu&mediaType=photo', name: 'ChaeturaSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whtswi1&mediaType=photo', name: 'VencejoMontanes' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=lstswi1&mediaType=photo', name: 'VencejoTijeretaMenor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=larswi1&mediaType=photo', name: 'VencejograndeSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=smaswi1&mediaType=photo', name: 'VencejoPequeñoSp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=swift1&mediaType=photo', name: 'VencejoSp.' },

    //{ url: 'https://media.ebird.org/catalog?taxonCode=whnjac1&mediaType=photo', name: 'ColibriCapuchaAzul' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whtsic1&mediaType=photo', name: 'PicohozColiverde' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=rubher&mediaType=photo', name: 'ErmitanoHirsuto' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=batbar1&mediaType=photo', name: 'ErmitanoBarbudoColibandeado' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=whbher1&mediaType=photo', name: 'ErmitanoBarbiblanco' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=greher1&mediaType=phot', name: 'ErmitanoVerde' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=tabher1&mediaType=photo', name: 'ErmitanoVentrihabano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=lobher&mediaType=photo', name: 'ColibriErmitanoMesoamericano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=pabher1&mediaType=photo', name: 'ErmitanoVentripalido' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=stther2&mediaType=photo', name: 'ColibriErmitanoEnano' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=grflan1&mediaType=photo', name: 'ColibriPicolanzaMayor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=webhum3&mediaType=photo', name: 'ColibriPicocunaOccidental' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=webhum1&mediaType=photo', name: 'ColibriPicocunaOriental' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=spvear1&mediaType=photo', name: 'ColibriRutilante' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=brvear1&mediaType=photo', name: 'ColibriPardo' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=lesvio1&mediaType=photo', name: 'ColibriOrejasVioletasMenor' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=violet1&mediaType=photo', name: 'Colibri(Colibri)sp.' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=pucfai1&mediaType=photo', name: 'ColibriHadaEnmascarada' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=ruthum1&mediaType=photo', name: 'ColibriRubi' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=bltman1&mediaType=photo', name: 'MangoGorjinegro' },
    //{ url: 'https://media.ebird.org/catalog?taxonCode=tousun1&mediaType=photo', name: 'ColibriTurmalina' }
    



   
];

async function scrapeImages(url, name) {
    const browser = await chromium.launch({ headless: false }); // Usa `headless: false` para ver la interacción
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle' });

    let images = [];
    let lastCount = 0;
    

    while (images.length < 1000) {
        // Extraer imágenes actuales
        const newImages = await page.$$eval('.ResultsGallery-link', (results) =>
            results.map((el) => {
                const image = el.querySelector('img')?.getAttribute('src');
                return { image };
            }).filter(item => item.image)
        );

        // Evitar duplicados
        images = [...new Map([...images, ...newImages].map(item => [item.image, item])).values()];

        // Verificar si hemos cargado más imágenes; si no, detener el bucle
        if (images.length === lastCount) break;
        lastCount = images.length;

        console.log(`Total imágenes obtenidas para ${name}: ${images.length}`);

        // Desplazamiento hacia abajo con un intervalo aleatorio
        await page.evaluate(() => window.scrollBy(0, window.innerHeight));
        await page.waitForTimeout(1000 + Math.floor(Math.random() * 4000));

        // Intentar hacer clic en el botón si está visible
        const showMoreButton = await page.$('.pagination .Button');
        if (showMoreButton) {
            await showMoreButton.scrollIntoViewIfNeeded();
            await showMoreButton.click();
            await page.waitForTimeout(4000);
        } else {
            console.log(`Botón 'More results' no encontrado para ${name}, saliendo del bucle.`);
            break;
        }
    }

    console.log(`Total imágenes finales para ${name}: ${images.length}`);
    

    
    const filename = `${name}.json`;

    fs.writeFileSync(filename, JSON.stringify(images, null, 2), 'utf-8');

    console.log(`Las imágenes de ${name} se han guardado en '${filename}'.`);

    await browser.close();
}

// Iterar sobre cada URL
for (const link of links) {
    await scrapeImages(link.url, link.name);
}
