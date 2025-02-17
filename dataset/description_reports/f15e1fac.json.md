# Task: f15e1fac.json

In the input, you should see...a many black grid with a few red squares and blue squares

The output grid size...the output grid is the same size

To make the output, you have to...copy the original grid. Imagine, but do not make, that the red blocks are actually parallel lines of red blocks Then for each blue square actually draw a line of blue squares as if you want the blue line to intersect the imaginary red line, but stop above where that line would be. Then for each blue line move one square over, or up or down, away from the original red block. Then, beginning in the place where the imaginary red line is draw another blue line in the same direction until you are above the next imaginary red line. Continue the pattern until you have reach the end of the grid. It should look like you are trying to draw a series of diagonal lines on grid paper

---

In the input, you should see...single blue either on the top or on the side and the single red on the side or the bottom.

The output grid size...stay the same

To make the output, you have to...fill in the blue continue with the single block down until a red block then you move to the right and continue down until you see another red block then move again to the right.  The red blocks indicate where the blue blocks should go.

---

In the input, you should see...black background with blue squares and red squares.

The output grid size...is the same as the input grid.

To make the output, you have to... First, copy the input grid and leave it as it is. The blue squares act as a starting point for you to draw lines, so if the blue squares are on the left, you have to draw lines horizontally to the right and if the blue squares are at the top, you have to draw the line vertically down. Next, after copying the grid, draw lines from each blue squares and stop just before the grid with the first red square. Then you will start again to draw your second blue lines starting from the grid with the red square, however, you will have to move your line by one grid according to the position of your red square - if your red square is at the bottom, you will move the second line up by one grid, if your red square is at the right, you will have to move your second line left by one grid and if your red square is at the left, you will have to move your second line to the right by one grid. These second blue lines stop just before the grid with the second red square. You will then draw another set of blue lines with the same rule as the second line all the way to the end of the grid.

---

