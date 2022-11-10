# image-difference-outliner
Takes two images that have differences and generate outlines of those differences. The outlines are output as SVG paths. 

I made a game called [Forgery Finder]("https://apps.apple.com/us/app/forgery-finder/id1641783715?ign-itscg=30200&ign-itsct=apps_box_promote_link") that takes an artwork from a museum and the play needs to find the differences between the artwork in the museum and what they see on the screen.  It's a spot the difference game that is meant to be played in person at a museum. 

Part of the game development is making images and the current flow for making the image is:  
--> Find museum images
--> Make the modifications
--> Outline the modificaitons in Inkscape using paths manually
--> Export the paths
--> Add the paths to a JSON config file
--> Import the config file into the app


I wanted to make it easier to outline the images and use image processing to help me. The outline is important because it's a cool effect in the app. 

![outline_sample](https://user-images.githubusercontent.com/11786205/201091464-edf338d6-546d-41d1-b6cc-c0a70327e463.gif)

I figured I can do this very easily by taking the difference of the images, then finding the edges, and converting that to a path. Obviously nothing is as straightforward as it seems. 

First problem the original image is a PNG and the modified one is a JPG. I can try to force the same image types but I already had these images and figured I can try to generalize this. 


The approach
1. Import the two images
2. Convert them to greyscale
3. Find the difference
4. Do some smoothing/noise reduction
5. Find the edges / contours
6. Convert the contours to SVG paths. 
  

### Limitations ###
1. The SVG paths are all straight lines so, curves don't come through as well.
2. The edge detection is more sensitive than the human eye or find differences where a human eye wouldn't.

