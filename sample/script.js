document.getElementById('analyzeButton').addEventListener('click', async function() {
    const messageInput = document.getElementById('messageInput').value;

    if (!messageInput) {
        alert('Please enter a message!');
        return;
    }


    let requestData;
    try {
        requestData = JSON.parse(messageInput);
    } catch (e) {
        alert('Invalid JSON format');
        return;
    }

    const requestCode = `POST /api/analyze\n${JSON.stringify(requestData, null, 2)}`;
    document.getElementById('requestCode').textContent = requestCode;


    const response = await simulateApiCall(requestData);

  
    document.getElementById('harassmentScore').textContent = `Harassment Score: ${response.harassment_score}`;
    const flagsList = document.getElementById('flagsList');
    flagsList.innerHTML = '';
    response.flags.forEach(flag => {
        const li = document.createElement('li');
        li.textContent = JSON.stringify(flag);
        flagsList.appendChild(li);
    });

    document.getElementById('resultArea').style.display = 'block';

    // const responseCode = `POST /api/analyze\n${JSON.stringify(response, null, 2)}`;
    // document.getElementById('responseCode').textContent = responseCode;


    displayFormattedResponse(response);
});


  
        function displayFormattedResponse(response) {
            const formattedDiv = document.getElementById('apijsonResponse');
            formattedDiv.innerHTML = '';
            const responseDiv = document.createElement('div');
            responseDiv.classList.add('key-value');
            formatObject(response, responseDiv);
            formattedDiv.appendChild(responseDiv);
        }


        function formatObject(obj, parentDiv) {
            for (const [key, value] of Object.entries(obj)) {
                const keyValueDiv = document.createElement('div');
                const keyDiv = document.createElement('span');
                keyDiv.classList.add('key');
                keyDiv.textContent = `${key}: `;
                keyValueDiv.appendChild(keyDiv);

                if (typeof value === 'object' && !Array.isArray(value) && value !== null) {
                    const collapsibleDiv = document.createElement('div');
                    collapsibleDiv.classList.add('collapsible');
                    collapsibleDiv.textContent = `${key} (Click to expand)`;
                    collapsibleDiv.onclick = function () {
                        const contentDiv = collapsibleDiv.nextElementSibling;
                        contentDiv.style.display = contentDiv.style.display === 'none' ? 'block' : 'none';
                    };

                    const contentDiv = document.createElement('div');
                    contentDiv.classList.add('content');
                    formatObject(value, contentDiv);
                    keyValueDiv.appendChild(collapsibleDiv);
                    keyValueDiv.appendChild(contentDiv);
                } else if (Array.isArray(value)) {
                    const arrayDiv = document.createElement('div');
                    arrayDiv.classList.add('value');
                    value.forEach((item, index) => {
                        arrayDiv.innerHTML += `Item ${index + 1}: ${item}<br>`;
                    });
                    keyValueDiv.appendChild(arrayDiv);
                } else {
                    const valueDiv = document.createElement('span');
                    valueDiv.classList.add('value');
                    valueDiv.textContent = value;
                    keyValueDiv.appendChild(valueDiv);
                }

                parentDiv.appendChild(keyValueDiv);
            }
        }



async function simulateApiCall(requestData) {
   
    const apiUrl = 'http://127.0.0.1:8000/api/analyze/analyze-messages';

    try {
      
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

       
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

      
        const data = await response.json();

      
        return {
            harassment_score: data.analysis_results.data.harassment_score,
            flags: data.analysis_results.data.flagged_phrases,
            is_harassment: data.analysis_results.data.is_harassment,
            harassment_type: data.analysis_results.data.harassment_type,
            recommendations: data.analysis_results.data.recommendations,
            revised_email: data.analysis_results.data.revised_email,
            tone: data.analysis_results.data.tone,
            sentiment: data.analysis_results.data.sentiment
        };
        
    } catch (error) {
        console.error('Error calling the API:', error);
        return {
            harassment_score: 0,
            flags: ['Error contacting API'],
            is_harassment: 'unknown',
            harassment_type: 'unknown',
            recommendations: 'Unable to analyze the email.',
            revised_email: 'No revised email available.',
            tone: 'unknown',
            sentiment: 'unknown'
        };
    }
}