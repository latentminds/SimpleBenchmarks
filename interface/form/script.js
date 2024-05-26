document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('quiz-container');

    try {
        // Function to get URL parameters
        function getQueryParam(param) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(param);
        }

        // Get the paths from the URL parameters
        const questionsPath = getQueryParam('questions');
        const answersPath = getQueryParam('answers');

        const questions = await fetch(questionsPath);
        const answers = await fetch(answersPath);
        
        const questions_data = await questions.json();
        const answers_data = await answers.json();
        
        Object.keys(questions_data).forEach(category => {

            const categoryElement = document.createElement('div');
            categoryElement.className = 'category';

            const categoryTitle = document.createElement('h1');
            categoryTitle.textContent = category;
            categoryElement.appendChild(categoryTitle);

            for(let i = 0; i < questions_data[category].length; i++) {
                questionData = questions_data[category][i]
                answersData = answers_data[category][i]

                const questionElement = createQuestionElement(questionData, answersData);
                categoryElement.appendChild(questionElement);
            }

            container.appendChild(categoryElement);
        });
    } catch (error) {
        console.error('Error fetching JSON data:', error);
    }

    function createQuestionElement(questionData, answersData) {
        const questionElement = document.createElement('div');
        questionElement.className = 'question';

        const questionTitle = document.createElement('h3');
        questionTitle.textContent = questionData.question;
        questionElement.appendChild(questionTitle);

        for(let i = 0; i < questionData.responses.length; i++) {
            response = questionData.responses[i]
            response_pct = answersData[i]

            const responseElement = document.createElement('div');
            responseElement.className = 'response';
            responseElement.textContent = response.text;

            const parentDiv = document.createElement('div');
            parentDiv.className = 'response_pct';
            parentDiv.style.width = `${response_pct*100}%`

            const parentparentDiv = document.createElement('div');

            parentDiv.appendChild(responseElement);
            parentparentDiv.appendChild(parentDiv);
            parentparentDiv.style.width = "2000px";
            questionElement.appendChild(parentparentDiv);

        }

        return questionElement;
    };

});
