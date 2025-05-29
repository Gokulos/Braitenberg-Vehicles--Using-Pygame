It works like this, imagine the left side is closer to the 
source, then ls is higher. Then (rs – ls) gives a negative value, and 
when multiplied by -0.5, it gives a positive result, resulting in a 
clockwise turn. And, if the right side is closer, then rs is higher. In 
this case, rs - ls gives a positive value, and when multiplied by -0.5, 
the result is negative, causing an anticlockwise turn. 
for showing Aggression -- Change this line from this 
  rotation = (rs - ls) * self.rotation_scaling * -0.5
  to this
  rotation = (rs - ls) * self.rotation_scaling * 0.5
