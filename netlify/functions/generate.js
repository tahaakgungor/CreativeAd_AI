import FormData from 'form-data';

export async function handler(event, context) {
    try {
        const formData = new FormData();

        // Gelen verileri JSON formatında parse et
        const requestBody = JSON.parse(event.body);

        console.log('Request body:', requestBody);

        // Form alanlarını FormData nesnesine ekleyin
        formData.append('image', requestBody.image); // Örnek: 'image' form alanı
        formData.append('prompt', requestBody.prompt);
        formData.append('color', requestBody.color);
        formData.append('logo', requestBody.logo);
        formData.append('punchline', requestBody.punchline);
        formData.append('punchline_color', requestBody.punchline_color);
        formData.append('button_text', requestBody.button_text);
        formData.append('button_color', requestBody.button_color);

        // Flask uygulamanızın API'sine verileri POST isteği ile gönderme
        const response = await fetch('https://creativead.netlify.app/.netlify/functions/generate', {
            method: 'POST',
            body: formData,
        });

        // Flask uygulamasından gelen cevabı JSON formatında al
        const responseData = await response.json();

        console.log('Response from API:', responseData);

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
