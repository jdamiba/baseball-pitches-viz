We will query the pybaseball API to get data about pitches they threw from MLB.com's Statcast database.

The first chart we can make using this player's pitch data is a scatter plot. We'll take each pitch and place it on the x-axis based on the order in which it was thrown. The first pitch in the data set will be all the way to the left and the last pitch in the data set will be all the way to the right.

On the y-axis we will plot the velocity of each pitch. The slowest pitch in the data set will be at the bottom while the fastest pitch in the data set will be at the top. In order to make the different pitches stand out from one another, we'll use different colors to plot each pitch.

The second chart we can make is a box plot. For this chart, we'll group similar pitches together on the x-axis. The y-axis will be the same as the scatter plot- the release speed of the pitch. We'll draw a shape around each pitch type describing the 25th and 75th percentiles as well as the median. Any points past the whiskers are outliers.