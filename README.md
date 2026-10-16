# DSAIT4310 — Modeling and Data Analysis in Complex Networks

After the feedback meeting with the professor, we have a clear path forward. We decided we will stick with the MovieLens dataset. Specifically the ml-latest, which can be found inside the data folder. We decided on 3 main ideas and areas of research for our project.

## Main project ideas

1. Accumulated watch patterns: Based on the YouTube example from the lecture, we treat the timestamp of reviews as individual views. We take the top most reviewed movies released in and after 2000 (500 currently) and then model the growth rate based on the two models presented in class to group them into viral and non-viral.
(_Luca_)

2. Movie clustering based on two networks: Make a movie-movie graph based on content similarity using the genome dataset and one based on positive user reviews (maybe >4.0 or extract a statistical threshold for what is considered a good movie). Then cluster the movies and see what movies are bridges or central to a hub and compare them.

3. Follow an infection-based data modeling approach: Using something similar to the task in the assignment. Look at user spreading and the influence of users over time. Needs a smart approach to reduce the size of the network as it is quite extensive.

