// netlify/functions/generate.js
export async function handler(event, context) {
    // Burada form verilerini alabilir ve Flask uygulamanızın API'sine yönlendirebilirsiniz.
    // Örnek bir işlem:
    const requestBody = JSON.parse(event.body);

    // Flask uygulamanızın API'sine verileri POST isteği ile gönderme örneği
    const response = await fetch('https://creativead.netlify.app/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
    });

    const responseData = await response.json();

    // Netlify'e geri dönecek cevap
    return {
        statusCode: response.status,
        body: JSON.stringify(responseData),
    };
}
