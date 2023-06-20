let responses = [
    { text: "Hello!", embeddings: null },
    { text: "Goodbye!", embeddings: null },
    { text: "How can I help you?", embeddings: null },
    { text: "I'm an AI chatbot.", embeddings: null }
];

let model;

async function loadModelAndEmbeddings() {
    model = await use.load(); // Use 'use' instead of 'universalSentenceEncoder'
    const sentences = responses.map(response => response.text);
    const embeddings = await model.embed(sentences);
    responses.forEach((response, index) => {
        response.embeddings = embeddings.slice([index, 0], [1]);
    });
}

async function getBotResponse(userMessage) {
    if (!model) {
        await loadModelAndEmbeddings();
    }

    // Check if userMessage contains mathematical expressions
    const arithmeticRegex = /(\b\d+(\.\d+)?\s*[\+\-\*\/]\s*)+\d+(\.\d+)?\b/g;
    const algebraExpressionRegex = /\b(\w+\s*=\s*\d+\s*[\+\-\*\/]\s*\d+|\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\w+|[a-zA-Z]\s*[\+\-\*\/]\s*\d+|[a-zA-Z])/g;
    const algebraVariableRegex = /\b(\w+\s*=\s*\d+)/g;

    const mathExpressions = userMessage.match(arithmeticRegex);
    const algebraExpressions = userMessage.match(algebraExpressionRegex);
    const algebraVariables = userMessage.match(algebraVariableRegex);

    let response = '';

    // Algebraic expressions with variable substitution
    if (algebraExpressions && algebraExpressions.length > 0 && algebraVariables && algebraVariables.length > 0) {
        let variables = {};
        for (let varExp of algebraVariables) {
            let [varName, varValue] = varExp.split('=');
            variables[varName.trim()] = Number(varValue);
        }

        for (let exp of algebraExpressions) {
            try {
                const result = math.evaluate(exp, variables);
                response += `${exp} = ${result}\n`;
            } catch (e) {
                response += `Sorry, I could not understand the expression ${exp}\n`;
            }
        }
    }

    // Arithmetic expressions
    if (mathExpressions && mathExpressions.length > 0) {
        for (let exp of mathExpressions) {
            try {
                const result = math.evaluate(exp);
                response += `${exp} = ${result}\n`;
            } catch (e) {
                response += `Sorry, I could not understand the expression ${exp}\n`;
            }
        }
    }

    // If mathematical expressions were found and processed
    if (response) {
        return response.trim();
    }

    // Otherwise, use embeddings to generate a response
    const messageEmbedding = await model.embed(userMessage);
    let maxSim = 0;
    let maxIndex = -1;

    responses.forEach((response, index) => {
        const sim = messageEmbedding.dot(response.embeddings.transpose()).dataSync()[0];
        if (sim > maxSim) {
            maxSim = sim;
            maxIndex = index;
        }
    });

    return responses[maxIndex].text;
}





// Export the function so that it can be used in main.js
window.getBotResponse = getBotResponse;
