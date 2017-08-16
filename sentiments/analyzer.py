import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # initialize empty sets to load words into
        p, n = set(), set()
        
        # add positive strings to p set
        with open(positives, "r") as filep:
            for line in filep:
                if not line.startswith(";"):
                    p.add(line.strip()) # add argument to strip?
        
        # add negative strings to n set                 
        with open(negatives, "r") as filen:
            for line in filen:
                if not line.startswith(";"):
                    n.add(line.strip())            
                    
        self.positives = p # set with positive words
        self.negatives = n # set with negative
        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # convert text to list list of words
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        
        # initialize subtotal counter for sentiment
        sentiment = 0
        
        # Add to counter for positive 
        for x in tokens:
            if x.lower() in self.positives:
                sentiment += 1
            elif x.lower() in self.negatives:
                sentiment += -1
        
        # return end value        
        return sentiment
