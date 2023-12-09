export async function handler(event, context) {
    try {
        // Gelen veriyi JSON formatında parse et
        const requestBody = JSON.parse(event.body);
        console.log('Parsed request body:', requestBody);

        // Flask uygulamanızın API'sine verileri POST isteği ile gönderme örneği
        const response = await fetch('https://creativead.netlify.app/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        // Flask uygulamasından gelen cevabı JSON formatında al
        const responseData = await response.json();

        // Netlify'e geri dönecek cevap
        return {
            statusCode: response.status,
            body: JSON.stringify(responseData),
        };
    } catch (error) {
        console.error('Error processing request:', error);

        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Internal Server Error' }),
        };
    }
}
