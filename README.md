# image-difference-outliner
Takes two images that have differences and generate outlines of those differences 

I developed a game called [Forgery Finder]("") that takes an artwork from a museum with some modifications and has the player find the differences. It's a spot the difference game that is mean to be played in person at a museum. The current flow for making the image is: 
--> Find museum images
--> Make the modifications
--> Outline the modificaitons in Inkscape using paths manually
--> Export the paths to a JSON config file
--> Import the config file into the app


I wanted to make it much easier to outline the images and use image processing to help me. The outline is important because it's a cool effect in the app. 
[GIF of outline animation]

I figured I can do this very easily by taking the difference of the images, then finding the edges, and converting that to a path. Obviously nothing is as straightforward as it seems. 

First problem the original image is a PNG and the modified one is a JPG. Yes, I can try to force the same image types but I already had these images and figured I can try to generalize this. 

The approach

1. Import the two images
2. Convert them to greyscale
3. Find the difference
4. Do some smoothing/noise reduction
5. 


