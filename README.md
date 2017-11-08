# NLP Final Project

Ann Keenan

## Summary

Final project for CSE 40657 Natural Language Processing

## Usage

### Baseline

Calculate the baseline stddev
* `python3 bin/baseline`

## Documentation

### Project Idea

I plan to process the tone of yelp reviews, measuring how much a person enjoyed
their experience based on the phrasing that they used in their review.

The input would be raw text taken from a review on yelp, and a series of models
would be trained on reviews to figure out certain phrases that are more likely
to be representative of a good or bad experience. Each phrase in the model would
be assigned a certain score based on the star rating that had been assigned to a
review with that particular ordering of words while training the model, and then
during the testing phase, the average of all the phrases when put together in a
new block of text i.e. a review will be used to generate a predicted total score.

The output would then be a predicted star rating that the reviewer would have
given the service, which could be compared against the actual star rating that
the user assigned to their review.

This processing would allow for a model to be generated that could predict based
on a user’s textual review just how much they enjoyed or had a bad experience
with a product. The model could be applied outside of the realm of yelp reviews,
being able to better predict the tone of reviews on other sites, as well as
figure out how user experiences are on sites such as twitter or reddit where
star ratings are not applicable.

### Baseline

The data that I will be using to train and then test can be found on the yelp
website in either json or sql. I chose to use the sql data as I would be able to
perform table joins on the keys mapping businesses to reviews or reviews to
users and therefore be able to access all the relevant information for each
business more quickly. The documentation is on
[yelp.com](https://www.yelp.com/dataset/documentation/sql),
and I have loaded the data into a MySQL database on my machine, to be accessed
with Python through the PyMySQL library with SQL queries.

I will read the reviews in as word tokens, ignoring things such as bullet
points. I will however take into account capitalization, as all caps is a sign
of its own, however, I will probably add a token to a word if it is in all caps
and treat it similarly to the same word represented with lowercase symbols.
Punctuation such as exclamation points can be very indicative of tone, so I will
tokenize punctuation separately from words, but keep them as important
information. I will strip any whitespace, as it will not be important when
trying to analyze sentiment.

I will use the metric of standard error of the estimate
[formula](http://onlinestatbook.com/2/regression/accuracy.html)
to measure the success of my training. I will find the standard deviation of my
predicted rating from the star rating that is actually associated with a review.

The baseline that I will be comparing against will predict the star rating of a
particular review of a restaurant as being equivalent to the average star rating
of that restaurant. To find a baseline standard deviation to compare my training
against, I ran through the reviews of businesses that had more than 50 reviews,
which amounts to 19,391 businesses. The above formula was substituted as Y being
the star rating given by an actual reviewer, Y’ being the average star review
for the associated busxiness to that review, and N being to total number of
reviews of all businesses with more than 50 reviews.

The metric returned upon calculating this value was a standard deviation of
1.217 from the actual ratings. To improve upon this, my model will attempt to
decrease this standard deviation to at least a number smaller than 1.
