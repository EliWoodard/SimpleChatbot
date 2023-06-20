document.addEventListener('DOMContentLoaded', function() {

    const responses = [
        { text: "Hello!", embeddings: null },
        { text: "Goodbye!", embeddings: null },
        { text: "How can I help you?", embeddings: null },
        { text: "I'm an AI chatbot.", embeddings: null }
    ];

    let model;

    async function loadModelAndEmbeddings() {
        model = await use.load();
        const sentences = responses.map(response => response.text);
        model.embed(sentences).then(embeddings => {
            responses.forEach((response, index) => {
                response.embeddings = embeddings.slice([index, 0], [1]);
            });
        });
    }



    async function getBotResponse(userMessage) {
        if (!model) {
            await loadModelAndEmbeddings();
        }

        const messageEmbedding = await model.embed(userMessage);
        let maxSim = 0;
        let maxIndex = -1;

        responses.forEach((response, index) => {
            const sim = tf.metrics.cosineDistance(messageEmbedding, response.embeddings);
            if (sim > maxSim) {
                maxSim = sim;
                maxIndex = index;
            }
        });

        return responses[maxIndex].text;
    }
});