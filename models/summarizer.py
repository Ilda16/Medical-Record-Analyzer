from transformers import pipeline

#Initalize the summarization model
summarizer = pipeline("summarization", model ="facebook/bart-large-cnn")

def summarize(text):
    # the functions helps to summarize text
    result = summarizer(text, max_length=50, min_length=10, do_sample=False)

    return result[0]['summary_text']