import os
import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("stopwords")
nltk.download("wordnet")

datasets = [
    os.path.join("exp", "d2_utterance", "nlv2_after.csv"),
    os.path.join("exp", "d2_utterance", "result", "task4_selected_0.csv"),
    os.path.join("exp", "d2_utterance", "result", "task4_two_selected_0.csv"),
]

names = ["original", "one_axis", "two_axes"]

if __name__ == "__main__":
    for i, dataset in enumerate(datasets):
        df = pd.read_csv(dataset)
        sentences = df["commands"].tolist()

        stop_words = set(stopwords.words("english"))
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()

        def preprocess_text(text):
            # Tokenize and convert to lowercase
            words = nltk.word_tokenize(text.lower())
            # Remove non-alphabetic characters
            words = [word for word in words if word.isalpha()]
            # Remove stopwords
            words = [word for word in words if word not in stop_words]
            # Lemmatize words
            words = [lemmatizer.lemmatize(word) for word in words]
            # Stem words
            # words = [stemmer.stem(word) for word in words]
            return " ".join(words)

        preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(preprocessed_sentences)
        word_frequencies = X.sum(axis=0)

        word_frequency_df = pd.DataFrame(
            {
                "Word": vectorizer.get_feature_names_out(),
                "Frequency": word_frequencies.tolist()[0],
            }
        )

        word_frequency_df.to_csv(
            os.path.join("exp", "analyze", "data", f"{names[i]}.csv"),
            index=False,
        )

        total_word_count = sum(word_frequencies.tolist()[0])
        unique_word_count = len(vectorizer.get_feature_names_out())
        most_common_words = word_frequency_df.nlargest(10, "Frequency")

        print(f"Total Word Count: {total_word_count}")
        print(f"Unique Word Count: {unique_word_count}")
        print(f"Most Common Words: {most_common_words}")
