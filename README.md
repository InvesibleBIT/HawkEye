
![alt text](https://github.com/InvesibleBIT/HawkEye/blob/master/w-he-logo-text.jpg)


## Inspiration
the crowd management is one the main issues in the Hajj, and we know there has been a lot of casualties in the past due to crowding in a single area or street. So with the Technology we have today we would like to help and assist with this problem

## What it does
Our software will create a **system that connect all CCTV cameras** in areas of interest such as Mina and Arafat areas, then it will monitor the traffic of people in these areas and provides a heat map for the area. The software will process the feeds from CCTV cameras and count people inside each street, then when a spot in the map started to be crowded the system will raise a flag to the authority to act quickly. Also, the heat map it will be very easy to predict if there is going to be a crowded area before it get crowded. 

## How I built it
Using openCV library to process the images and integrate it with heatmap framework and google maps.

## Challenges I ran into
we have ran into many challenges like:
each camera will find the count how many people had passed in front of it, but we need to build the relation between each camera to calculate the number of people in any specific zone.
In such crowded areas it become harder and harder to identify the moving objects.



## Accomplishments that we are proud of
Providing a ready prototype in a short time.Thinking of solution that can prevent a disasters from happening. Building a system that not only going to benefit single type of people, but instead every person in the Mina and Arafat area will benefit from this system by one way or another.


## What I learned
How to deal with OpenCV libraries. Also we learned how to divide the work into aspects with specified inputs and outputs which allowed us to work on all aspects of the system at the same time.

## What's next for HawkEye
Generalizing the solution for different government entity for traffic control.
To be more and more efficient in the future we will include AI in the software and with the needed training it will be more and more accurate over time. 
Make AI define patterns and the probability of an area to get crowded based on the given data from the heatmap

## project description
Software will be connected to all CCTV cameras in areas of interest such as Mina and Arafat areas, then it will monitor the traffic of people in these areas and provides a heat map for the area.
The backend built with python using OpenCV and the front end built with AngularJS

## The existing code before the hackathon
 [heatmap.js framework](https://www.patrick-wied.at/static/heatmapjs/)


