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

        const decodedQuestions = decodeURIComponent(questionsPath);
        const decodedAnswers = decodeURIComponent(answersPath);

        const questions = await fetch(decodedQuestions);
        const answers = await fetch(decodedAnswers);
        
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

            const sliderElement = document.createElement('div');
            sliderElement.className = 'response_pct';
            sliderElement.style.width = `${response_pct*800}px`
            
            const answerCont = document.createElement('div');
            answerCont.className = 'answerCont';
            
            answerCont.appendChild(sliderElement);
            answerCont.appendChild(responseElement);
            
            questionElement.appendChild(answerCont);

        }

        return questionElement;
    };

});
