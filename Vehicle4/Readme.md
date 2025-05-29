Added a Method non_linear_Gauss_func for Gaussian-shaped speed response, So 
that, it will return a speed that is highest near peak_distance(near the source) and 
decreases as distance moves away from it, in this, the peak_distance is the 
amplitude (or height) of the Gaussian curve, Distance which is how far the vehicle 
is from the source is the mean of the curve and standard deviation is sigma, which 
controls the width of the curve.
